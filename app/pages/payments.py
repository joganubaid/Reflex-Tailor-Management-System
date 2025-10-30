import reflex as rx
from app.states.payment_state import PaymentState
from app.components.sidebar import sidebar, mobile_header
from app.components.payment_form import payment_installment_form

STATUS_COLORS = {
    "paid": "bg-green-100 text-green-800",
    "pending": "bg-yellow-100 text-yellow-800",
    "overdue": "bg-red-100 text-red-800",
}


def payment_status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status.lower(),
            ("paid", STATUS_COLORS["paid"] + base_classes),
            ("pending", STATUS_COLORS["pending"] + base_classes),
            ("overdue", STATUS_COLORS["overdue"] + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def installment_row(installment: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            f"#{installment['order_id']}",
            class_name="px-6 py-4 font-medium text-gray-900",
        ),
        rx.el.td(installment["customer_name"], class_name="px-6 py-4"),
        rx.el.td(
            installment["installment_number"].to_string(),
            class_name="px-6 py-4 text-center",
        ),
        rx.el.td(
            f"₹{installment['amount'].to_string()}",
            class_name="px-6 py-4 font-semibold",
        ),
        rx.el.td(
            installment["due_date"].to_string().split("T")[0], class_name="px-6 py-4"
        ),
        rx.el.td(payment_status_badge(installment["status"]), class_name="px-6 py-4"),
        rx.el.td(
            rx.cond(
                installment["paid_date"],
                installment["paid_date"].to_string().split("T")[0],
                "-",
            ),
            class_name="px-6 py-4 text-center",
        ),
        rx.el.td(
            rx.cond(
                installment["last_reminder_sent"],
                installment["last_reminder_sent"].to_string().split("T")[0],
                "-",
            ),
            class_name="px-6 py-4 text-center",
        ),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    installment["status"] != "paid",
                    rx.el.button(
                        rx.icon("check_check", class_name="h-4 w-4 mr-1"),
                        "Mark Paid",
                        on_click=lambda: PaymentState.mark_as_paid(
                            installment["installment_id"]
                        ),
                        class_name="flex items-center px-3 py-1.5 text-xs font-medium text-green-600 border border-green-200 rounded-md hover:bg-green-50",
                    ),
                    rx.el.span("", class_name="w-24"),
                ),
                rx.cond(
                    installment["status"] != "paid",
                    rx.el.button(
                        rx.icon("send", class_name="h-4 w-4 mr-1"),
                        "Reminder",
                        on_click=lambda: PaymentState.send_reminder_sms(installment),
                        class_name="flex items-center px-3 py-1.5 text-xs font-medium text-blue-600 border border-blue-200 rounded-md hover:bg-blue-50",
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def payments_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Payment Management",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Track all payment installments and send reminders.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search by customer or order ID...",
                            type="search",
                            class_name="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            on_change=PaymentState.set_search_query,
                        ),
                        class_name="relative w-full md:w-80",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="md:mr-2 h-5 w-5"),
                        rx.el.span("Add Installment", class_name="hidden md:inline"),
                        on_click=PaymentState.toggle_installment_form,
                        class_name="flex items-center justify-center bg-purple-600 text-white p-2 md:px-4 md:py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                    ),
                    class_name="flex flex-col md:flex-row justify-between items-center mb-6 gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Order ID",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Customer",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Installment",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Amount",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Due Date",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Paid On",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Last Reminder",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        PaymentState.filtered_installments,
                                        installment_row,
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            PaymentState.filtered_installments.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "indian-rupee",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "No Payment Installments Found",
                                    class_name="text-lg font-semibold text-gray-700",
                                ),
                                rx.el.p(
                                    "Add payment installments for orders to track them here.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="bg-white p-2 md:p-6 rounded-xl shadow-sm",
                ),
                payment_installment_form(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )