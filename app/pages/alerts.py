import reflex as rx
from app.states.alert_state import AlertState
from app.components.sidebar import sidebar, mobile_header


def alerts_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Alerts & Automation",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Configure smart alerts and view system notifications.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("settings", class_name="h-16 w-16 text-gray-400 mb-6"),
                        rx.el.h2(
                            "Smart Alerts Coming Soon",
                            class_name="text-2xl font-bold text-gray-700 mb-4",
                        ),
                        rx.el.p(
                            "The smart alerts system requires additional database tables:",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.ul(
                            rx.el.li("• alert_settings", class_name="text-gray-600"),
                            rx.el.li("• alert_history", class_name="text-gray-600"),
                            rx.el.li(
                                "• automation_workflows", class_name="text-gray-600"
                            ),
                            class_name="mb-6 space-y-2",
                        ),
                        rx.el.p(
                            "Once these tables are added to your database schema, you'll get:",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon("bell", class_name="h-8 w-8 text-yellow-500"),
                                rx.el.div(
                                    rx.el.h4(
                                        "Low Stock Alerts",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Get notified when materials run low",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-yellow-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.icon("clock", class_name="h-8 w-8 text-orange-500"),
                                rx.el.div(
                                    rx.el.h4(
                                        "Payment Reminders",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Auto-remind customers about due payments",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-orange-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.icon("truck", class_name="h-8 w-8 text-blue-500"),
                                rx.el.div(
                                    rx.el.h4(
                                        "Delivery Alerts",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Track order deadlines and delivery dates",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-blue-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "smartphone", class_name="h-8 w-8 text-green-500"
                                ),
                                rx.el.div(
                                    rx.el.h4(
                                        "SMS & Email Notifications",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Choose how and when to receive alerts",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-green-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.icon("zap", class_name="h-8 w-8 text-purple-500"),
                                rx.el.div(
                                    rx.el.h4(
                                        "Automated Workflows",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Set up automated actions based on triggers",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-purple-50 rounded-lg",
                            ),
                            class_name="grid gap-4 mb-8",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "🔔 Current: You can still manually track orders and payments using the existing sections.",
                                class_name="text-sm text-indigo-700 bg-indigo-50 p-3 rounded-lg",
                            )
                        ),
                        class_name="text-center max-w-2xl mx-auto",
                    ),
                    class_name="bg-white p-8 rounded-xl shadow-sm",
                ),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )