import reflex as rx
from typing import cast
from app.models import OrderWithCustomerName, Customer
from sqlalchemy import text
import datetime
import logging


class OrderCompletionState(rx.State):
    show_completion_dialog: bool = False
    is_processing: bool = False
    order_to_complete: OrderWithCustomerName | None = None
    customer_details: Customer | None = None
    payment_amount: float = 0.0
    payment_method: str = "cash"
    send_sms: bool = True
    send_whatsapp: bool = False
    show_success_screen: bool = False
    points_awarded: int = 0
    tier_upgraded_to: str | None = None
    referrer_reward: int | None = None
    notification_channels: list[str] = []

    @rx.event(background=True)
    async def start_completion(self, order_id: int):
        async with rx.asession() as session:
            order_res = await session.execute(
                text("""SELECT o.*, c.name as customer_name 
                       FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
                       WHERE o.order_id = :order_id"""),
                {"order_id": order_id},
            )
            order = order_res.mappings().first()
            if not order:
                yield rx.toast.error("Order not found.")
                return
            customer_res = await session.execute(
                text("SELECT * FROM customers WHERE customer_id = :customer_id"),
                {"customer_id": order["customer_id"]},
            )
            customer = customer_res.mappings().first()
        async with self:
            self.order_to_complete = cast(OrderWithCustomerName, dict(order))
            self.customer_details = cast(Customer, dict(customer)) if customer else None
            self.payment_amount = float(order["balance_payment"])
            self.send_sms = self.customer_details.get("prefer_whatsapp") != "whatsapp"
            self.send_whatsapp = self.customer_details.get(
                "opt_in_whatsapp"
            ) and self.customer_details.get("prefer_whatsapp") in ["whatsapp", "both"]
            self.show_completion_dialog = True
            self.show_success_screen = False
            self._reset_success_info()

    def _reset_success_info(self):
        self.points_awarded = 0
        self.tier_upgraded_to = None
        self.referrer_reward = None
        self.notification_channels = []

    @rx.event
    def close_dialog(self):
        self.show_completion_dialog = False
        self.is_processing = False
        self.order_to_complete = None
        self.customer_details = None
        self.show_success_screen = False

    @rx.event(background=True)
    async def complete_order(self, form_data: dict):
        async with self:
            if not self.order_to_complete or not self.customer_details:
                yield rx.toast.error("Session expired. Please try again.")
                return
            self.is_processing = True
        order_id = self.order_to_complete["order_id"]
        customer_id = self.order_to_complete["customer_id"]
        paid_amount = float(form_data.get("payment_amount", 0.0))
        payment_method = form_data.get("payment_method", "cash")
        from app.state import OrderState

        async with rx.asession() as session, session.begin():
            await session.execute(
                text("""INSERT INTO transactions (order_id, transaction_date, transaction_type, amount, payment_method, description)
                     VALUES (:order_id, :date, 'order_payment', :amount, :method, 'Final balance payment')"""),
                {
                    "order_id": order_id,
                    "date": datetime.date.today(),
                    "amount": paid_amount,
                    "method": payment_method,
                },
            )
            await session.execute(
                text(
                    "UPDATE orders SET balance_payment = balance_payment - :paid WHERE order_id = :order_id"
                ),
                {"paid": paid_amount, "order_id": order_id},
            )
            await session.execute(
                text(
                    "UPDATE orders SET status = 'delivered', delivery_date = :date WHERE order_id = :order_id"
                ),
                {"date": datetime.date.today(), "order_id": order_id},
            )
            order_info_res = await session.execute(
                text(
                    "SELECT total_amount, discount_amount FROM orders WHERE order_id = :id"
                ),
                {"id": order_id},
            )
            order_info = order_info_res.mappings().first()
            final_amount = float(
                order_info["total_amount"] - (order_info["discount_amount"] or 0)
            )
            points_earned = int(final_amount / 100)
            cust_res = await session.execute(
                text(
                    "SELECT total_points, customer_tier FROM customers WHERE customer_id = :cid"
                ),
                {"cid": customer_id},
            )
            customer_data = cust_res.mappings().first()
            current_points = customer_data["total_points"]
            new_total_points = current_points + points_earned
            current_tier = customer_data["customer_tier"]
            new_tier = current_tier
            if new_total_points > 2000 and current_tier != "vip":
                new_tier = "vip"
            elif new_total_points > 500 and current_tier not in ["vip", "regular"]:
                new_tier = "regular"
            await session.execute(
                text(
                    "UPDATE customers SET total_points = :points, customer_tier = :tier WHERE customer_id = :cid"
                ),
                {"points": new_total_points, "tier": new_tier, "cid": customer_id},
            )
            await session.execute(
                text("""INSERT INTO loyalty_points (customer_id, points_change, new_balance, transaction_type, order_id, description)
                     VALUES (:cid, :points, :balance, 'purchase', :oid, :desc)"""),
                {
                    "cid": customer_id,
                    "points": points_earned,
                    "balance": new_total_points,
                    "oid": order_id,
                    "desc": f"Points from order #{order_id}",
                },
            )
            async with self:
                self.points_awarded = points_earned
                if new_tier != current_tier:
                    self.tier_upgraded_to = new_tier.capitalize()
            referral_check = await session.execute(
                text("""SELECT r.referral_id, r.referrer_customer_id, r.reward_points, c.name as referrer_name 
                     FROM customer_referrals r JOIN customers c ON r.referrer_customer_id = c.customer_id
                     WHERE r.referred_customer_id = :referred_id AND r.referral_status = 'pending'"""),
                {"referred_id": customer_id},
            )
            referral_info = referral_check.mappings().first()
            order_count_check = await session.execute(
                text(
                    "SELECT COUNT(*) FROM orders WHERE customer_id = :cid AND status = 'delivered'"
                ),
                {"cid": customer_id},
            )
            if referral_info and order_count_check.scalar_one() == 1:
                referrer_id, reward_points = (
                    referral_info["referrer_customer_id"],
                    referral_info["reward_points"],
                )
                referrer_cust_res = await session.execute(
                    text("SELECT total_points FROM customers WHERE customer_id = :rid"),
                    {"rid": referrer_id},
                )
                new_referrer_points = referrer_cust_res.scalar_one() + reward_points
                await session.execute(
                    text(
                        "UPDATE customers SET total_points = :points WHERE customer_id = :rid"
                    ),
                    {"points": new_referrer_points, "rid": referrer_id},
                )
                await session.execute(
                    text("""INSERT INTO loyalty_points (customer_id, points_change, new_balance, transaction_type, description)
                                     VALUES (:cid, :points, :balance, 'referral', :desc)"""),
                    {
                        "cid": referrer_id,
                        "points": reward_points,
                        "balance": new_referrer_points,
                        "desc": f"Referral bonus for {self.customer_details['name']}",
                    },
                )
                await session.execute(
                    text(
                        "UPDATE customer_referrals SET referral_status = 'completed', completed_date = :date, order_completed = TRUE WHERE referral_id = :ref_id"
                    ),
                    {
                        "date": datetime.date.today(),
                        "ref_id": referral_info["referral_id"],
                    },
                )
                async with self:
                    self.referrer_reward = reward_points
                yield rx.toast.success(
                    f"Referrer {referral_info['referrer_name']} awarded {reward_points} points!"
                )
        customer_name = self.customer_details["name"]
        customer_phone = self.customer_details["phone_number"]
        notification_channels = []
        if form_data.get("send_sms") == "on":
            from app.utils.sms import send_status_update_notification

            if send_status_update_notification(
                customer_phone, customer_name, order_id, "delivered"
            ):
                notification_channels.append("SMS")
        if form_data.get("send_whatsapp") == "on":
            from app.utils.whatsapp import send_whatsapp_status_update

            if send_whatsapp_status_update(
                customer_phone, customer_name, order_id, "delivered"
            ):
                notification_channels.append("WhatsApp")
        from app.utils.pdf import generate_invoice_pdf
        from app.utils.email import send_email

        pdf_path = generate_invoice_pdf(self.order_to_complete, self.customer_details)
        if pdf_path and self.customer_details.get("email"):
            email_body = f"<p>Hi {customer_name},</p>\n                         <p>Thank you for your business! Please find attached the invoice for your recent order #{order_id}.</p>\n                         <p>We appreciate your timely payment.</p>\n                         <p>Best regards,<br/>The TailorFlow Team</p>"
            email_sent = send_email(
                to_email=self.customer_details["email"],
                subject=f"Invoice for Order #{order_id}",
                body=email_body,
                attachment_path=pdf_path,
                attachment_filename=pdf_path.split("/")[-1],
            )
            if email_sent:
                notification_channels.append("Email Invoice")
        async with self:
            self.notification_channels = notification_channels
            self.is_processing = False
            self.show_success_screen = True
            order_state = await self.get_state(OrderState)
            yield order_state.get_orders