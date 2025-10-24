import os
import reflex as rx
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
if not all([ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
    logging.warning(
        "Twilio credentials are not fully configured. WhatsApp notifications will be disabled."
    )
    client = None
else:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)


def _send_whatsapp_message(to: str, body: str, media_url: str | None = None) -> bool:
    """Sends a WhatsApp message using Twilio."""
    if not client:
        logging.error("Twilio client is not initialized. Cannot send WhatsApp message.")
        return False
    from_number = f"whatsapp:{TWILIO_PHONE_NUMBER}"
    to_number = f"whatsapp:+91{to}" if not to.startswith("+") else f"whatsapp:{to}"
    try:
        message_args = {"body": body, "from_": from_number, "to": to_number}
        if media_url:
            message_args["media_url"] = [media_url]
        client.messages.create(**message_args)
        logging.info(f"WhatsApp message sent to {to_number}")
        return True
    except TwilioRestException as e:
        logging.exception(f"Failed to send WhatsApp message to {to_number}: {e}")
        return False


def send_whatsapp_order_confirmation(
    customer_phone: str,
    customer_name: str,
    order_id: int,
    delivery_date: str,
    total_amount: float,
) -> bool:
    """Sends an order confirmation via WhatsApp."""
    message = f"Hi {customer_name}, your order #{order_id} with TailorFlow has been confirmed!\n\n*Total Amount:* ₹{total_amount:.2f}\n*Estimated Delivery:* {delivery_date}\n\nWe'll notify you once it's ready. Thank you!"
    return _send_whatsapp_message(customer_phone, message)


def send_whatsapp_order_ready(
    customer_phone: str, customer_name: str, order_id: int
) -> bool:
    """Sends an order ready notification via WhatsApp."""
    message = f"Hi {customer_name}, great news! Your order #{order_id} is now ready for pickup.\nYou can collect it from our shop anytime during business hours.\n\nThank you for choosing TailorFlow!"
    return _send_whatsapp_message(customer_phone, message)


def send_whatsapp_invoice(
    customer_phone: str, customer_name: str, order_id: int, invoice_pdf_url: str
) -> bool:
    """Sends an invoice PDF via WhatsApp."""
    message = f"Hi {customer_name}, please find attached the invoice for your order #{order_id}.\n\nThank you for your business!"
    return _send_whatsapp_message(customer_phone, message, media_url=invoice_pdf_url)


def send_whatsapp_order_photo(
    customer_phone: str, customer_name: str, order_id: int, photo_url: str
) -> bool:
    """Sends an order photo for customer approval via WhatsApp."""
    message = f"Hi {customer_name}, here is a photo of your completed order #{order_id} for your approval. Please let us know if it looks good!"
    return _send_whatsapp_message(customer_phone, message, media_url=photo_url)