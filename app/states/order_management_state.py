import reflex as rx
from typing import Optional


class OrderManagementState(rx.State):
    """Comprehensive order management for mobile"""

    show_manage_dialog: bool = False
    selected_order: dict | None = None
    active_tab: str = "actions"
    payment_amount: float = 0.0
    payment_method: str = "cash"
    send_sms: bool = True
    send_whatsapp: bool = False
    send_email: bool = False
    new_status: str = ""
    status_note: str = ""
    notification_type: str = "sms"
    custom_message: str = ""

    @rx.event
    def open_manage_dialog(self, order: dict):
        """Open management dialog for an order"""
        self.selected_order = order
        self.payment_amount = float(order.get("balance_payment", 0.0))
        self.show_manage_dialog = True

    @rx.event
    def close_manage_dialog(self):
        """Close dialog"""
        self.show_manage_dialog = False
        self.selected_order = None

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event(background=True)
    async def complete_order_full(self):
        """Complete order with all notifications"""
        async with self:
            if not self.selected_order:
                yield rx.toast.error("No order selected.")
                return
            from app.states.order_completion_state import OrderCompletionState

            order_completion_state = await self.get_state(OrderCompletionState)
            order_completion_state.payment_amount = self.payment_amount
            order_completion_state.payment_method = self.payment_method
            order_completion_state.send_sms = self.send_sms
            order_completion_state.send_whatsapp = self.send_whatsapp
            yield OrderCompletionState.start_completion(self.selected_order["order_id"])
        async with self:
            self.show_manage_dialog = False

    @rx.event(background=True)
    async def send_manual_notification(self):
        """Send manual notification"""
        async with self:
            if not self.selected_order or not self.custom_message:
                yield rx.toast.error("Order and message are required.")
                return
            customer_phone = self.selected_order.get("customer_phone", "")
            customer_name = self.selected_order.get("customer_name", "Customer")
            if self.notification_type == "sms":
                from app.utils.sms import _send_sms

                _send_sms(to=customer_phone, body=self.custom_message)
                yield rx.toast.success("SMS Sent!")
            elif self.notification_type == "whatsapp":
                from app.utils.whatsapp import _send_whatsapp_message

                _send_whatsapp_message(to=customer_phone, body=self.custom_message)
                yield rx.toast.success("WhatsApp message sent!")