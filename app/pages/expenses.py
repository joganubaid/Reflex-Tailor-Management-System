import reflex as rx
from app.states.expense_state import ExpenseState
from app.components.sidebar import sidebar, mobile_header


def expense_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.el.h2(
                    "Expense Tracking Coming Soon",
                    class_name="text-2xl font-bold text-gray-800 mb-4",
                ),
                rx.el.p(
                    "The expense tracking feature requires additional database tables that are not yet configured in your system.",
                    class_name="text-gray-600 mb-4",
                ),
                rx.el.p(
                    "Please contact your system administrator to add the required tables: expense_categories, expenses, and bank_accounts.",
                    class_name="text-gray-600 mb-6",
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        on_click=ExpenseState.toggle_form,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 font-semibold",
                    )
                ),
                class_name="p-8 bg-white rounded-xl shadow-lg w-[36rem]",
            )
        ),
        open=ExpenseState.show_form,
        on_open_change=ExpenseState.set_show_form,
    )


def expenses_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Expense Tracking",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Record and manage all your business expenses.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "construction", class_name="h-16 w-16 text-gray-400 mb-6"
                        ),
                        rx.el.h2(
                            "Feature Under Development",
                            class_name="text-2xl font-bold text-gray-700 mb-4",
                        ),
                        rx.el.p(
                            "The expense tracking feature requires additional database tables:",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.ul(
                            rx.el.li(
                                "• expense_categories", class_name="text-gray-600"
                            ),
                            rx.el.li("• expenses", class_name="text-gray-600"),
                            rx.el.li("• bank_accounts", class_name="text-gray-600"),
                            class_name="mb-6 space-y-2",
                        ),
                        rx.el.p(
                            "Once these tables are added to your database schema, you'll be able to:",
                            class_name="text-gray-600 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon("receipt", class_name="h-8 w-8 text-blue-500"),
                                rx.el.div(
                                    rx.el.h4(
                                        "Track All Expenses",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Record rent, utilities, salaries, materials, and more",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-blue-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "trending-up", class_name="h-8 w-8 text-green-500"
                                ),
                                rx.el.div(
                                    rx.el.h4(
                                        "Expense Analytics",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "View spending trends and category breakdowns",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-green-50 rounded-lg",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "calculator", class_name="h-8 w-8 text-purple-500"
                                ),
                                rx.el.div(
                                    rx.el.h4(
                                        "Profit Calculation",
                                        class_name="font-semibold text-gray-800",
                                    ),
                                    rx.el.p(
                                        "Automatic profit/loss calculation with revenue",
                                        class_name="text-sm text-gray-600",
                                    ),
                                ),
                                class_name="flex items-start gap-4 p-4 bg-purple-50 rounded-lg",
                            ),
                            class_name="grid gap-4 mb-8",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "💡 Tip: Use the existing Orders and Materials sections to track income and inventory costs for now.",
                                class_name="text-sm text-blue-700 bg-blue-50 p-3 rounded-lg",
                            )
                        ),
                        class_name="text-center max-w-2xl mx-auto",
                    ),
                    class_name="bg-white p-8 rounded-xl shadow-sm",
                ),
                expense_form(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )