import reflex as rx
from typing import cast
from app.models import PaymentInstallment
from sqlalchemy import text
from app.utils.sms import send_payment_reminder
from app.utils.razorpay import create_payment_link
import os


class PaymentState(rx.State):
    is_loading: bool = False
    all_installments: list[PaymentInstallment] = []
    search_query: str = ""
    status_filter: str = "all"

    @rx.var
    def filtered_installments(self) -> list[PaymentInstallment]:
        installments = self.all_installments
        if self.status_filter != "all":
            installments = [
                i for i in installments if i["status"] == self.status_filter
            ]
        if self.search_query.strip():
            lower_query = self.search_query.lower()
            installments = [
                i for i in installments if lower_query in i["customer_name"].lower()
            ]
        return installments

    @rx.event(background=True)
    async def get_all_installments(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT pi.*, c.name as customer_name, c.phone_number as customer_phone
                     FROM payment_installments pi
                     JOIN orders o ON pi.order_id = o.order_id
                     JOIN customers c ON o.customer_id = c.customer_id
                     ORDER BY pi.due_date""")
            )
            rows = result.mappings().all()
            async with self:
                self.all_installments = [
                    cast(PaymentInstallment, dict(row)) for row in rows
                ]
                self.is_loading = False

    @rx.event(background=True)
    async def send_reminder_sms(self, installment_id: int):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT pi.*, c.name as customer_name, c.phone_number as customer_phone
                         FROM payment_installments pi
                         JOIN orders o ON pi.order_id = o.order_id
                         JOIN customers c ON o.customer_id = c.customer_id
                         WHERE pi.installment_id = :installment_id"""),
                {"installment_id": installment_id},
            )
            installment = result.mappings().first()
        if installment:
            link = create_payment_link(
                amount=float(installment["amount"]),
                description=f"Payment for Order #{installment['order_id']}",
                customer_name=installment["customer_name"],
                customer_contact=installment["customer_phone"],
                customer_email=None,
                order_id=installment["order_id"],
            )
            sent = send_payment_reminder(
                customer_phone=installment["customer_phone"],
                customer_name=installment["customer_name"],
                order_id=installment["order_id"],
                due_date=str(installment["due_date"]),
                amount=float(installment["amount"]),
                payment_link=link,
            )
            if sent:
                async with self:
                    yield rx.toast.success("Reminder SMS sent!")
                async with rx.asession() as session:
                    await session.execute(
                        text(
                            "UPDATE payment_installments SET last_reminder_sent = NOW() WHERE installment_id = :id"
                        ),
                        {"id": installment_id},
                    )
                    await session.commit()
            else:
                async with self:
                    yield rx.toast.error("Failed to send SMS.")

    @rx.event
    async def resend_payment_link(self, installment_id: int):
        yield PaymentState.send_reminder_sms(installment_id)


@rx.page(route="/payment-success")
def payment_success():
    return rx.el.div(
        rx.icon("check_check", class_name="text-green-500 text-6xl mx-auto mb-4"),
        rx.el.h1("Payment Successful!", class_name="text-3xl font-bold text-center"),
        rx.el.p(
            "Your payment has been processed and your order is updated.",
            class_name="text-center mt-2",
        ),
        rx.el.a(
            "Back to Dashboard",
            href="/dashboard",
            class_name="mt-6 bg-purple-600 text-white px-4 py-2 rounded-lg",
        ),
        class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50",
    )


@rx.page(route="/payment-failure")
def payment_failure():
    return rx.el.div(
        rx.icon("circle_x", class_name="text-red-500 text-6xl mx-auto mb-4"),
        rx.el.h1("Payment Failed", class_name="text-3xl font-bold text-center"),
        rx.el.p(
            "There was an issue with your payment. Please try again or contact support.",
            class_name="text-center mt-2",
        ),
        rx.el.a(
            "Try Again",
            href="/orders",
            class_name="mt-6 bg-purple-600 text-white px-4 py-2 rounded-lg",
        ),
        class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50",
    )