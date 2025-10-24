import reflex as rx
from app.components.sidebar import sidebar


def report_card(title: str, description: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-8 w-8 text-purple-600"),
            rx.el.h3(title, class_name="text-lg font-semibold text-gray-800"),
            class_name="flex items-center gap-4",
        ),
        rx.el.p(description, class_name="text-sm text-gray-500 mt-2"),
        rx.el.div(
            rx.el.select(
                rx.el.option("Last 7 Days", value="7d"),
                rx.el.option("Last 30 Days", value="30d"),
                rx.el.option("This Month", value="month"),
                rx.el.option("Last 3 Months", value="3m"),
                class_name="px-3 py-1.5 border rounded-md text-sm bg-white",
            ),
            rx.el.button(
                rx.icon("download", class_name="h-4 w-4 mr-2"),
                "Export",
                class_name="flex items-center text-sm font-medium text-purple-600 border border-purple-200 px-3 py-1.5 rounded-md hover:bg-purple-50",
            ),
            class_name="flex items-center justify-between mt-4 pt-4 border-t",
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-lg transition-shadow duration-200",
    )


def reports_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Reports Center", class_name="text-3xl font-bold text-gray-800"
                ),
                rx.el.p(
                    "Generate and export detailed reports for your business.",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                report_card(
                    "Sales Report",
                    "Track revenue, orders, and payment statuses over time.",
                    "trending-up",
                ),
                report_card(
                    "Customer Report",
                    "Analyze top customers, order frequency, and lifetime value.",
                    "users",
                ),
                report_card(
                    "Inventory Report",
                    "Monitor stock levels, material usage, and low-stock items.",
                    "package",
                ),
                report_card(
                    "Worker Productivity Report",
                    "View orders completed and efficiency metrics for each worker.",
                    "contact",
                ),
                report_card(
                    "Payment & Expense Report",
                    "Consolidated view of all incoming payments and outgoing expenses.",
                    "banknote",
                ),
                report_card(
                    "GST & Tax Report",
                    "Generate reports for tax filing with GST calculations.",
                    "file-text",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )