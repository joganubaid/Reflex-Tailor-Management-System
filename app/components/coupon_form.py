import reflex as rx
from app.states.coupon_state import CouponState


def _form_label(text: str) -> rx.Component:
    return rx.el.label(
        text, class_name="block text-sm font-semibold text-gray-700 mb-2"
    )


def _form_input(**props) -> rx.Component:
    return rx.el.input(
        **props,
        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
    )


def coupon_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(CouponState.is_editing, "Edit Coupon", "Create New Coupon"),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    _form_label("Coupon Code"),
                    rx.el.div(
                        _form_input(
                            name="coupon_code",
                            default_value=CouponState.coupon_code,
                            required=True,
                        ),
                        rx.el.button(
                            "Generate",
                            type="button",
                            on_click=CouponState.generate_coupon_code,
                            class_name="ml-2 px-3 py-2 text-sm bg-gray-100 rounded-md hover:bg-gray-200",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Discount Type"),
                        rx.el.select(
                            rx.el.option("Percentage", value="percentage"),
                            rx.el.option("Fixed Amount", value="fixed_amount"),
                            name="discount_type",
                            value=CouponState.discount_type,
                            on_change=CouponState.set_discount_type,
                            class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                        ),
                    ),
                    rx.el.div(
                        _form_label("Discount Value"),
                        _form_input(
                            name="discount_value",
                            type="number",
                            default_value=CouponState.discount_value.to_string(),
                            required=True,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Minimum Order Value"),
                        _form_input(
                            name="min_order_value",
                            type="number",
                            default_value=CouponState.min_order_value.to_string(),
                        ),
                    ),
                    rx.el.div(
                        _form_label("Usage Limit"),
                        _form_input(
                            name="usage_limit",
                            type="number",
                            default_value=CouponState.usage_limit.to_string(),
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Valid From"),
                        _form_input(
                            name="valid_from",
                            type="date",
                            default_value=CouponState.valid_from,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Valid Until"),
                        _form_input(
                            name="valid_until",
                            type="date",
                            default_value=CouponState.valid_until,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    _form_label("Description (Optional)"),
                    rx.el.textarea(
                        name="description",
                        default_value=CouponState.description,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.input(
                        type="checkbox",
                        name="is_active",
                        checked=CouponState.is_active,
                        class_name="mr-2",
                    ),
                    rx.el.label(
                        "Is Active", class_name="text-sm font-semibold text-gray-700"
                    ),
                    class_name="flex items-center mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=CouponState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            CouponState.is_editing, "Save Changes", "Create Coupon"
                        ),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4",
                ),
                on_submit=CouponState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[36rem] max-w-[90vw]",
        ),
        open=CouponState.show_form,
        on_open_change=CouponState.set_show_form,
    )


def delete_coupon_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirm Deletion", class_name="text-xl font-bold text-gray-800"
            ),
            rx.dialog.description(
                "Are you sure you want to delete this coupon? This action cannot be undone.",
                class_name="my-4 text-gray-600",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=CouponState.cancel_delete,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Delete",
                        on_click=CouponState.delete_coupon,
                        class_name="py-2 px-4 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold",
                    )
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-100 w-96",
        ),
        open=CouponState.show_delete_dialog,
        on_open_change=CouponState.set_show_delete_dialog,
    )