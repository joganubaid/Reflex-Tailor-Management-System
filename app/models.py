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


class OrderWithCustomerName(Order):
    customer_name: str


class OrderMaterial(TypedDict):
    id: int
    order_id: int
    material_id: int
    quantity_used: float
    wastage: float
    cost: float


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