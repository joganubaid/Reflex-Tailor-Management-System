import reflex as rx
from app.components.sidebar import sidebar, mobile_header


def install_instructions_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "smartphone",
                            class_name="h-12 w-12 text-purple-600 mx-auto mb-4",
                        ),
                        rx.el.h1(
                            "Install TailorFlow App",
                            class_name="text-3xl font-bold text-gray-800 text-center mb-2",
                        ),
                        rx.el.p(
                            "Get native app experience with offline support",
                            class_name="text-gray-600 text-center mb-8",
                        ),
                        class_name="text-center mb-12",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("smartphone", class_name="h-8 w-8 text-green-600"),
                            rx.el.h2(
                                "Android (Chrome/Edge)",
                                class_name="text-xl font-bold text-gray-800 ml-3",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.ol(
                            rx.el.li(
                                rx.el.span("📱 ", class_name="mr-2"),
                                "Visit this website on your Android phone",
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("🔔 ", class_name="mr-2"),
                                'Look for "Install TailorFlow" popup or tap address bar',
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("⬇️ ", class_name="mr-2"),
                                'Tap "Install" or "Add to Home Screen"',
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("✅ ", class_name="mr-2"),
                                "App icon appears on your home screen!",
                                class_name="mb-3 flex items-center",
                            ),
                            class_name="list-none space-y-2",
                        ),
                        class_name="bg-green-50 border border-green-200 rounded-lg p-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("apple", class_name="h-8 w-8 text-gray-800"),
                            rx.el.h2(
                                "iPhone/iPad (Safari)",
                                class_name="text-xl font-bold text-gray-800 ml-3",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.ol(
                            rx.el.li(
                                rx.el.span("🧭 ", class_name="mr-2"),
                                "Open this website in Safari browser",
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("📤 ", class_name="mr-2"),
                                "Tap the Share button (square with arrow up)",
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("➕ ", class_name="mr-2"),
                                'Scroll down and tap "Add to Home Screen"',
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("✅ ", class_name="mr-2"),
                                'Tap "Add" to install the app',
                                class_name="mb-3 flex items-center",
                            ),
                            class_name="list-none space-y-2",
                        ),
                        class_name="bg-gray-50 border border-gray-200 rounded-lg p-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("monitor", class_name="h-8 w-8 text-blue-600"),
                            rx.el.h2(
                                "Desktop (Chrome/Edge)",
                                class_name="text-xl font-bold text-gray-800 ml-3",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.ol(
                            rx.el.li(
                                rx.el.span("💻 ", class_name="mr-2"),
                                "Look for install icon in address bar",
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("🖱️ ", class_name="mr-2"),
                                'Click the icon and select "Install"',
                                class_name="mb-3 flex items-center",
                            ),
                            rx.el.li(
                                rx.el.span("🪟 ", class_name="mr-2"),
                                "App opens in its own window",
                                class_name="mb-3 flex items-center",
                            ),
                            class_name="list-none space-y-2",
                        ),
                        class_name="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Why Install?",
                            class_name="text-xl font-bold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "zap", class_name="h-6 w-6 text-yellow-500 mb-2"
                                ),
                                rx.el.h3(
                                    "Faster Access", class_name="font-semibold mb-1"
                                ),
                                rx.el.p(
                                    "Launch instantly from home screen",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="text-center",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "wifi-off",
                                    class_name="h-6 w-6 text-orange-500 mb-2",
                                ),
                                rx.el.h3(
                                    "Works Offline", class_name="font-semibold mb-1"
                                ),
                                rx.el.p(
                                    "Access cached pages without internet",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="text-center",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "maximize", class_name="h-6 w-6 text-green-500 mb-2"
                                ),
                                rx.el.h3(
                                    "Full Screen", class_name="font-semibold mb-1"
                                ),
                                rx.el.p(
                                    "No browser UI, like a native app",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="text-center",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                        ),
                        class_name="bg-white border border-gray-200 rounded-lg p-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.icon("arrow-left", class_name="h-5 w-5 mr-2"),
                            "Back to TailorFlow",
                            href="/dashboard",
                            class_name="inline-flex items-center bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                        ),
                        class_name="text-center",
                    ),
                ),
                class_name="flex-1 p-4 md:p-8 overflow-auto max-w-4xl mx-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )