import reflex as rx
from app.states.supplier_state import SupplierState
from app.components.sidebar import sidebar, mobile_header
from app.components.supplier_form import supplier_form, delete_supplier_dialog


def supplier_card(supplier: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(supplier["name"], class_name="font-bold text-lg"),
            rx.el.p(
                f"Rating: {supplier['rating']}/5",
                class_name="text-sm font-semibold text-yellow-600",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(supplier["contact"], class_name="text-sm text-gray-600"),
        rx.el.p(
            f"{supplier['materials_count']} materials supplied",
            class_name="text-xs text-gray-500 mt-2",
        ),
        rx.el.div(
            rx.el.button(
                "Edit",
                on_click=lambda: SupplierState.start_editing(supplier),
                class_name="text-xs p-1",
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: SupplierState.show_delete_confirmation(supplier),
                class_name="text-xs p-1 text-red-600",
            ),
            class_name="flex justify-end gap-2 mt-2",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border",
    )


def suppliers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1("Supplier Management", class_name="text-3xl font-bold mb-6"),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search suppliers...",
                        on_change=SupplierState.set_search_query,
                        class_name="w-full md:w-72 p-2 border rounded-lg",
                    ),
                    rx.el.button(
                        "Add Supplier",
                        on_click=SupplierState.toggle_form,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    SupplierState.is_loading,
                    rx.el.p("Loading suppliers..."),
                    rx.el.div(
                        rx.foreach(SupplierState.filtered_suppliers, supplier_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                ),
                supplier_form(),
                delete_supplier_dialog(),
                class_name="p-4 md:p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50",
    )