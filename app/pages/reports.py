import reflex as rx
from app.states.report_state import ReportState
from app.components.sidebar import sidebar, mobile_header


def reports_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Advanced Reports",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.input(
                        name="report_start_date",
                        type="date",
                        default_value=ReportState.report_start_date,
                        class_name="p-2 border rounded-lg",
                    ),
                    rx.el.input(
                        name="report_end_date",
                        type="date",
                        default_value=ReportState.report_end_date,
                        class_name="p-2 border rounded-lg",
                    ),
                    rx.el.button(
                        "Generate Reports",
                        on_click=ReportState.load_all_reports,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg",
                    ),
                    class_name="flex items-center gap-4 mb-8",
                ),
                rx.cond(
                    ReportState.is_loading,
                    rx.el.div(rx.spinner(), "Generating reports..."),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Customer Lifetime Value (CLV) Analysis",
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    f"Avg. CLV: ₹{ReportState.avg_customer_lifetime_value.to_string()}"
                                ),
                                rx.el.p(
                                    f"Total Customers: {ReportState.total_customer_count}"
                                ),
                                class_name="flex gap-8 mb-4",
                            ),
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th("Customer"),
                                        rx.el.th("Total Spent"),
                                        rx.el.th("Total Orders"),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ReportState.top_clv_customers,
                                        lambda c: rx.el.tr(
                                            rx.el.td(c["name"]),
                                            rx.el.td(f"₹{c['total_spent']}"),
                                            rx.el.td(c["total_orders"]),
                                        ),
                                    )
                                ),
                            ),
                            class_name="p-6 bg-white rounded-xl shadow-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Material Wastage Analysis",
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.el.p(
                                f"Total Wastage Cost: ₹{ReportState.total_wastage_cost.to_string()}"
                            ),
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th("Material"),
                                        rx.el.th("Wastage %"),
                                        rx.el.th("Wastage Cost"),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ReportState.wastage_by_material,
                                        lambda w: rx.el.tr(
                                            rx.el.td(w["material_name"]),
                                            rx.el.td(
                                                f"{w['wastage_percentage']}%",
                                                class_name="text-red-500",
                                            ),
                                            rx.el.td(f"₹{w['wastage_cost']}"),
                                        ),
                                    )
                                ),
                            ),
                            class_name="p-6 bg-white rounded-xl shadow-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "GST Report", class_name="text-xl font-semibold mb-4"
                            ),
                            rx.el.div(
                                rx.el.p(
                                    f"Taxable Sales: ₹{ReportState.taxable_sales.to_string()}"
                                ),
                                rx.el.p(
                                    f"Total GST Collected: ₹{ReportState.total_gst_collected.to_string()}"
                                ),
                                class_name="flex gap-8 mb-4",
                            ),
                            class_name="p-6 bg-white rounded-xl shadow-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Seasonal Trends",
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.recharts.line_chart(
                                rx.recharts.x_axis(data_key="month"),
                                rx.recharts.y_axis(),
                                rx.recharts.line(data_key="revenue", stroke="#8884d8"),
                                rx.recharts.line(
                                    data_key="order_count", stroke="#82ca9d"
                                ),
                                data=ReportState.monthly_order_trends,
                                width="100%",
                                height=300,
                            ),
                            class_name="p-6 bg-white rounded-xl shadow-sm",
                        ),
                    ),
                ),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )