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
        "Twilio credentials are not fully configured. SMS notifications will be disabled."
    )
    client = None
else:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)


def _send_sms(to: str, body: str) -> bool:
    """Sends an SMS message using Twilio."""
    if not client:
        logging.error("Twilio client is not initialized. Cannot send SMS.")
        return False
    if not to.startswith("+"):
        to = f"+91{to}"
    try:
        client.messages.create(body=body, from_=TWILIO_PHONE_NUMBER, to=to)
        logging.info(f"SMS sent to {to}")
        return True
    except TwilioRestException as e:
        logging.exception(f"Failed to send SMS to {to}: {e}")
        return False


def send_order_confirmation(
    customer_phone: str,
    customer_name: str,
    order_id: int,
    delivery_date: str,
    total_amount: float,
) -> bool:
    """Sends an order confirmation SMS."""
    message = f"Hi {customer_name}, your order #{order_id} with TailorFlow has been confirmed!\nTotal: ₹{total_amount:.2f}\nEst. Delivery: {delivery_date}\nWe'll notify you once it's ready. Thank you!"
    return _send_sms(customer_phone, message)


def send_order_ready_notification(
    customer_phone: str, customer_name: str, order_id: int
) -> bool:
    """Sends an SMS when an order is ready for pickup."""
    message = f"Hi {customer_name}, your order #{order_id} is ready for pickup!\nYou can collect it from our shop anytime during business hours.\nThank you for choosing TailorFlow!"
    return _send_sms(customer_phone, message)


def send_delivery_reminder(
    customer_phone: str, customer_name: str, order_id: int
) -> bool:
    """Sends a delivery reminder SMS."""
    message = f"Hi {customer_name}, this is a friendly reminder that your order #{order_id} is ready for pickup.\nPlease collect it at your earliest convenience.\nThank you, TailorFlow."
    return _send_sms(customer_phone, message)