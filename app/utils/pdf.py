import reflex as rx
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import Color, black, purple, white
from app.models import OrderWithCustomerName, Customer
import datetime
import logging


def generate_invoice_pdf(order: OrderWithCustomerName, customer: Customer) -> str:
    """Generate a PDF invoice for a given order."""
    upload_dir = rx.get_upload_dir() / "invoices"
    upload_dir.mkdir(parents=True, exist_ok=True)
    invoice_number = (
        f"INV-{order['order_id']}-{datetime.date.today().strftime('%Y%m%d')}"
    )
    file_path = upload_dir / f"{invoice_number}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    header_table = Table(
        [
            [
                Paragraph("<b>TailorFlow</b>", styles["h1"]),
                Paragraph(f"<b>INVOICE</b><br/>#{invoice_number}", styles["h2"]),
            ]
        ],
        colWidths=[3.5 * inch, 2 * inch],
    )
    header_table.setStyle(
        TableStyle(
            [("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (1, 0), "RIGHT")]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 0.25 * inch))
    shop_details = "<b>From:</b><br/>TailorFlow Inc.<br/>123 Main Street<br/>Anytown, ST 12345<br/>Email: contact@tailorflow.com"
    customer_details = f"<b>To:</b><br/>{customer['name']}<br/>{customer['phone_number']}<br/>{customer.get('address') or 'N/A'}"
    details_table = Table(
        [
            [
                Paragraph(shop_details, styles["Normal"]),
                Paragraph(customer_details, styles["Normal"]),
            ]
        ]
    )
    details_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(details_table)
    story.append(Spacer(1, 0.5 * inch))
    order_data = [
        ["Item", "Quantity", "Unit Price", "Total"],
        [
            f"{order['cloth_type'].capitalize()} ({order['special_instructions'] or 'Standard'})",
            str(order["quantity"]),
            f"₹{order['total_amount'] / order['quantity']:.2f}",
            f"₹{order['total_amount']:.2f}",
        ],
        ["", "", "", ""],
        ["", "", "Subtotal", f"₹{order['total_amount']:.2f}"],
        ["", "", "Discount", f"-₹{order.get('discount_amount', 0.0):.2f}"],
        [
            "",
            "",
            Paragraph("<b>Total Amount</b>", styles["Normal"]),
            Paragraph(
                f"<b>₹{float(order['total_amount']) - float(order.get('discount_amount', 0.0)):.2f}</b>",
                styles["Normal"],
            ),
        ],
        ["", "", "Advance Paid", f"₹{order['advance_payment']:.2f}"],
        [
            "",
            "",
            Paragraph("<b>Balance Due</b>", styles["Normal"]),
            Paragraph(f"<b>₹{order['balance_payment']:.2f}</b>", styles["Normal"]),
        ],
    ]
    order_table = Table(
        order_data, colWidths=[2.5 * inch, 1 * inch, 1 * inch, 1 * inch]
    )
    order_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), Color(0.9, 0.9, 0.9)),
                ("TEXTCOLOR", (0, 0), (-1, 0), black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("GRID", (0, 0), (-1, -1), 1, Color(0.8, 0.8, 0.8)),
                ("SPAN", (0, 2), (2, 2)),
                ("SPAN", (0, 3), (2, 3)),
                ("SPAN", (0, 4), (2, 4)),
                ("SPAN", (0, 5), (2, 5)),
                ("SPAN", (0, 6), (2, 6)),
                ("SPAN", (0, 7), (2, 7)),
                ("FONTNAME", (2, 5), (3, 5), "Helvetica-Bold"),
                ("FONTNAME", (2, 7), (3, 7), "Helvetica-Bold"),
            ]
        )
    )
    story.append(order_table)
    story.append(Spacer(1, 0.5 * inch))
    footer_text = "Thank you for your business! All payments are due upon receipt."
    story.append(Paragraph(footer_text, styles["Italic"]))
    try:
        doc.build(story)
        logging.info(f"Invoice generated: {file_path}")
        return f"invoices/{invoice_number}.pdf"
    except Exception as e:
        logging.exception(f"Failed to generate PDF invoice: {e}")
        return ""