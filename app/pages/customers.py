import reflex as rx
from app.state import CustomerState
from app.components.sidebar import sidebar, mobile_header
from app.components.customer_form import customer_form, delete_confirmation_dialog


def customer_card(customer: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(customer["name"], class_name="font-bold text-lg text-gray-800"),
                rx.el.p(
                    f"{customer['total_orders']} orders",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: CustomerState.start_editing(customer),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: CustomerState.show_delete_confirmation(customer),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("phone", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(customer["phone_number"]),
                href=f"tel:{customer['phone_number']}",
                class_name="flex items-center text-purple-600 hover:underline",
            ),
            rx.el.a(
                rx.icon("mail", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(customer["email"]),
                href=f"mailto:{customer['email']}",
                class_name="flex items-center text-purple-600 hover:underline",
            ),
            class_name="flex flex-col sm:flex-row sm:gap-6 gap-2 mt-3 text-sm",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def customer_row(customer: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(customer["name"], class_name="px-6 py-4 font-medium text-gray-900"),
        rx.el.td(
            rx.el.div(
                rx.icon("phone", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(customer["phone_number"]),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("mail", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(customer["email"]),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(
            customer["total_orders"], class_name="px-6 py-4 text-center text-gray-600"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: CustomerState.start_editing(customer),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: CustomerState.show_delete_confirmation(customer),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def customers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Customer Management",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Manage all your customer profiles in one place.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search by name or phone...",
                            type="search",
                            on_change=CustomerState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            default_value=CustomerState.search_query,
                        ),
                        class_name="relative",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Add Customer",
                        on_click=CustomerState.toggle_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                    ),
                    class_name="flex flex-col md:flex-row justify-between items-center mb-6 gap-4 md:gap-0",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(CustomerState.filtered_customers, customer_card),
                            class_name="grid grid-cols-1 gap-4 md:hidden",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Name",
                                                scope="col",
                                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Phone",
                                                scope="col",
                                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Email",
                                                scope="col",
                                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Orders",
                                                scope="col",
                                                class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Actions",
                                                scope="col",
                                                class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                            ),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            CustomerState.filtered_customers,
                                            customer_row,
                                        )
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            class_name="hidden md:block rounded-lg border border-gray-200 shadow-sm",
                        ),
                        rx.cond(
                            CustomerState.filtered_customers.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "user-x", class_name="h-12 w-12 text-gray-400 mb-4"
                                ),
                                rx.el.h3(
                                    "No Customers Found",
                                    class_name="text-lg font-semibold text-gray-700",
                                ),
                                rx.el.p(
                                    "Add your first customer to get started.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                    ),
                    class_name="md:bg-white md:p-6 md:rounded-xl md:shadow-sm",
                ),
                customer_form(),
                delete_confirmation_dialog(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )