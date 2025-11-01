import reflex as rx
from app.states.profit_state import ProfitAnalysisState
from app.components.sidebar import sidebar, mobile_header


def profit_analysis_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Profit Analysis",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.cond(
                    ProfitAnalysisState.is_loading,
                    rx.el.div(rx.spinner(), "Loading analysis..."),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Total Revenue", class_name="text-sm"),
                                rx.el.p(
                                    f"₹{ProfitAnalysisState.total_revenue.to_string()}",
                                    class_name="text-2xl font-bold",
                                ),
                                class_name="p-4 bg-green-100 rounded-lg",
                            ),
                            rx.el.div(
                                rx.el.p("Total Costs", class_name="text-sm"),
                                rx.el.p(
                                    f"₹{ProfitAnalysisState.total_costs.to_string()}",
                                    class_name="text-2xl font-bold",
                                ),
                                class_name="p-4 bg-red-100 rounded-lg",
                            ),
                            rx.el.div(
                                rx.el.p("Net Profit", class_name="text-sm"),
                                rx.el.p(
                                    f"₹{ProfitAnalysisState.net_profit.to_string()}",
                                    class_name="text-2xl font-bold",
                                ),
                                class_name="p-4 bg-blue-100 rounded-lg",
                            ),
                            rx.el.div(
                                rx.el.p("Profit Margin", class_name="text-sm"),
                                rx.el.p(
                                    f"{ProfitAnalysisState.profit_margin.to_string()}%",
                                    class_name="text-2xl font-bold",
                                ),
                                class_name="p-4 bg-purple-100 rounded-lg",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Monthly Profit Trend",
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.recharts.line_chart(
                                rx.recharts.x_axis(data_key="month"),
                                rx.recharts.y_axis(),
                                rx.recharts.line(data_key="profit", stroke="#82ca9d"),
                                data=ProfitAnalysisState.monthly_profit_trend,
                                width="100%",
                                height=300,
                            ),
                            class_name="p-6 bg-white rounded-xl shadow-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "Profit by Cloth Type",
                                    class_name="text-xl font-semibold mb-4",
                                ),
                                rx.recharts.bar_chart(
                                    rx.recharts.x_axis(data_key="cloth_type"),
                                    rx.recharts.y_axis(),
                                    rx.recharts.bar(
                                        data_key="total_profit", fill="#8884d8"
                                    ),
                                    data=ProfitAnalysisState.profit_by_cloth_type,
                                    width="100%",
                                    height=300,
                                ),
                                class_name="p-6 bg-white rounded-xl shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.h2(
                                    "Top Profitable Customers",
                                    class_name="text-xl font-semibold mb-4",
                                ),
                                rx.el.div(
                                    rx.foreach(
                                        ProfitAnalysisState.top_profitable_customers,
                                        lambda c: rx.el.div(
                                            rx.el.p(c["customer_name"]),
                                            rx.el.p(
                                                f"₹{c['total_profit']}",
                                                class_name="font-semibold",
                                            ),
                                            class_name="flex justify-between p-2 border-b",
                                        ),
                                    )
                                ),
                                class_name="p-6 bg-white rounded-xl shadow-sm",
                            ),
                            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
                        ),
                    ),
                ),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )