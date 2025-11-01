import reflex as rx
from app.states.payment_state import PaymentState
from app.components.sidebar import sidebar, mobile_header


def payment_installment_row(installment: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(f"#{installment['order_id']}", class_name="px-6 py-4"),
        rx.el.td(installment["customer_name"], class_name="px-6 py-4 font-medium"),
        rx.el.td(f"₹{installment['amount']}", class_name="px-6 py-4 font-semibold"),
        rx.el.td(
            installment["due_date"].to_string().split("T")[0], class_name="px-6 py-4"
        ),
        rx.el.td(
            rx.el.span(
                installment["status"].capitalize(),
                class_name=rx.cond(
                    installment["status"] == "paid",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-700",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-700",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.cond(
                installment["status"] == "pending",
                rx.el.div(
                    rx.el.button(
                        "Send Reminder",
                        on_click=lambda: PaymentState.send_reminder_sms(
                            installment["installment_id"]
                        ),
                        class_name="text-sm text-blue-600 hover:underline",
                    ),
                    rx.el.button(
                        "Resend Link",
                        on_click=lambda: PaymentState.resend_payment_link(
                            installment["installment_id"]
                        ),
                        class_name="text-sm text-purple-600 hover:underline ml-2",
                    ),
                ),
                rx.el.p("Paid", class_name="text-sm text-gray-500"),
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def payments_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Payment Management",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search by customer name...",
                        on_change=PaymentState.set_search_query,
                        class_name="w-full md:w-72 p-2 border rounded-lg",
                    ),
                    rx.el.select(
                        rx.el.option("All Statuses", value="all"),
                        rx.el.option("Pending", value="pending"),
                        rx.el.option("Paid", value="paid"),
                        value=PaymentState.status_filter,
                        on_change=PaymentState.set_status_filter,
                        class_name="w-full md:w-48 p-2 border rounded-lg bg-white",
                    ),
                    class_name="flex flex-col md:flex-row gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th("Order ID"),
                                rx.el.th("Customer"),
                                rx.el.th("Amount"),
                                rx.el.th("Due Date"),
                                rx.el.th("Status"),
                                rx.el.th("Actions"),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                PaymentState.filtered_installments,
                                payment_installment_row,
                            )
                        ),
                        class_name="w-full text-left table-auto",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm overflow-x-auto",
                ),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )