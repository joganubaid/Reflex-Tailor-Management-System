import reflex as rx
from typing import cast, TypedDict
from app.models import PaymentInstallment, OrderWithCustomerName
from sqlalchemy import text
import datetime


class SuggestedCreditTerms(TypedDict):
    score: float
    rating: str
    advance_free_eligible: bool
    max_credit_days: int


class PaymentState(rx.State):
    installments: list[PaymentInstallment] = []
    orders_with_balance: list[OrderWithCustomerName] = []
    show_installment_form: bool = False
    is_editing: bool = False
    editing_installment_id: int | None = None
    selected_order_id: str = ""
    installment_amount: str = ""
    due_date: str = ""
    notes: str = ""
    search_query: str = ""
    customer_credit_scores: dict[int, float] = {}
    credit_terms_available: dict[int, bool] = {}
    suggested_credit_terms: SuggestedCreditTerms = {}

    async def _calculate_payment_punctuality(self, customer_id: int) -> float:
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT pi.due_date, pi.paid_date 
                       FROM payment_installments pi
                       JOIN orders o ON pi.order_id = o.order_id
                       WHERE o.customer_id = :customer_id AND pi.status = 'paid'"""),
                {"customer_id": customer_id},
            )
            installments = result.mappings().all()
        if not installments:
            return 100.0
        on_time_payments = sum(
            (
                1
                for i in installments
                if i["paid_date"]
                and i["due_date"]
                and (i["paid_date"] <= i["due_date"])
            )
        )
        return on_time_payments / len(installments) * 100

    @rx.event(background=True)
    async def update_customer_credit_score(self, customer_id: int):
        punctuality = await self._calculate_payment_punctuality(customer_id)
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT customer_tier FROM customers WHERE customer_id = :customer_id"
                ),
                {"customer_id": customer_id},
            )
            customer = result.mappings().first()
        if not customer:
            return
        tier = customer["customer_tier"]
        tier_bonus = {"vip": 30, "regular": 20, "new": 10}.get(tier, 0)
        score = punctuality * 0.7 + tier_bonus
        async with self:
            self.customer_credit_scores[customer_id] = score
            self.credit_terms_available[customer_id] = score > 80

    @rx.event(background=True)
    async def get_credit_terms_suggestion(self, customer_id: int):
        async with self:
            if customer_id not in self.customer_credit_scores:
                yield PaymentState.update_customer_credit_score(customer_id)
        async with self:
            score = self.customer_credit_scores.get(customer_id, 0)
            if score > 90:
                rating, max_credit_days = ("Excellent", 30)
            elif score > 70:
                rating, max_credit_days = ("Good", 15)
            elif score > 50:
                rating, max_credit_days = ("Fair", 7)
            else:
                rating, max_credit_days = ("Poor", 0)
            self.suggested_credit_terms = {
                "score": score,
                "rating": rating,
                "advance_free_eligible": self.credit_terms_available.get(
                    customer_id, False
                ),
                "max_credit_days": max_credit_days,
            }
        yield rx.toast.info(f"Credit suggestion loaded for customer #{customer_id}")

    @rx.var
    def filtered_installments(self) -> list[PaymentInstallment]:
        today = datetime.date.today()
        processed_installments = []
        for inst in self.installments:
            inst_copy = inst.copy()
            due_date = datetime.datetime.strptime(
                str(inst_copy["due_date"]).split(" ")[0], "%Y-%m-%d"
            ).date()
            if inst_copy["status"] == "pending" and due_date < today:
                inst_copy["status"] = "overdue"
            processed_installments.append(inst_copy)
        if not self.search_query:
            return processed_installments
        lower_query = self.search_query.lower()
        return [
            i
            for i in processed_installments
            if lower_query in i["customer_name"].lower()
            or str(i["order_id"]) == lower_query
        ]

    @rx.event(background=True)
    async def get_all_installments(self):
        async with rx.asession() as session:
            installments_result = await session.execute(
                text("""SELECT pi.*, c.name as customer_name, c.phone_number as customer_phone,
                            (SELECT MAX(pr.sent_date) FROM payment_reminders pr WHERE pr.installment_id = pi.installment_id) as last_reminder_sent
                     FROM payment_installments pi
                     JOIN orders o ON pi.order_id = o.order_id
                     JOIN customers c ON o.customer_id = c.customer_id
                     ORDER BY pi.due_date DESC""")
            )
            orders_result = await session.execute(
                text("""SELECT o.*, c.name as customer_name 
                         FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
                         WHERE o.balance_payment > 0 ORDER BY o.order_id DESC""")
            )
            async with self:
                self.installments = [
                    cast(PaymentInstallment, dict(row))
                    for row in installments_result.mappings().all()
                ]
                self.orders_with_balance = [
                    cast(OrderWithCustomerName, dict(row))
                    for row in orders_result.mappings().all()
                ]

    def _reset_form(self):
        self.is_editing = False
        self.editing_installment_id = None
        self.selected_order_id = ""
        self.installment_amount = ""
        self.due_date = ""
        self.notes = ""

    @rx.event
    def toggle_installment_form(self):
        self.show_installment_form = not self.show_installment_form
        self._reset_form()
        if self.show_installment_form:
            return PaymentState.get_all_installments

    @rx.event(background=True)
    async def handle_form_submit(self, form_data: dict):
        order_id = int(self.selected_order_id)
        async with rx.asession() as session:
            count_result = await session.execute(
                text(
                    "SELECT COUNT(*) FROM payment_installments WHERE order_id = :order_id"
                ),
                {"order_id": order_id},
            )
            installment_number = (count_result.scalar_one_or_none() or 0) + 1
            await session.execute(
                text("""INSERT INTO payment_installments (order_id, installment_number, amount, due_date, status, notes)
                     VALUES (:order_id, :installment_number, :amount, :due_date, 'pending', :notes)"""),
                {
                    "order_id": order_id,
                    "installment_number": installment_number,
                    "amount": float(form_data.get("installment_amount", 0.0)),
                    "due_date": form_data.get("due_date"),
                    "notes": form_data.get("notes"),
                },
            )
            await session.commit()
        async with self:
            self.show_installment_form = False
        yield PaymentState.get_all_installments
        yield rx.toast.success("Installment added successfully!")

    @rx.event(background=True)
    async def mark_as_paid(self, installment_id: int):
        from app.state import OrderState

        async with rx.asession() as session, session.begin():
            result = await session.execute(
                text("""UPDATE payment_installments 
                     SET status = 'paid', paid_date = :paid_date, payment_method = 'cash'
                     WHERE installment_id = :installment_id
                     RETURNING order_id, amount"""),
                {"installment_id": installment_id, "paid_date": datetime.date.today()},
            )
            res = result.mappings().first()
            if not res:
                yield rx.toast.error("Failed to update payment. Installment not found.")
                return
            order_id = res["order_id"]
            paid_amount = res["amount"]
            await session.execute(
                text(
                    "UPDATE orders SET balance_payment = balance_payment - :paid WHERE order_id = :order_id"
                ),
                {"paid": paid_amount, "order_id": order_id},
            )
            balance_res = await session.execute(
                text(
                    "SELECT balance_payment, status FROM orders WHERE order_id = :order_id"
                ),
                {"order_id": order_id},
            )
            order_details = balance_res.mappings().first()
        async with self:
            yield rx.toast.success(f"Installment #{installment_id} marked as paid.")
            if order_details and order_details["balance_payment"] <= 0:
                if order_details["status"] not in ["delivered", "ready", "finishing"]:
                    from app.state import OrderState

                    order_state = await self.get_state(OrderState)
                    yield order_state.update_order_status(order_id, "finishing")
                    yield rx.toast.info("Order fully paid and moved to finishing.")
                else:
                    yield rx.toast.info("Order fully paid.")
            yield PaymentState.get_all_installments
            from app.state import OrderState

            order_state_for_refresh = await self.get_state(OrderState)
            yield order_state_for_refresh.get_orders

    async def _create_payment_link_for_installment(
        self, installment: PaymentInstallment
    ) -> str | None:
        from app.utils.razorpay import create_payment_link
        import logging

        try:
            link = create_payment_link(
                amount=float(installment.get("amount", 0.0)),
                description=f"Payment for Order #{installment.get('order_id')}, Installment #{installment.get('installment_number')}",
                customer_name=installment.get("customer_name", ""),
                customer_contact=installment.get("customer_phone", ""),
                customer_email=None,
                order_id=installment.get("order_id"),
            )
            return link
        except Exception as e:
            logging.exception(
                f"Error creating payment link for installment {installment.get('installment_id')}: {e}"
            )
            return None

    @rx.event(background=True)
    async def send_reminder_sms(self, installment: PaymentInstallment):
        from app.utils.sms import send_payment_reminder

        payment_link = await self._create_payment_link_for_installment(installment)
        if not payment_link:
            yield rx.toast.error("Could not generate payment link.")
            return
        sms_sent = send_payment_reminder(
            customer_phone=installment["customer_phone"],
            customer_name=installment["customer_name"],
            order_id=installment["order_id"],
            due_date=str(installment["due_date"]),
            amount=float(installment["amount"]),
            payment_link=payment_link,
        )
        async with self:
            if sms_sent:
                async with rx.asession() as session:
                    await session.execute(
                        text("""INSERT INTO payment_reminders (installment_id, reminder_date, sent_date, status)
                             VALUES (:installment_id, :reminder_date, :sent_date, 'sent')"""),
                        {
                            "installment_id": installment["installment_id"],
                            "reminder_date": datetime.date.today(),
                            "sent_date": datetime.datetime.now(),
                        },
                    )
                    await session.commit()
                yield rx.toast.success(
                    f"Payment reminder sent for order #{installment['order_id']}."
                )
                yield PaymentState.get_all_installments
            else:
                yield rx.toast.error("Failed to send payment reminder SMS.")

    @rx.event(background=True)
    async def check_and_send_payment_reminders(self):
        """Checks for overdue installments and sends reminders."""
        async with rx.asession() as session:
            overdue_installments_res = await session.execute(
                text("""SELECT pi.*, c.name as customer_name, c.phone_number as customer_phone
                       FROM payment_installments pi
                       JOIN orders o ON pi.order_id = o.order_id
                       JOIN customers c ON o.customer_id = c.customer_id
                       WHERE pi.status = 'pending' AND pi.due_date <= :today
                       AND NOT EXISTS (
                           SELECT 1 FROM payment_reminders pr 
                           WHERE pr.installment_id = pi.installment_id 
                           AND pr.reminder_date = :today
                       )"""),
                {"today": datetime.date.today()},
            )
            installments_to_remind = overdue_installments_res.mappings().all()
        for inst in installments_to_remind:
            async with self:
                yield PaymentState.send_reminder_sms(dict(inst))