import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
import reflex as rx

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str | None = None,
    attachment_filename: str | None = None,
) -> bool:
    """Sends an email with an optional attachment."""
    if not all([SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD]):
        logging.error("SMTP credentials not fully configured. Cannot send email.")
        return False
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    if attachment_path and attachment_filename:
        try:
            full_path = rx.get_upload_dir() / attachment_path
            with open(full_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename= {attachment_filename}"
            )
            msg.attach(part)
        except Exception as e:
            logging.exception(f"Failed to attach file {attachment_path}: {e}")
            return False
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, to_email, text)
        server.quit()
        logging.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logging.exception(f"Failed to send email to {to_email}: {e}")
        return False