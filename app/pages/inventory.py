import reflex as rx
from app.state import MaterialState
from app.components.sidebar import sidebar, mobile_header
from app.components.material_form import material_form, delete_material_dialog


def material_card(material: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(material["material_name"], class_name="font-bold text-gray-800"),
            rx.el.span(
                material["material_type"].capitalize(),
                class_name="px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-700",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.p("In Stock:", class_name="text-sm text-gray-500"),
            rx.el.p(
                f"{material['quantity_in_stock']} {material['unit']}",
                class_name="font-semibold",
            ),
            class_name="flex justify-between mt-2",
        ),
        rx.el.div(
            rx.el.p("Reorder Level:", class_name="text-sm text-gray-500"),
            rx.el.p(
                f"{material['reorder_level']} {material['unit']}",
                class_name="font-semibold",
            ),
            class_name="flex justify-between mt-1",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def inventory_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Inventory Management",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search materials...",
                        on_change=MaterialState.set_search_query,
                        class_name="w-full md:w-72 p-2 border rounded-lg",
                    ),
                    rx.el.button(
                        "Add Material",
                        on_click=MaterialState.toggle_form,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    MaterialState.is_loading,
                    rx.el.p("Loading materials..."),
                    rx.el.div(
                        rx.foreach(MaterialState.filtered_materials, material_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
                    ),
                ),
                material_form(),
                delete_material_dialog(),
                class_name="p-4 md:p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )