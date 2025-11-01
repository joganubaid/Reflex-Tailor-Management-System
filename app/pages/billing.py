import reflex as rx
from app.states.payment_state import PaymentState
from app.components.sidebar import sidebar, mobile_header
from app.components.payment_form import payment_installment_form

STATUS_COLORS = {
    "pending": "bg-yellow-100 text-yellow-800",
    "paid": "bg-green-100 text-green-800",
    "overdue": "bg-red-100 text-red-800",
}


def status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status.lower(),
            ("pending", STATUS_COLORS["pending"] + base_classes),
            ("paid", STATUS_COLORS["paid"] + base_classes),
            ("overdue", STATUS_COLORS["overdue"] + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def installment_card(installment: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"Order #{installment['order_id']}",
                    class_name="font-bold text-gray-800",
                ),
                rx.el.p(
                    installment["customer_name"], class_name="text-sm text-gray-600"
                ),
            ),
            status_badge(installment["status"]),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Due Date", class_name="text-xs text-gray-500"),
                rx.el.p(
                    installment["due_date"].to_string().split("T")[0],
                    class_name="font-medium",
                ),
            ),
            rx.el.div(
                rx.el.p("Amount", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"\u2009{installment['amount'].to_string()}",
                    class_name="font-bold text-lg text-purple-600",
                ),
            ),
            class_name="grid grid-cols-2 gap-4 mt-3 pt-3 border-t",
        ),
        rx.el.div(
            rx.el.button(
                "Send Reminder",
                on_click=lambda: PaymentState.send_reminder_sms(installment),
                class_name=rx.cond(
                    installment["status"] != "paid",
                    "px-3 py-1.5 text-xs bg-blue-100 text-blue-700 rounded-md font-semibold",
                    "hidden",
                ),
            ),
            rx.el.button(
                "Mark as Paid",
                on_click=lambda: PaymentState.mark_as_paid(
                    installment["installment_id"]
                ),
                class_name=rx.cond(
                    installment["status"] != "paid",
                    "px-3 py-1.5 text-xs bg-green-100 text-green-700 rounded-md font-semibold",
                    "hidden",
                ),
            ),
            class_name="flex gap-2 justify-end mt-3 pt-3 border-t",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def installment_row(installment: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            f"#{installment['order_id']}",
            class_name="px-6 py-4 font-medium text-gray-900",
        ),
        rx.el.td(installment["customer_name"], class_name="px-6 py-4"),
        rx.el.td(
            installment["due_date"].to_string().split("T")[0], class_name="px-6 py-4"
        ),
        rx.el.td(
            f"\u2009{installment['amount'].to_string()}",
            class_name="px-6 py-4 font-semibold text-purple-600",
        ),
        rx.el.td(status_badge(installment["status"]), class_name="px-6 py-4"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Send Reminder",
                    on_click=lambda: PaymentState.send_reminder_sms(installment),
                    class_name=rx.cond(
                        installment["status"] != "paid",
                        "px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded",
                        "hidden",
                    ),
                ),
                rx.el.button(
                    "Mark Paid",
                    on_click=lambda: PaymentState.mark_as_paid(
                        installment["installment_id"]
                    ),
                    class_name=rx.cond(
                        installment["status"] != "paid",
                        "px-2 py-1 text-xs bg-green-100 text-green-700 rounded",
                        "hidden",
                    ),
                ),
                class_name="flex gap-2",
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
                rx.el.div(
                    rx.el.h1(
                        "Payment Management",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Track upcoming and overdue payments.",
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
                            on_change=PaymentState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg",
                        ),
                        class_name="relative",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Add Installment",
                        on_click=PaymentState.toggle_installment_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(
                            PaymentState.filtered_installments, installment_card
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:hidden",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Order ID",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Customer",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Due Date",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Amount",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
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
                            (PaymentState.filtered_installments.length() == 0)
                            & ~PaymentState.is_loading,
                            rx.el.div(
                                rx.icon(
                                    "dollar-sign",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "No Payments Found",
                                    class_name="text-lg font-semibold",
                                ),
                                rx.el.p(
                                    "All payments are up to date!",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="hidden md:block overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="md:bg-white md:p-6 rounded-xl shadow-sm",
                ),
                payment_installment_form(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )