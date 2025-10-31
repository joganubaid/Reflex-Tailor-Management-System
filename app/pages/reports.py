import reflex as rx
from app.components.sidebar import sidebar, mobile_header
from app.states.report_state import ReportState

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


def clv_customer_row(customer: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(customer["name"], class_name="px-6 py-4 font-medium"),
        rx.el.td(customer["phone_number"], class_name="px-6 py-4"),
        rx.el.td(
            customer["total_orders"].to_string(), class_name="px-6 py-4 text-center"
        ),
        rx.el.td(
            f"₹{customer['total_spent'].to_string()}",
            class_name="px-6 py-4 font-bold text-green-600",
        ),
        rx.el.td(f"₹{customer['avg_order_value'].to_string()}", class_name="px-6 py-4"),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def wastage_row(material: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(material["material_name"], class_name="px-6 py-4 font-medium"),
        rx.el.td(material["material_type"].capitalize(), class_name="px-6 py-4"),
        rx.el.td(
            f"{material['total_wastage'].to_string()} {material['unit']}",
            class_name="px-6 py-4 text-red-600",
        ),
        rx.el.td(
            f"₹{material['wastage_cost'].to_string()}",
            class_name="px-6 py-4 font-semibold text-red-700",
        ),
        rx.el.td(
            f"{material['wastage_percentage'].to_string()}%", class_name="px-6 py-4"
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def reports_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Advanced Reports & Analytics",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Comprehensive business intelligence and insights.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    metric_card(
                        "users",
                        "Total Customers",
                        ReportState.total_customer_count.to_string(),
                        "bg-blue-500",
                    ),
                    metric_card(
                        "trending-up",
                        "Avg. Customer Lifetime Value",
                        f"₹{ReportState.avg_customer_lifetime_value.to_string()}",
                        "bg-green-500",
                    ),
                    metric_card(
                        "badge_alert",
                        "Total Wastage Cost",
                        f"₹{ReportState.total_wastage_cost.to_string()}",
                        "bg-red-500",
                    ),
                    metric_card(
                        "receipt",
                        "GST Collected (This Month)",
                        f"\u2009{ReportState.total_gst_collected.to_string()}",
                        "bg-purple-500",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Top 10 Customers by Lifetime Value",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Customer Name",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Phone",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Orders",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Total Spent",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Avg Order",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ReportState.top_clv_customers, clv_customer_row
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            (ReportState.top_clv_customers.length() == 0)
                            & ~ReportState.is_loading,
                            rx.el.div(
                                rx.icon(
                                    "users", class_name="h-12 w-12 text-gray-400 mb-4"
                                ),
                                rx.el.p(
                                    "No customer data available.",
                                    class_name="text-gray-500",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Material Wastage Analysis",
                            class_name="text-xl font-semibold text-gray-700",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Avg Wastage: ", class_name="text-sm text-gray-600"
                            ),
                            rx.el.span(
                                f"{ReportState.avg_wastage_percentage.to_string()}%",
                                class_name="text-lg font-bold text-red-600",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Material",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Type",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Total Wastage",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Cost",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Wastage %",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ReportState.wastage_by_material, wastage_row
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            (ReportState.wastage_by_material.length() == 0)
                            & ~ReportState.is_loading,
                            rx.el.div(
                                rx.icon(
                                    "package", class_name="h-12 w-12 text-gray-400 mb-4"
                                ),
                                rx.el.p(
                                    "No wastage data available.",
                                    class_name="text-gray-500",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm mb-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Monthly Order Trends (Past 12 Months)",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.cond(
                        ReportState.monthly_order_trends.length() > 0,
                        rx.recharts.area_chart(
                            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                            rx.recharts.x_axis(data_key="month"),
                            rx.recharts.y_axis(),
                            rx.recharts.area(
                                type_="monotone",
                                data_key="order_count",
                                stroke="#8884d8",
                                fill="#8884d8",
                                name="Orders",
                                fill_opacity=0.6,
                            ),
                            data=ReportState.monthly_order_trends,
                            height=300,
                            width="100%",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "No trend data available.",
                                class_name="text-gray-500 text-center",
                            ),
                            class_name="flex items-center justify-center h-64",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm mb-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "GST Summary (Current Month)",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Total Invoices", class_name="text-sm text-gray-500"
                            ),
                            rx.el.p(
                                ReportState.gst_summary["total_invoices"].to_string(),
                                class_name="text-2xl font-bold",
                            ),
                            class_name="p-4 bg-blue-50 rounded-lg",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Taxable Sales", class_name="text-sm text-gray-500"
                            ),
                            rx.el.p(
                                f"₹{ReportState.taxable_sales.to_string()}",
                                class_name="text-2xl font-bold text-green-600",
                            ),
                            class_name="p-4 bg-green-50 rounded-lg",
                        ),
                        rx.el.div(
                            rx.el.p("CGST", class_name="text-sm text-gray-500"),
                            rx.el.p(
                                f"₹{ReportState.gst_summary['cgst'].to_string()}",
                                class_name="text-2xl font-bold text-purple-600",
                            ),
                            class_name="p-4 bg-purple-50 rounded-lg",
                        ),
                        rx.el.div(
                            rx.el.p("SGST", class_name="text-sm text-gray-500"),
                            rx.el.p(
                                f"₹{ReportState.gst_summary['sgst'].to_string()}",
                                class_name="text-2xl font-bold text-purple-600",
                            ),
                            class_name="p-4 bg-purple-50 rounded-lg",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-4 gap-4",
                    ),
                    class_name="bg-white p-4 md:p-6 rounded-xl shadow-sm",
                ),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )