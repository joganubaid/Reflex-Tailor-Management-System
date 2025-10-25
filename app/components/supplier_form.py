import reflex as rx
from app.states.supplier_state import SupplierState


def supplier_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(
                        SupplierState.is_editing, "Edit Supplier", "Add New Supplier"
                    ),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Supplier Name",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="name",
                        default_value=SupplierState.name,
                        required=True,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Contact Number",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="contact",
                            default_value=SupplierState.contact,
                            required=True,
                            class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="email",
                            type="email",
                            default_value=SupplierState.email,
                            class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Address",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        name="address",
                        default_value=SupplierState.address,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Rating (1-5)",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="rating",
                        type="number",
                        default_value=SupplierState.rating.to_string(),
                        min=0,
                        max=5,
                        step=0.1,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Notes",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        name="notes",
                        default_value=SupplierState.notes,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=SupplierState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            SupplierState.is_editing, "Save Changes", "Add Supplier"
                        ),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4",
                ),
                on_submit=SupplierState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[36rem] max-w-[90vw]",
        ),
        open=SupplierState.show_form,
        on_open_change=SupplierState.set_show_form,
    )


def delete_supplier_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirm Deletion", class_name="text-xl font-bold text-gray-800"
            ),
            rx.dialog.description(
                "Are you sure you want to delete this supplier? This will also remove their associations with any materials. This action cannot be undone.",
                class_name="my-4 text-gray-600",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=SupplierState.cancel_delete,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Delete",
                        on_click=SupplierState.delete_supplier,
                        class_name="py-2 px-4 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold",
                    )
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-100 w-96",
        ),
        open=SupplierState.show_delete_dialog,
        on_open_change=SupplierState.set_show_delete_dialog,
    )