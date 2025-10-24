import reflex as rx
from typing import cast, Any
from app.models import PaymentInstallment, OrderWithCustomerName
from sqlalchemy import text
import datetime


class PaymentState(rx.State):
    installments: list[PaymentInstallment] = []
    orders_with_balance: list[OrderWithCustomerName] = []
    show_installment_form: bool = False
    is_editing: bool = False
    editing_installment_id: int | None = None
    selected_order_id: str = ""
    installment_amount: float = 0.0
    due_date: str = ""
    notes: str = ""

    @rx.event(background=True)
    async def get_all_installments(self):
        async with rx.asession() as session:
            installments_result = await session.execute(
                text("""SELECT pi.*, c.name as customer_name, c.phone_number as customer_phone
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
        self.installment_amount = 0.0
        self.due_date = ""
        self.notes = ""

    @rx.event
    def toggle_installment_form(self):
        self.show_installment_form = not self.show_installment_form
        self._reset_form()

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
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE payment_installments 
                     SET status = 'paid', paid_date = :paid_date
                     WHERE installment_id = :installment_id"""),
                {"installment_id": installment_id, "paid_date": datetime.date.today()},
            )
            await session.commit()
        async with self:
            yield PaymentState.get_all_installments
            yield rx.toast.success(f"Installment #{installment_id} marked as paid.")

    @rx.event(background=True)
    async def send_reminder_sms(self, installment: PaymentInstallment):
        from app.utils.sms import send_payment_reminder

        sms_sent = send_payment_reminder(
            customer_phone=installment["customer_phone"],
            customer_name=installment["customer_name"],
            order_id=installment["order_id"],
            due_date=str(installment["due_date"]),
            amount=float(installment["amount"]),
        )
        async with self:
            if sms_sent:
                yield rx.toast.success(
                    f"Payment reminder sent for order #{installment['order_id']}."
                )
            else:
                yield rx.toast.error("Failed to send payment reminder SMS.")