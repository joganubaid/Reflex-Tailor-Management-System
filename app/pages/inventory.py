import reflex as rx
from app.state import MaterialState
from app.components.sidebar import sidebar, mobile_header
from app.components.material_form import material_form, delete_material_dialog


def material_row(material: rx.Var[dict]) -> rx.Component:
    is_low_stock = material["quantity_in_stock"] <= material["reorder_level"]
    row_class = rx.cond(is_low_stock, "bg-red-50 border-l-4 border-red-400", "bg-white")
    return rx.el.tr(
        rx.el.td(
            material["material_name"], class_name="px-6 py-4 font-medium text-gray-900"
        ),
        rx.el.td(
            material["material_type"].capitalize(), class_name="px-6 py-4 text-gray-600"
        ),
        rx.el.td(
            rx.el.span(
                material["quantity_in_stock"].to_string(),
                rx.el.span(f" {material['unit']}", class_name="text-gray-500 ml-1"),
                class_name=rx.cond(
                    is_low_stock, "font-bold text-red-600", "text-gray-800"
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            f"\t20b9{material['unit_price'].to_string()}",
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(
            f"\t20b9{(material['quantity_in_stock'] * material['unit_price']).to_string()}",
            class_name="px-6 py-4 font-semibold text-gray-800",
        ),
        rx.el.td(material["supplier_name"], class_name="px-6 py-4 text-gray-600"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: MaterialState.start_editing(material),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: MaterialState.show_delete_confirmation(material),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name=f"{row_class} border-b hover:bg-gray-50/50 transition-colors duration-150",
    )


def inventory_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Inventory Management",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Track and manage all your materials and supplies.",
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
                            placeholder="Search by material name or type...",
                            on_change=MaterialState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            default_value=MaterialState.search_query,
                        ),
                        class_name="relative",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Total Inventory Value: ",
                                class_name="font-semibold text-gray-700",
                            ),
                            rx.el.span(
                                f"\t20b9{MaterialState.total_inventory_value.to_string()}",
                                class_name="font-bold text-purple-600",
                            ),
                            class_name="px-4 py-2 bg-purple-50 rounded-lg border border-purple-200",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="mr-2 h-5 w-5"),
                            "Add Material",
                            on_click=MaterialState.toggle_form,
                            class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    class_name="flex justify-between items-center mb-6",
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
                                        "Type",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Stock",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Unit Price",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Value",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Supplier",
                                        scope="col",
                                        class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
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
                                    MaterialState.filtered_materials, material_row
                                )
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        rx.cond(
                            MaterialState.filtered_materials.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "package-x",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "No Materials Found",
                                    class_name="text-lg font-semibold text-gray-700",
                                ),
                                rx.el.p(
                                    "Add your first material to get started.",
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
                material_form(),
                delete_material_dialog(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )