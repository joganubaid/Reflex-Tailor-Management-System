import reflex as rx
from app.states.profit_state import ProfitAnalysisState
from app.components.sidebar import sidebar

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#E8E8E8",
        "border_radius": "0.75rem",
        "font_family": "'Lato', sans-serif",
    }
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


def chart_container(
    title: str, chart: rx.Component, empty_message: str, data: rx.Var
) -> rx.Component:
    return rx.el.div(
        rx.el.h2(title, class_name="text-xl font-semibold text-gray-700 mb-4"),
        rx.cond(
            data.length() > 0,
            chart,
            rx.el.div(
                rx.el.p(empty_message, class_name="text-gray-500 text-center"),
                class_name="flex items-center justify-center h-64",
            ),
        ),
        class_name="p-6 bg-white rounded-xl shadow-sm",
    )


def profit_analysis_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1(
                "Profit & Loss Analysis",
                class_name="text-3xl font-bold text-gray-800 mb-6",
            ),
            rx.el.div(
                metric_card(
                    "trending-up",
                    "Total Revenue",
                    f"₹{ProfitAnalysisState.total_revenue.to_string()}",
                    "bg-blue-500",
                ),
                metric_card(
                    "arrow_down",
                    "Total Costs",
                    f"₹{ProfitAnalysisState.total_costs.to_string()}",
                    "bg-orange-500",
                ),
                metric_card(
                    "indian-rupee",
                    "Net Profit",
                    f"₹{ProfitAnalysisState.net_profit.to_string()}",
                    "bg-green-500",
                ),
                metric_card(
                    "percent",
                    "Profit Margin",
                    f"{ProfitAnalysisState.profit_margin.to_string()}%",
                    "bg-purple-500",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                chart_container(
                    "Monthly Profit Trend",
                    rx.el.div(
                        rx.recharts.area_chart(
                            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                            rx.recharts.x_axis(data_key="month"),
                            rx.recharts.y_axis(),
                            rx.recharts.area(
                                type_="monotone",
                                data_key="revenue",
                                stroke="#3b82f6",
                                fill="#3b82f6",
                                name="Revenue",
                                fill_opacity=0.3,
                            ),
                            rx.recharts.area(
                                type_="monotone",
                                data_key="costs",
                                stroke="#f97316",
                                fill="#f97316",
                                name="Costs",
                                fill_opacity=0.3,
                            ),
                            rx.recharts.area(
                                type_="monotone",
                                data_key="profit",
                                stroke="#22c55e",
                                fill="#22c55e",
                                name="Profit",
                                fill_opacity=0.3,
                            ),
                            data=ProfitAnalysisState.monthly_profit_trend,
                            height=250,
                            width="100%",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(class_name="w-3 h-3 bg-[#3b82f6] rounded-sm"),
                                "Revenue",
                                class_name="flex items-center gap-2 text-sm text-gray-600",
                            ),
                            rx.el.div(
                                rx.el.div(class_name="w-3 h-3 bg-[#f97316] rounded-sm"),
                                "Costs",
                                class_name="flex items-center gap-2 text-sm text-gray-600",
                            ),
                            rx.el.div(
                                rx.el.div(class_name="w-3 h-3 bg-[#22c55e] rounded-sm"),
                                "Profit",
                                class_name="flex items-center gap-2 text-sm text-gray-600",
                            ),
                            class_name="flex justify-center items-center gap-4 mt-4",
                        ),
                    ),
                    "No sales data available for this period.",
                    ProfitAnalysisState.monthly_profit_trend,
                ),
                chart_container(
                    "Profit by Cloth Type",
                    rx.recharts.pie_chart(
                        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                        rx.recharts.pie(
                            data=ProfitAnalysisState.profit_by_cloth_type,
                            data_key="total_profit",
                            name_key="cloth_type",
                            cx="50%",
                            cy="50%",
                            outer_radius=80,
                            fill="#8884d8",
                            label=True,
                            stroke="#fff",
                            stroke_width=2,
                        ),
                        height=300,
                        width="100%",
                    ),
                    "No profit data available by cloth type.",
                    ProfitAnalysisState.profit_by_cloth_type,
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
            ),
            rx.el.div(
                chart_container(
                    "Top 5 Profitable Customers",
                    rx.recharts.bar_chart(
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                        rx.recharts.x_axis(data_key="customer_name"),
                        rx.recharts.y_axis(),
                        rx.recharts.bar(data_key="total_profit", fill="#8884d8"),
                        data=ProfitAnalysisState.top_profitable_customers,
                        layout="vertical",
                        height=300,
                        width="100%",
                    ),
                    "No data on profitable customers.",
                    ProfitAnalysisState.top_profitable_customers,
                ),
                chart_container(
                    "Profit by Worker",
                    rx.recharts.bar_chart(
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                        rx.recharts.x_axis(data_key="worker_name"),
                        rx.recharts.y_axis(),
                        rx.recharts.bar(data_key="total_profit", fill="#82ca9d"),
                        data=ProfitAnalysisState.profit_by_worker,
                        height=300,
                        width="100%",
                    ),
                    "No data on profit by worker.",
                    ProfitAnalysisState.profit_by_worker,
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
            ),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )