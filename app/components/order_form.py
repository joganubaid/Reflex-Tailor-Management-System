import reflex as rx
from app.state import OrderState


def _form_label(text: str) -> rx.Component:
    return rx.el.label(
        text, class_name="block text-sm font-semibold text-gray-700 mb-2"
    )


def _form_input(*children, **props) -> rx.Component:
    base_class = "w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500"
    if "class_name" in props:
        props["class_name"] = f"{base_class} {props['class_name']}"
    else:
        props["class_name"] = base_class
    return rx.el.input(*children, **props)


def _form_select(*children, **props) -> rx.Component:
    return rx.el.select(
        *children,
        **props,
        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
    )


def measurement_fields() -> rx.Component:
    cloth_type = OrderState.selected_cloth_type
    return rx.el.div(
        rx.el.h3(
            "Measurements",
            class_name="text-lg font-bold text-gray-800 mb-4 border-t pt-6 mt-6",
        ),
        rx.el.div(
            rx.cond(
                (cloth_type == "shirt")
                | (cloth_type == "suit")
                | (cloth_type == "blouse")
                | (cloth_type == "dress"),
                rx.el.div(
                    _form_label("Chest"),
                    _form_input(
                        name="chest",
                        type="number",
                        default_value=OrderState.chest,
                        on_change=OrderState.set_chest,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "shirt")
                | (cloth_type == "suit")
                | (cloth_type == "pant")
                | (cloth_type == "blouse")
                | (cloth_type == "dress"),
                rx.el.div(
                    _form_label("Waist"),
                    _form_input(
                        name="waist",
                        type="number",
                        default_value=OrderState.waist,
                        on_change=OrderState.set_waist,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "suit")
                | (cloth_type == "pant")
                | (cloth_type == "dress"),
                rx.el.div(
                    _form_label("Hip"),
                    _form_input(
                        name="hip",
                        type="number",
                        default_value=OrderState.hip,
                        on_change=OrderState.set_hip,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "shirt")
                | (cloth_type == "suit")
                | (cloth_type == "blouse")
                | (cloth_type == "dress"),
                rx.el.div(
                    _form_label("Shoulder Width"),
                    _form_input(
                        name="shoulder_width",
                        type="number",
                        default_value=OrderState.shoulder_width,
                        on_change=OrderState.set_shoulder_width,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "shirt")
                | (cloth_type == "suit")
                | (cloth_type == "blouse"),
                rx.el.div(
                    _form_label("Sleeve Length"),
                    _form_input(
                        name="sleeve_length",
                        type="number",
                        default_value=OrderState.sleeve_length,
                        on_change=OrderState.set_sleeve_length,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "shirt")
                | (cloth_type == "blouse")
                | (cloth_type == "dress"),
                rx.el.div(
                    _form_label("Length"),
                    _form_input(
                        name="shirt_length",
                        type="number",
                        default_value=OrderState.shirt_length,
                        on_change=OrderState.set_shirt_length,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "suit") | (cloth_type == "pant"),
                rx.el.div(
                    _form_label("Pant Length"),
                    _form_input(
                        name="pant_length",
                        type="number",
                        default_value=OrderState.pant_length,
                        on_change=OrderState.set_pant_length,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "suit") | (cloth_type == "pant"),
                rx.el.div(
                    _form_label("Inseam"),
                    _form_input(
                        name="inseam",
                        type="number",
                        default_value=OrderState.inseam,
                        on_change=OrderState.set_inseam,
                    ),
                ),
            ),
            rx.cond(
                (cloth_type == "shirt") | (cloth_type == "suit"),
                rx.el.div(
                    _form_label("Neck"),
                    _form_input(
                        name="neck",
                        type="number",
                        default_value=OrderState.neck,
                        on_change=OrderState.set_neck,
                    ),
                ),
            ),
            class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
        ),
        class_name="mt-4",
    )


def order_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(OrderState.is_editing_order, "Edit Order", "Add New Order"),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Customer"),
                        _form_select(
                            rx.el.option("Select a customer", value="", disabled=True),
                            rx.foreach(
                                OrderState.available_customers,
                                lambda customer: rx.el.option(
                                    f"{customer['name']} ({customer['phone_number']})",
                                    value=customer["customer_id"].to_string(),
                                ),
                            ),
                            name="customer_id",
                            value=OrderState.selected_customer_id,
                            on_change=OrderState.set_selected_customer_id,
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Cloth Type"),
                        _form_select(
                            rx.el.option("Shirt", value="shirt"),
                            rx.el.option("Pant", value="pant"),
                            rx.el.option("Suit", value="suit"),
                            rx.el.option("Blouse", value="blouse"),
                            rx.el.option("Dress", value="dress"),
                            name="cloth_type",
                            value=OrderState.selected_cloth_type,
                            on_change=OrderState.on_cloth_type_changed,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Quantity"),
                        _form_input(
                            name="quantity",
                            type="number",
                            default_value=OrderState.order_quantity,
                            on_change=OrderState.set_order_quantity,
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Delivery Date"),
                        _form_input(
                            name="delivery_date",
                            type="date",
                            default_value=OrderState.order_delivery_date,
                            on_change=OrderState.set_order_delivery_date,
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    _form_label("Priority"),
                    _form_select(
                        rx.el.option("Standard", value="standard"),
                        rx.el.option("High", value="high"),
                        rx.el.option("Urgent", value="urgent"),
                        name="priority",
                        value=OrderState.order_priority,
                        on_change=OrderState.set_order_priority,
                    ),
                    class_name="mb-4",
                ),
                measurement_fields(),
                rx.el.div(
                    _form_label("Special Instructions (Optional)"),
                    rx.el.textarea(
                        name="special_instructions",
                        default_value=OrderState.order_special_instructions,
                        on_change=OrderState.set_order_special_instructions,
                        placeholder="e.g., add extra pockets",
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="my-6",
                ),
                rx.el.div(
                    _form_label("Pricing"),
                    rx.el.div(
                        rx.el.div(
                            _form_label("Total Amount"),
                            _form_input(
                                name="total_amount",
                                type="number",
                                default_value=OrderState.order_total_amount,
                                on_change=[
                                    OrderState.set_order_total_amount,
                                    OrderState.calculate_balance,
                                ],
                                required=True,
                            ),
                        ),
                        rx.el.div(
                            _form_label("Advance Payment"),
                            _form_input(
                                name="advance_payment",
                                type="number",
                                default_value=OrderState.order_advance_payment,
                                on_change=[
                                    OrderState.set_order_advance_payment,
                                    OrderState.calculate_balance,
                                ],
                            ),
                        ),
                        rx.el.div(
                            _form_label("Balance"),
                            _form_input(
                                name="balance_payment",
                                type="number",
                                value=OrderState.order_balance_payment,
                                is_read_only=True,
                                class_name="w-full p-3 bg-gray-100 border border-gray-200 rounded-lg",
                            ),
                        ),
                        class_name="grid grid-cols-3 gap-4",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=OrderState.toggle_order_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            OrderState.is_editing_order, "Save Changes", "Add Order"
                        ),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4 mt-8",
                ),
                on_submit=OrderState.handle_order_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[56rem] max-w-[95vw]",
        ),
        open=OrderState.show_order_form,
        on_open_change=OrderState.set_show_order_form,
    )