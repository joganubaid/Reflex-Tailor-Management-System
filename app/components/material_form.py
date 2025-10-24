import reflex as rx
from app.state import MaterialState


def _form_label(text: str) -> rx.Component:
    return rx.el.label(
        text, class_name="block text-sm font-semibold text-gray-700 mb-2"
    )


def _form_input(**props) -> rx.Component:
    return rx.el.input(
        **props,
        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
    )


def _form_select(*children, **props) -> rx.Component:
    return rx.el.select(
        *children,
        **props,
        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
    )


def material_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(
                        MaterialState.is_editing, "Edit Material", "Add New Material"
                    ),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Material Name"),
                        _form_input(
                            name="material_name",
                            default_value=MaterialState.material_name,
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Material Type"),
                        _form_select(
                            rx.el.option("Fabric", value="fabric"),
                            rx.el.option("Button", value="button"),
                            rx.el.option("Thread", value="thread"),
                            rx.el.option("Zipper", value="zipper"),
                            rx.el.option("Lining", value="lining"),
                            name="material_type",
                            value=MaterialState.material_type,
                            on_change=MaterialState.set_material_type,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Quantity in Stock"),
                        _form_input(
                            name="quantity_in_stock",
                            type="number",
                            default_value=MaterialState.quantity_in_stock.to_string(),
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Unit"),
                        _form_select(
                            rx.el.option("Meter", value="meter"),
                            rx.el.option("Piece", value="piece"),
                            rx.el.option("Roll", value="roll"),
                            name="unit",
                            value=MaterialState.unit,
                            on_change=MaterialState.set_unit,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Unit Price"),
                        _form_input(
                            name="unit_price",
                            type="number",
                            default_value=MaterialState.unit_price.to_string(),
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Reorder Level"),
                        _form_input(
                            name="reorder_level",
                            type="number",
                            default_value=MaterialState.reorder_level.to_string(),
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Supplier Name (Optional)"),
                        _form_input(
                            name="supplier_name",
                            default_value=MaterialState.supplier_name,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Supplier Contact (Optional)"),
                        _form_input(
                            name="supplier_contact",
                            default_value=MaterialState.supplier_contact,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    _form_label("Last Purchase Date (Optional)"),
                    _form_input(
                        name="last_purchase_date",
                        type="date",
                        default_value=MaterialState.last_purchase_date,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=MaterialState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            MaterialState.is_editing, "Save Changes", "Add Material"
                        ),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4",
                ),
                on_submit=MaterialState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[48rem] max-w-[90vw]",
        ),
        open=MaterialState.show_form,
        on_open_change=MaterialState.set_show_form,
    )


def delete_material_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirm Deletion", class_name="text-xl font-bold text-gray-800"
            ),
            rx.dialog.description(
                "Are you sure you want to delete this material? This action cannot be undone.",
                class_name="my-4 text-gray-600",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=MaterialState.cancel_delete,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Delete",
                        on_click=MaterialState.delete_material,
                        class_name="py-2 px-4 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold",
                    )
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-100 w-96",
        ),
        open=MaterialState.show_delete_dialog,
        on_open_change=MaterialState.set_show_delete_dialog,
    )