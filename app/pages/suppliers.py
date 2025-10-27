import reflex as rx
from app.states.supplier_state import SupplierState
from app.components.sidebar import sidebar, mobile_header
from app.components.supplier_form import supplier_form, delete_supplier_dialog


def star_rating(rating: rx.Var[float]) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            rx.Var.range(5),
            lambda i: rx.icon(
                "star",
                class_name=rx.cond(
                    i < rating,
                    "h-4 w-4 text-yellow-400 fill-yellow-400",
                    "h-4 w-4 text-gray-300",
                ),
            ),
        ),
        class_name="flex items-center",
    )


def supplier_row(supplier: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(supplier["name"], class_name="px-6 py-4 font-medium text-gray-900"),
        rx.el.td(
            rx.el.div(
                rx.icon("phone", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(supplier["contact"]),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("mail", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(supplier["email"]),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(star_rating(supplier["rating"].to(float)), class_name="px-6 py-4"),
        rx.el.td(
            supplier["materials_count"].to_string(),
            class_name="px-6 py-4 text-center text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: SupplierState.start_editing(supplier),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: SupplierState.show_delete_confirmation(supplier),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def suppliers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Supplier Management",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Manage all your material suppliers.",
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
                            placeholder="Search by name or contact...",
                            type="search",
                            on_change=SupplierState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            default_value=SupplierState.search_query,
                        ),
                        class_name="relative",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Add Supplier",
                        on_click=SupplierState.toggle_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
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
                                            "Contact",
                                            scope="col",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Email",
                                            scope="col",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Rating",
                                            scope="col",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Materials",
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
                                        SupplierState.filtered_suppliers, supplier_row
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            SupplierState.filtered_suppliers.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "truck", class_name="h-12 w-12 text-gray-400 mb-4"
                                ),
                                rx.el.h3(
                                    "No Suppliers Found",
                                    class_name="text-lg font-semibold text-gray-700",
                                ),
                                rx.el.p(
                                    "Add your first supplier to get started.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm",
                ),
                supplier_form(),
                delete_supplier_dialog(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )