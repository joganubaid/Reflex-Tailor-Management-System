import os
import reflex as rx
import razorpay
import logging
from typing import Optional

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
if not all([RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET]):
    logging.warning(
        "Razorpay credentials not fully configured. Payment link generation will be disabled."
    )
    client = None
else:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def create_payment_link(
    amount: float,
    description: str,
    customer_name: str,
    customer_contact: str,
    customer_email: Optional[str],
    order_id: int,
) -> Optional[str]:
    """Create a Razorpay payment link."""
    if not client:
        logging.error("Razorpay client not initialized. Cannot create payment link.")
        return None
    try:
        payment_link_data = {
            "amount": int(amount * 100),
            "currency": "INR",
            "accept_partial": False,
            "description": description,
            "customer": {
                "name": customer_name,
                "contact": customer_contact,
                "email": customer_email,
            },
            "notify": {"sms": True, "email": bool(customer_email)},
            "reminder_enable": True,
            "notes": {"order_id": str(order_id)},
            "callback_url": f"{os.getenv('BASE_URL', 'http://localhost:3000')}/payment-success",
            "callback_method": "get",
        }
        payment_link = client.payment_link.create(payment_link_data)
        return payment_link.get("short_url")
    except Exception as e:
        logging.exception(f"Failed to create Razorpay payment link: {e}")
        return None