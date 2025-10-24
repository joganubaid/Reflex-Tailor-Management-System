import reflex as rx
from app.state import CustomerState


def customer_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(
                        CustomerState.is_editing, "Edit Customer", "Add New Customer"
                    ),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="name",
                        default_value=CustomerState.name,
                        placeholder="e.g., John Doe",
                        required=True,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone Number",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="phone_number",
                        default_value=CustomerState.phone_number,
                        placeholder="e.g., 9876543210",
                        required=True,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address (Optional)",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="email",
                        type="email",
                        default_value=CustomerState.email,
                        placeholder="e.g., john.doe@example.com",
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Address (Optional)",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        name="address",
                        default_value=CustomerState.address,
                        placeholder="Enter full address",
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Notes (Optional)",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        name="notes",
                        default_value=CustomerState.notes,
                        placeholder="Any special notes about the customer",
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "WhatsApp Opt-in",
                            class_name="flex items-center gap-2 text-sm font-semibold text-gray-700",
                        ),
                        rx.el.input(
                            type="checkbox",
                            name="whatsapp_opt_in",
                            checked=CustomerState.whatsapp_opt_in,
                            class_name="form-checkbox h-5 w-5 text-purple-600 border-gray-300 rounded focus:ring-purple-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Notification Preference",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.el.option("SMS", value="sms"),
                            rx.el.option("WhatsApp", value="whatsapp"),
                            rx.el.option("Both", value="both"),
                            name="preferred_notification",
                            value=CustomerState.preferred_notification,
                            on_change=CustomerState.set_preferred_notification,
                            class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=CustomerState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            CustomerState.is_editing, "Save Changes", "Add Customer"
                        ),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4",
                ),
                on_submit=CustomerState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[32rem] max-w-[90vw]",
        ),
        open=CustomerState.show_form,
        on_open_change=CustomerState.set_show_form,
    )


def delete_confirmation_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirm Deletion", class_name="text-xl font-bold text-gray-800"
            ),
            rx.dialog.description(
                "Are you sure you want to delete this customer? This action cannot be undone.",
                class_name="my-4 text-gray-600",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=CustomerState.cancel_delete,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Delete",
                        on_click=CustomerState.delete_customer,
                        class_name="py-2 px-4 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold",
                    )
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-100 w-96",
        ),
        open=CustomerState.show_delete_dialog,
        on_open_change=CustomerState.set_show_delete_dialog,
    )