import reflex as rx


def offline_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("wifi-off", class_name="h-16 w-16 text-gray-400 mx-auto mb-6"),
            rx.el.h1(
                "You're Offline",
                class_name="text-2xl font-bold text-gray-800 text-center mb-4",
            ),
            rx.el.p(
                "It looks like you're not connected to the internet.",
                class_name="text-gray-600 text-center mb-2",
            ),
            rx.el.p(
                "Some content may be available from cache while you're offline.",
                class_name="text-gray-600 text-center mb-8",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-5 w-5 mr-2"),
                    "Try Again",
                    onclick="window.location.reload()",
                    class_name="bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors flex items-center mx-auto",
                ),
                class_name="text-center mb-8",
            ),
            rx.el.div(
                rx.el.h2("Available Offline:", class_name="font-semibold mb-3"),
                rx.el.ul(
                    rx.el.li(
                        rx.el.a(
                            "Dashboard",
                            href="/dashboard",
                            class_name="text-purple-600 hover:underline",
                        ),
                        class_name="mb-2",
                    ),
                    rx.el.li(
                        rx.el.a(
                            "Customers",
                            href="/customers",
                            class_name="text-purple-600 hover:underline",
                        ),
                        class_name="mb-2",
                    ),
                    rx.el.li(
                        rx.el.a(
                            "Orders",
                            href="/orders",
                            class_name="text-purple-600 hover:underline",
                        ),
                        class_name="mb-2",
                    ),
                    rx.el.li(
                        rx.el.a(
                            "Inventory",
                            href="/inventory",
                            class_name="text-purple-600 hover:underline",
                        ),
                        class_name="mb-2",
                    ),
                    class_name="list-none space-y-1",
                ),
                class_name="bg-gray-50 border border-gray-200 rounded-lg p-6",
            ),
            class_name="max-w-md mx-auto mt-16",
        ),
        class_name="min-h-screen bg-white p-8 flex items-center justify-center",
    )