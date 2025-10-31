import reflex as rx
from app.state import BillingState
from app.components.sidebar import sidebar, mobile_header

STATUS_COLORS = {
    "paid": "bg-green-100 text-green-800",
    "partial": "bg-yellow-100 text-yellow-800",
    "pending": "bg-red-100 text-red-800",
}


def payment_status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status.lower(),
            ("paid", STATUS_COLORS["paid"] + base_classes),
            ("partial", STATUS_COLORS["partial"] + base_classes),
            ("pending", STATUS_COLORS["pending"] + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def billing_order_card(order: rx.Var[dict]) -> rx.Component:
    payment_status = rx.cond(
        order["balance_payment"] == 0,
        "Paid",
        rx.cond(order["advance_payment"] > 0, "Partial", "Pending"),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"Order #{order['order_id']}", class_name="font-bold text-gray-800"
                ),
                payment_status_badge(payment_status),
            ),
            rx.el.p(order["customer_name"], class_name="text-sm text-gray-600"),
            class_name="flex justify-between items-center mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Total", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"₹{order['total_amount']}",
                    class_name="font-semibold text-gray-700",
                ),
            ),
            rx.el.div(
                rx.el.p("Advance", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"₹{order['advance_payment']}",
                    class_name="font-semibold text-gray-700",
                ),
            ),
            rx.el.div(
                rx.el.p("Balance", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"₹{order['balance_payment']}", class_name="font-bold text-red-600"
                ),
            ),
            class_name="grid grid-cols-3 gap-4 py-3 border-t border-b",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("file-text", class_name="h-4 w-4 mr-2"),
                "Invoice",
                class_name="flex items-center px-3 py-1.5 text-xs font-medium text-purple-600 border border-purple-200 rounded-md hover:bg-purple-50",
            ),
            rx.el.button(
                rx.icon("credit-card", class_name="h-4 w-4 mr-2"),
                "Pay",
                class_name="flex items-center px-3 py-1.5 text-xs font-medium text-green-600 border border-green-200 rounded-md hover:bg-green-50",
            ),
            class_name="flex items-center justify-end gap-2 mt-3",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def billing_order_row(order: rx.Var[dict]) -> rx.Component:
    payment_status = rx.cond(
        order["balance_payment"] == 0,
        "Paid",
        rx.cond(order["advance_payment"] > 0, "Partial", "Pending"),
    )
    return rx.el.tr(
        rx.el.td(
            f"#{order['order_id']}", class_name="px-6 py-4 font-medium text-gray-900"
        ),
        rx.el.td(order["customer_name"], class_name="px-6 py-4"),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    order["order_date"],
                    order["order_date"].to_string().split("T")[0],
                    "N/A",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            f"₹{order['total_amount'].to_string()}", class_name="px-6 py-4 font-medium"
        ),
        rx.el.td(f"₹{order['advance_payment'].to_string()}", class_name="px-6 py-4"),
        rx.el.td(
            f"₹{order['balance_payment'].to_string()}",
            class_name=rx.cond(
                order["balance_payment"] > 0,
                "px-6 py-4 text-red-600 font-medium",
                "px-6 py-4 font-medium",
            ),
        ),
        rx.el.td(payment_status_badge(payment_status), class_name="px-6 py-4"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-text", class_name="h-4 w-4 mr-2"),
                    "Invoice",
                    class_name="flex items-center px-3 py-1.5 text-xs font-medium text-purple-600 border border-purple-200 rounded-md hover:bg-purple-50",
                ),
                rx.el.button(
                    rx.icon("credit-card", class_name="h-4 w-4 mr-2"),
                    "Pay",
                    class_name="flex items-center px-3 py-1.5 text-xs font-medium text-green-600 border border-green-200 rounded-md hover:bg-green-50",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def billing_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Billing & Invoices",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Manage invoices, payments, and view transaction history.",
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
                            placeholder="Search by order ID or customer...",
                            class_name="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                        ),
                        class_name="relative w-full md:w-80",
                    ),
                    rx.el.select(
                        rx.el.option("All Statuses", value="all"),
                        rx.el.option("Paid", value="paid"),
                        rx.el.option("Partial", value="partial"),
                        rx.el.option("Pending", value="pending"),
                        class_name="w-full md:w-auto px-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500 bg-white",
                    ),
                    class_name="flex flex-col md:flex-row justify-between items-center mb-6 gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(BillingState.orders_for_billing, billing_order_card),
                        class_name="grid grid-cols-1 gap-4 md:hidden",
                    ),
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
                                            "Order Date",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Total",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Advance",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Balance",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Pay Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        BillingState.orders_for_billing,
                                        billing_order_row,
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            (BillingState.orders_for_billing.length() == 0)
                            & ~BillingState.is_loading,
                            rx.el.div(
                                rx.icon(
                                    "receipt", class_name="h-12 w-12 text-gray-400 mb-4"
                                ),
                                rx.el.h3(
                                    "No Orders Found for Billing",
                                    class_name="text-lg font-semibold text-gray-700",
                                ),
                                rx.el.p(
                                    "All orders will appear here for invoicing and payment tracking.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="hidden md:block overflow-x-auto border border-gray-200 rounded-xl",
                    ),
                    class_name="md:bg-white md:p-2 md:p-6 rounded-xl shadow-sm",
                ),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )