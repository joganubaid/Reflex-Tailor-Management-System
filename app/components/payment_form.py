import reflex as rx
from app.states.payment_state import PaymentState


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


def payment_installment_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    "Add Payment Installment",
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    _form_label("Order (Customer - Balance)"),
                    _form_select(
                        rx.el.option("Select an order", value="", disabled=True),
                        rx.foreach(
                            PaymentState.orders_with_balance,
                            lambda order: rx.el.option(
                                f"#{order['order_id']} - {order['customer_name']} (₹{order['balance_payment']})",
                                value=order["order_id"].to_string(),
                            ),
                        ),
                        name="order_id",
                        value=PaymentState.selected_order_id,
                        on_change=PaymentState.set_selected_order_id,
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Installment Amount"),
                        _form_input(
                            name="installment_amount",
                            type="number",
                            default_value=PaymentState.installment_amount,
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Due Date"),
                        _form_input(
                            name="due_date",
                            type="date",
                            default_value=PaymentState.due_date,
                            required=True,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                _form_label("Notes (Optional)"),
                rx.el.textarea(
                    name="notes",
                    default_value=PaymentState.notes,
                    placeholder="Any notes regarding this installment",
                    class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=PaymentState.toggle_installment_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        "Add Installment",
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4 mt-8",
                ),
                on_submit=PaymentState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[40rem] max-w-[90vw]",
        ),
        open=PaymentState.show_installment_form,
        on_open_change=PaymentState.set_show_installment_form,
    )