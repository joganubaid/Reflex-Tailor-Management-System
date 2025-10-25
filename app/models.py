from typing import TypedDict
import datetime


class Customer(TypedDict):
    customer_id: int
    name: str
    phone_number: str
    email: str | None
    address: str | None
    registration_date: str
    total_orders: int
    notes: str | None
    whatsapp_opt_in: bool
    preferred_notification: str


class Measurement(TypedDict):
    measurement_id: int
    customer_id: int
    cloth_type: str
    chest: float | None
    waist: float | None
    hip: float | None
    shoulder_width: float | None
    sleeve_length: float | None
    shirt_length: float | None
    pant_length: float | None
    inseam: float | None
    neck: float | None
    measurement_date: str


class Material(TypedDict):
    material_id: int
    material_name: str
    material_type: str
    quantity_in_stock: float
    unit: str
    unit_price: float
    reorder_level: float
    supplier_name: str | None
    supplier_contact: str | None
    last_purchase_date: str | None
    batch_number: str | None


class Order(TypedDict):
    order_id: int
    customer_id: int
    order_date: str
    delivery_date: str
    status: str
    cloth_type: str
    quantity: int
    total_amount: float
    advance_payment: float
    balance_payment: float
    special_instructions: str | None
    assigned_worker: int | None
    labor_cost: float | None
    material_cost: float | None
    profit: float | None


class OrderWithCustomerName(Order):
    customer_name: str


class OrderMaterial(TypedDict):
    id: int
    order_id: int
    material_id: int
    quantity_used: float
    wastage: float
    cost: float


class PaymentInstallment(TypedDict):
    installment_id: int
    order_id: int
    installment_number: int
    amount: float
    due_date: str
    paid_date: str | None
    status: str
    payment_method: str | None
    notes: str | None


class Photo(TypedDict):
    photo_id: int
    photo_type: str
    reference_id: int
    file_name: str
    file_path: str
    storage_type: str
    file_size: int
    mime_type: str
    upload_date: str
    uploaded_by: str | None
    caption: str | None
    is_approved: bool
    approval_date: str | None


class PaymentReminder(TypedDict):
    reminder_id: int
    installment_id: int
    reminder_date: str
    sent_date: str | None
    status: str


class Transaction(TypedDict):
    transaction_id: int
    order_id: int
    transaction_date: str
    transaction_type: str
    amount: float
    payment_method: str | None
    description: str | None
    material_id: int | None
    invoice_number: str | None
    total_amount: float
    status: str


class Worker(TypedDict):
    worker_id: int
    worker_name: str
    phone_number: str
    role: str
    salary: float
    joining_date: str
    active_status: bool
    orders_assigned: int


class Invoice(TypedDict):
    invoice_id: int
    order_id: int
    invoice_number: str
    invoice_date: str
    subtotal: float
    gst_amount: float
    total_amount: float
    payment_status: str
    pdf_path: str | None


class Supplier(TypedDict):
    supplier_id: int
    name: str
    contact: str
    email: str | None
    address: str | None
    rating: float | None
    notes: str | None
    registration_date: str
    materials_count: int


class MaterialSupplier(TypedDict):
    id: int
    material_id: int
    supplier_id: int
    price: float
    is_preferred: bool


class PaymentInstallment(TypedDict):
    installment_id: int
    order_id: int
    customer_name: str
    customer_phone: str
    installment_number: int
    amount: float
    due_date: str
    paid_date: str | None
    status: str
    payment_method: str | None
    notes: str | None