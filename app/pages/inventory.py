import reflex as rx
from app.state import MaterialState
from app.components.sidebar import sidebar, mobile_header
from app.components.material_form import material_form, delete_material_dialog


def stock_status_badge(material: rx.Var[dict]) -> rx.Component:
    is_low = material["quantity_in_stock"] <= material["reorder_level"]
    is_out = material["quantity_in_stock"] == 0
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        rx.cond(is_out, "Out of Stock", rx.cond(is_low, "Low Stock", "In Stock")),
        class_name=rx.cond(
            is_out,
            "bg-red-100 text-red-800" + base_classes,
            rx.cond(
                is_low,
                "bg-yellow-100 text-yellow-800" + base_classes,
                "bg-green-100 text-green-800" + base_classes,
            ),
        ),
    )


def material_card(material: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(material["material_name"], class_name="font-bold text-gray-800"),
            stock_status_badge(material),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Stock", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"{material['quantity_in_stock']} {material['unit']}",
                    class_name="font-semibold text-gray-700",
                ),
            ),
            rx.el.div(
                rx.el.p("Price", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"₹{material['unit_price']}",
                    class_name="font-semibold text-gray-700",
                ),
            ),
            rx.el.div(
                rx.el.p("Value", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"₹{(material['quantity_in_stock'] * material['unit_price']).to_string()}",
                    class_name="font-bold text-purple-600",
                ),
            ),
            class_name="grid grid-cols-3 gap-4 mt-3 pt-3 border-t",
        ),
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
            class_name="flex items-center gap-2 mt-2",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def material_row(material: rx.Var[dict]) -> rx.Component:
    is_low_stock = material["quantity_in_stock"] <= material["reorder_level"]
    row_class = rx.cond(is_low_stock, "bg-yellow-50", "bg-white")
    return rx.el.tr(
        rx.el.td(
            material["material_name"], class_name="px-6 py-4 font-medium text-gray-900"
        ),
        rx.el.td(
            material["material_type"].capitalize(), class_name="px-6 py-4 text-gray-600"
        ),
        rx.el.td(stock_status_badge(material), class_name="px-6 py-4"),
        rx.el.td(
            rx.el.span(
                material["quantity_in_stock"].to_string(),
                rx.el.span(f" {material['unit']}", class_name="text-gray-500 ml-1"),
            ),
            class_name="px-6 py-4 text-gray-800 text-center",
        ),
        rx.el.td(
            f"₹{material['unit_price'].to_string()}",
            class_name="px-6 py-4 text-gray-600 text-right",
        ),
        rx.el.td(
            f"₹{(material['quantity_in_stock'] * material['unit_price']).to_string()}",
            class_name="px-6 py-4 font-semibold text-gray-800 text-right",
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
                            placeholder="Search by material name...",
                            type="search",
                            on_change=MaterialState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            default_value=MaterialState.search_query,
                        ),
                        class_name="relative w-full md:w-auto",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("All Stock", value="all"),
                            rx.el.option("Low Stock", value="low"),
                            rx.el.option("Out of Stock", value="out"),
                            value=MaterialState.stock_filter,
                            on_change=MaterialState.set_stock_filter,
                            class_name="w-full px-4 py-2 border rounded-lg bg-white focus:ring-purple-500",
                        ),
                        rx.el.select(
                            rx.el.option("All Types", value="all"),
                            rx.el.option("Fabric", value="fabric"),
                            rx.el.option("Button", value="button"),
                            rx.el.option("Thread", value="thread"),
                            rx.el.option("Zipper", value="zipper"),
                            rx.el.option("Lining", value="lining"),
                            value=MaterialState.type_filter,
                            on_change=MaterialState.set_type_filter,
                            class_name="w-full px-4 py-2 border rounded-lg bg-white focus:ring-purple-500",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="md:mr-2 h-5 w-5"),
                            rx.el.span("Add Material", class_name="hidden md:inline"),
                            on_click=MaterialState.toggle_form,
                            class_name="flex items-center justify-center bg-purple-600 text-white p-2 md:px-4 md:py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                        ),
                        class_name="flex items-center gap-2 w-full md:w-auto",
                    ),
                    class_name="flex flex-col md:flex-row justify-between items-center mb-6 gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(MaterialState.filtered_materials, material_card),
                        class_name="grid grid-cols-1 gap-4 md:hidden",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Name",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Type",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Stock",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Unit Price",
                                            class_name="px-6 py-3 text-right text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Value",
                                            class_name="px-6 py-3 text-right text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Supplier",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
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
                            class_name="overflow-x-auto",
                        ),
                        class_name="hidden md:block border border-gray-200 rounded-xl",
                    ),
                    rx.cond(
                        MaterialState.filtered_materials.length() == 0,
                        rx.el.div(
                            rx.icon(
                                "package-x", class_name="h-12 w-12 text-gray-400 mb-4"
                            ),
                            rx.el.h3(
                                "No Materials Found",
                                class_name="text-lg font-semibold text-gray-700",
                            ),
                            rx.el.p(
                                "Add your first material or adjust your filters.",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="text-center py-16 bg-white rounded-xl shadow-sm",
                        ),
                        None,
                    ),
                    class_name="md:bg-white md:p-2 md:rounded-xl md:shadow-sm",
                ),
                material_form(),
                delete_material_dialog(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )