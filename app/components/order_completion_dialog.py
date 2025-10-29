import reflex as rx
from app.states.order_completion_state import OrderCompletionState


def _form_label(text: str) -> rx.Component:
    return rx.el.label(
        text, class_name="block text-sm font-semibold text-gray-700 mb-2"
    )


def order_completion_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.cond(
                    OrderCompletionState.show_success_screen,
                    success_screen(),
                    completion_form(),
                ),
                class_name="w-full",
            ),
            class_name="p-0 bg-white rounded-xl shadow-lg border border-gray-100 w-[36rem] max-w-[90vw]",
        ),
        open=OrderCompletionState.show_completion_dialog,
        on_open_change=OrderCompletionState.close_dialog,
    )


def completion_form() -> rx.Component:
    return rx.el.form(
        rx.dialog.title(
            "Complete Order", class_name="text-2xl font-bold text-gray-800 p-6 border-b"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Customer", class_name="text-sm text-gray-500"),
                rx.el.p(
                    OrderCompletionState.order_to_complete.get("customer_name", ""),
                    class_name="font-semibold",
                ),
                class_name="flex justify-between items-center",
            ),
            rx.el.div(
                rx.el.p("Order ID", class_name="text-sm text-gray-500"),
                rx.el.p(
                    f"#{OrderCompletionState.order_to_complete.get('order_id', '')}",
                    class_name="font-semibold",
                ),
                class_name="flex justify-between items-center",
            ),
            rx.el.div(
                rx.el.p("Balance Due", class_name="text-sm text-gray-500"),
                rx.el.p(
                    f"₹{OrderCompletionState.order_to_complete.get('balance_payment', '0.00')}",
                    class_name="font-bold text-red-600",
                ),
                class_name="flex justify-between items-center",
            ),
            class_name="space-y-2 p-6 bg-gray-50",
        ),
        rx.el.div(
            rx.el.div(
                _form_label("Payment Amount"),
                rx.el.input(
                    name="payment_amount",
                    type="number",
                    default_value=OrderCompletionState.payment_amount.to_string(),
                    class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    required=True,
                ),
            ),
            rx.el.div(
                _form_label("Payment Method"),
                rx.el.select(
                    rx.el.option("Cash", value="cash"),
                    rx.el.option("UPI", value="upi"),
                    rx.el.option("Card", value="card"),
                    rx.el.option("Bank Transfer", value="bank_transfer"),
                    name="payment_method",
                    value=OrderCompletionState.payment_method,
                    on_change=OrderCompletionState.set_payment_method,
                    class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                ),
            ),
            class_name="grid grid-cols-2 gap-4 p-6",
        ),
        rx.el.div(
            _form_label("Notifications"),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        type="checkbox",
                        name="send_sms",
                        default_checked=OrderCompletionState.send_sms,
                        class_name="mr-2",
                    ),
                    rx.el.label("Send SMS Receipt", class_name="text-sm"),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.input(
                        type="checkbox",
                        name="send_whatsapp",
                        default_checked=OrderCompletionState.send_whatsapp,
                        class_name="mr-2",
                    ),
                    rx.el.label("Send WhatsApp Receipt", class_name="text-sm"),
                    class_name="flex items-center",
                ),
                class_name="flex gap-4",
            ),
            class_name="p-6 border-t",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                type="button",
                on_click=OrderCompletionState.close_dialog,
                class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
            ),
            rx.el.button(
                rx.cond(
                    OrderCompletionState.is_processing,
                    rx.el.div(rx.spinner(size="2"), class_name="h-6"),
                    "Complete Order",
                ),
                type="submit",
                class_name="py-2 px-6 rounded-lg bg-green-600 text-white hover:bg-green-700 font-semibold",
                disabled=OrderCompletionState.is_processing,
            ),
            class_name="flex justify-end gap-4 p-6 border-t bg-gray-50",
        ),
        on_submit=OrderCompletionState.complete_order,
    )


def success_screen() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("party_popper", class_name="h-16 w-16 text-green-500 mx-auto"),
            rx.el.h2(
                "Order Completed!", class_name="text-2xl font-bold text-center mt-4"
            ),
            rx.el.p(
                "All automated tasks have been successfully processed.",
                class_name="text-gray-600 text-center mt-2",
            ),
            class_name="p-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("gem", class_name="h-5 w-5 text-purple-500"),
                rx.el.p("Loyalty Points Awarded"),
                rx.el.p(
                    f"{OrderCompletionState.points_awarded}", class_name="font-bold"
                ),
                class_name="flex items-center justify-between p-3 bg-purple-50 rounded-lg",
            ),
            rx.cond(
                OrderCompletionState.tier_upgraded_to,
                rx.el.div(
                    rx.icon("award", class_name="h-5 w-5 text-yellow-500"),
                    rx.el.p("Tier Upgrade!"),
                    rx.el.p(
                        OrderCompletionState.tier_upgraded_to, class_name="font-bold"
                    ),
                    class_name="flex items-center justify-between p-3 bg-yellow-50 rounded-lg",
                ),
                rx.fragment(),
            ),
            rx.cond(
                OrderCompletionState.referrer_reward,
                rx.el.div(
                    rx.icon("gift", class_name="h-5 w-5 text-pink-500"),
                    rx.el.p("Referral Bonus"),
                    rx.el.p(
                        f"{OrderCompletionState.referrer_reward} pts",
                        class_name="font-bold",
                    ),
                    class_name="flex items-center justify-between p-3 bg-pink-50 rounded-lg",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.icon("send", class_name="h-5 w-5 text-blue-500"),
                rx.el.p("Notifications Sent"),
                rx.el.p(
                    OrderCompletionState.notification_channels.join(", "),
                    class_name="font-bold",
                ),
                class_name="flex items-center justify-between p-3 bg-blue-50 rounded-lg",
            ),
            class_name="space-y-3 p-6",
        ),
        rx.el.div(
            rx.el.button(
                "Close",
                on_click=OrderCompletionState.close_dialog,
                class_name="w-full py-3 bg-gray-200 rounded-lg font-semibold",
            ),
            class_name="p-6 border-t bg-gray-50",
        ),
    )