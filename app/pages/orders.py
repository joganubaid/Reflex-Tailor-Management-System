import reflex as rx
from app.state import OrderState
from app.states.photo_state import PhotoState
import reflex as rx
from app.state import OrderState
from app.states.photo_state import PhotoState
from app.components.sidebar import sidebar
from app.components.order_form import order_form
from app.components.photo_uploader import photo_upload_dialog

STATUS_COLORS = {
    "pending": "bg-red-100 text-red-800",
    "cutting": "bg-orange-100 text-orange-800",
    "stitching": "bg-yellow-100 text-yellow-800",
    "finishing": "bg-blue-100 text-blue-800",
    "ready": "bg-green-100 text-green-800",
    "delivered": "bg-gray-100 text-gray-800",
}
PRIORITY_COLORS = {
    "urgent": "border-red-500 bg-red-50",
    "high": "border-orange-500 bg-orange-50",
    "standard": "border-transparent",
}


def status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status.lower(),
            ("pending", STATUS_COLORS["pending"] + base_classes),
            ("cutting", STATUS_COLORS["cutting"] + base_classes),
            ("stitching", STATUS_COLORS["stitching"] + base_classes),
            ("finishing", STATUS_COLORS["finishing"] + base_classes),
            ("ready", STATUS_COLORS["ready"] + base_classes),
            ("delivered", STATUS_COLORS["delivered"] + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def order_row(order: rx.Var[dict]) -> rx.Component:
    row_class = rx.match(
        order["priority"].to_string(),
        ("urgent", f"border-l-4 {PRIORITY_COLORS['urgent']}"),
        ("high", f"border-l-4 {PRIORITY_COLORS['high']}"),
        PRIORITY_COLORS["standard"],
    )
    return rx.el.tr(
        rx.el.td(
            order["customer_name"], class_name="px-6 py-4 font-medium text-gray-900"
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    order["order_date"],
                    order["order_date"].to_string().split("T")[0],
                    "N/A",
                )
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    order["delivery_date"],
                    order["delivery_date"].to_string().split("T")[0],
                    "N/A",
                )
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(status_badge(order["status"]), class_name="px-6 py-4"),
        rx.el.td(
            f"₹{order['total_amount'].to_string()}",
            class_name="px-6 py-4 text-gray-800 font-medium",
        ),
        rx.el.td(
            f"₹{order['balance_payment'].to_string()}",
            class_name="px-6 py-4 text-red-600 font-medium",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("camera", class_name="h-4 w-4"),
                    on_click=lambda: PhotoState.open_photo_uploader(
                        "order_photo", order["order_id"]
                    ),
                    class_name="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("copy", class_name="h-4 w-4"),
                    on_click=lambda: OrderState.duplicate_order(order["order_id"]),
                    class_name="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name=f"{row_class} border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def orders_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Order Management", class_name="text-3xl font-bold text-gray-800"
                ),
                rx.el.p(
                    "Track and manage all customer orders.",
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
                        placeholder="Search by customer...",
                        on_change=OrderState.set_search_query,
                        class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                    ),
                    class_name="relative",
                ),
                rx.el.select(
                    rx.el.option("All Priorities", value="all"),
                    rx.el.option("Urgent", value="urgent"),
                    rx.el.option("High", value="high"),
                    rx.el.option("Standard", value="standard"),
                    value=OrderState.priority_filter,
                    on_change=OrderState.set_priority_filter,
                    class_name="px-4 py-2 border rounded-lg bg-white focus:ring-purple-500",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("layout-grid", class_name="mr-2 h-5 w-5"),
                        "Templates",
                        on_click=OrderState.open_template_manager,
                        class_name="flex items-center bg-gray-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-gray-700 transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Add Order",
                        on_click=OrderState.toggle_order_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Customer",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Order Date",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Delivery Date",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Total",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Balance",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    scope="col",
                                    class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                            )
                        ),
                        rx.el.tbody(rx.foreach(OrderState.filtered_orders, order_row)),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    rx.cond(
                        OrderState.filtered_orders.length() == 0,
                        rx.el.div(
                            rx.icon(
                                "shopping-cart",
                                class_name="h-12 w-12 text-gray-400 mb-4",
                            ),
                            rx.el.h3(
                                "No Orders Yet",
                                class_name="text-lg font-semibold text-gray-700",
                            ),
                            rx.el.p(
                                "Create your first order to get started.",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="text-center py-16",
                        ),
                        None,
                    ),
                    class_name="overflow-hidden border border-gray-200 rounded-xl",
                ),
                class_name="bg-white p-6 rounded-xl shadow-sm",
            ),
            order_form(),
            photo_upload_dialog(),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )