import reflex as rx
from app.states.order_management_state import OrderManagementState
from app.states.order_completion_state import OrderCompletionState
from app.state import OrderState


def _tab_button(label: str, icon: str, is_active: rx.Var[bool]) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(label, class_name="hidden md:inline"),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-2 px-4 py-2 text-sm font-semibold text-purple-600 bg-purple-100 rounded-lg",
            "flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg",
        ),
        on_click=OrderManagementState.set_active_tab(label.lower()),
    )


def _actions_tab() -> rx.Component:
    return rx.el.div(
        rx.cond(
            OrderManagementState.selected_order.get("status") == "ready",
            rx.el.div(
                rx.el.h3("Complete Order", class_name="text-lg font-bold mb-2"),
                rx.el.input(
                    name="payment_amount",
                    default_value=OrderManagementState.payment_amount.to_string(),
                    type="number",
                    placeholder="Payment Amount",
                    class_name="w-full p-2 border rounded mb-2",
                ),
                rx.el.select(
                    rx.el.option("Cash", value="cash"),
                    rx.el.option("UPI", value="upi"),
                    rx.el.option("Card", value="card"),
                    name="payment_method",
                    value=OrderManagementState.payment_method,
                    on_change=OrderManagementState.set_payment_method,
                    class_name="w-full p-2 border rounded mb-2",
                ),
                rx.el.button(
                    "Complete Order & Notify",
                    on_click=OrderCompletionState.start_completion(
                        OrderManagementState.selected_order["order_id"]
                    ),
                ),
                class_name="p-4 bg-gray-50 rounded-lg mb-4",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.h3("Update Status", class_name="text-lg font-bold mb-2"),
            rx.el.select(
                rx.el.option("Pending", value="pending"),
                rx.el.option("Cutting", value="cutting"),
                rx.el.option("Stitching", value="stitching"),
                rx.el.option("Finishing", value="finishing"),
                rx.el.option("Ready", value="ready"),
                rx.el.option("Delivered", value="delivered"),
                name="new_status",
                on_change=OrderManagementState.set_new_status,
                class_name="w-full p-2 border rounded mb-2",
            ),
            rx.el.button(
                "Update Status",
                on_click=lambda: OrderState.update_order_status(
                    OrderManagementState.selected_order["order_id"],
                    OrderManagementState.new_status,
                ),
            ),
            class_name="p-4 bg-gray-50 rounded-lg",
        ),
        class_name="space-y-4",
    )


def _notifications_tab() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Send Manual Notification", class_name="text-lg font-bold mb-2"),
        rx.el.select(
            rx.el.option("SMS", value="sms"),
            rx.el.option("WhatsApp", value="whatsapp"),
            name="notification_type",
            value=OrderManagementState.notification_type,
            on_change=OrderManagementState.set_notification_type,
            class_name="w-full p-2 border rounded mb-2",
        ),
        rx.el.textarea(
            name="custom_message",
            placeholder="Enter your message...",
            on_change=OrderManagementState.set_custom_message,
            class_name="w-full p-2 border rounded mb-2",
        ),
        rx.el.button(
            "Send Notification", on_click=OrderManagementState.send_manual_notification
        ),
        class_name="p-4 bg-gray-50 rounded-lg",
    )


def order_management_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                OrderManagementState.selected_order,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            f"Manage Order #{OrderManagementState.selected_order.get('order_id', '')}",
                            class_name="text-xl font-bold",
                        ),
                        rx.el.button(
                            rx.icon("x"),
                            on_click=OrderManagementState.close_manage_dialog,
                            class_name="p-2 rounded-full hover:bg-gray-100",
                        ),
                        class_name="flex justify-between items-center p-4 border-b",
                    ),
                    rx.el.div(
                        _tab_button(
                            "Actions",
                            "hammer",
                            OrderManagementState.active_tab == "actions",
                        ),
                        _tab_button(
                            "Notify",
                            "bell",
                            OrderManagementState.active_tab == "notify",
                        ),
                        class_name="flex space-x-2 p-2 bg-gray-100 rounded-lg m-4",
                    ),
                    rx.el.div(
                        rx.match(
                            OrderManagementState.active_tab,
                            ("actions", _actions_tab()),
                            ("notify", _notifications_tab()),
                            _actions_tab(),
                        ),
                        class_name="p-4",
                    ),
                ),
                rx.fragment(),
            ),
            class_name="p-0 bg-white rounded-xl shadow-lg border border-gray-100 w-full max-w-md mx-auto md:max-w-lg",
        ),
        open=OrderManagementState.show_manage_dialog,
        on_open_change=OrderManagementState.close_manage_dialog,
    )