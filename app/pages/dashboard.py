import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.sidebar import sidebar

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#E8E8E8",
        "border_radius": "0.75rem",
        "box_shadow": "0px 2px 6px 0px rgba(28, 32, 36, 0.02)",
        "font_family": "'Lato', sans-serif",
        "font_size": "0.875rem",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {},
    "label_style": {"color": "#374151"},
}


def metric_card(
    icon: str, title: str, value: rx.Var, icon_bg_color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-white"),
            class_name=f"p-3 rounded-full {icon_bg_color}",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1("Dashboard", class_name="text-3xl font-bold text-gray-800 mb-6"),
            rx.el.div(
                metric_card(
                    "indian-rupee",
                    "Today's Revenue",
                    f"₹{DashboardState.today_revenue.to_string()}",
                    "bg-green-500",
                ),
                metric_card(
                    "clock",
                    "Pending Orders",
                    DashboardState.pending_orders_count.to_string(),
                    "bg-orange-500",
                ),
                metric_card(
                    "check_check",
                    "Ready for Delivery",
                    DashboardState.ready_orders_count.to_string(),
                    "bg-blue-500",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Monthly Sales",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.recharts.area_chart(
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                        rx.recharts.x_axis(data_key="day"),
                        rx.recharts.y_axis(),
                        rx.recharts.area(
                            type_="monotone",
                            data_key="sales",
                            stroke="#8884d8",
                            fill="#8884d8",
                            fill_opacity=0.3,
                        ),
                        data=DashboardState.monthly_sales_data,
                        height=300,
                        width="100%",
                        class_name="[&_.recharts-cartesian-axis-tick-value]:fill-gray-500 [&_.recharts-cartesian-axis-line]:stroke-gray-300",
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-sm",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Low Stock Items",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.low_stock_items,
                            lambda item: rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        item["material_name"],
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        item["material_type"].capitalize(),
                                        class_name="text-sm text-gray-500",
                                    ),
                                ),
                                rx.el.p(
                                    f"{item['quantity_in_stock']} {item['unit']}",
                                    class_name="text-red-600 font-bold",
                                ),
                                class_name="flex justify-between items-center py-2 border-b",
                            ),
                        ),
                        rx.cond(
                            DashboardState.low_stock_items.length() == 0,
                            rx.el.p(
                                "All items are well-stocked.",
                                class_name="text-gray-500 text-center py-8",
                            ),
                            None,
                        ),
                        class_name="space-y-2",
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-sm",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Top Customers",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.foreach(
                        DashboardState.top_customers,
                        lambda customer: rx.el.div(
                            rx.el.p(
                                customer["name"], class_name="font-medium text-gray-800"
                            ),
                            rx.el.p(
                                f"₹{customer['total_spent'].to_string()}",
                                class_name="text-green-600 font-semibold",
                            ),
                            class_name="flex justify-between items-center py-2 border-b",
                        ),
                    ),
                    rx.cond(
                        DashboardState.top_customers.length() == 0,
                        rx.el.p(
                            "No customer data available.",
                            class_name="text-gray-500 text-center py-8",
                        ),
                        None,
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-sm",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Recent Activity",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.foreach(
                        DashboardState.recent_transactions,
                        lambda trx: rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    f"Order #{trx['order_id']}",
                                    class_name="font-medium text-gray-800",
                                ),
                                rx.el.p(
                                    f"₹{trx['total_amount'].to_string()}",
                                    class_name="text-sm text-gray-600",
                                ),
                            ),
                            rx.el.p(
                                trx["status"].capitalize(),
                                class_name="text-sm text-purple-600 font-semibold",
                            ),
                            class_name="flex justify-between items-center py-2 border-b",
                        ),
                    ),
                    rx.cond(
                        DashboardState.recent_transactions.length() == 0,
                        rx.el.p(
                            "No recent activity.",
                            class_name="text-gray-500 text-center py-8",
                        ),
                        None,
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-sm",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-8",
            ),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )