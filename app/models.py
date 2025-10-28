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
    opt_in_whatsapp: bool
    prefer_whatsapp: str


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
    priority: str
    is_bulk_order: bool
    bulk_order_details: str | None
    order_template_id: int | None
    is_duplicate: bool | None
    original_order_id: int | None
    coupon_code: str | None
    discount_amount: float | None
    points_earned: int | None


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
    customer_name: str
    customer_phone: str
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
    notes: str | None


class OrderTemplate(TypedDict):
    template_id: int
    template_name: str
    cloth_type: str
    measurements: dict
    special_instructions: str | None
    default_price: float | None
    created_date: str
    created_by: str | None
    is_active: bool


class QCCheckpoint(TypedDict):
    checklist_id: int
    order_id: int
    checkpoint_name: str
    status: str
    checked_by: str | None
    checked_date: str | None
    notes: str | None
    created_at: str


class AlterationOrder(TypedDict):
    alteration_id: int
    customer_id: int
    original_order_id: int | None
    alteration_type: str
    description: str
    price: float
    status: str
    created_date: str
    completion_date: str | None
    assigned_worker: int | None
    notes: str | None


class WorkerAttendance(TypedDict):
    attendance_id: int
    worker_id: int
    worker_name: str
    date: str
    check_in_time: str | None
    check_out_time: str | None
    total_hours: float | None
    status: str
    notes: str | None


class WorkerTask(TypedDict):
    task_id: int
    order_id: int
    worker_id: int
    worker_name: str
    task_type: str
    assigned_date: str
    completed_date: str | None
    status: str
    notes: str | None


class WorkerSkill(TypedDict):
    skill_id: int
    worker_id: int
    skill_name: str
    proficiency_level: str
    years_experience: int


class WorkerLeave(TypedDict):
    leave_id: int
    worker_id: int
    worker_name: str
    leave_type: str
    start_date: str
    end_date: str
    total_days: int
    reason: str
    status: str


class ExpenseCategory(TypedDict):
    category_id: int
    category_name: str
    description: str | None


class Expense(TypedDict):
    expense_id: int
    category_id: int
    category_name: str
    amount: float
    expense_date: str
    description: str | None
    vendor_name: str | None


class BankAccount(TypedDict):
    account_id: int
    bank_name: str
    account_number: str
    account_type: str
    balance: float
    is_active: bool


class AlertSetting(TypedDict):
    setting_id: int
    alert_type: str
    enabled: bool
    threshold_value: float | None
    notification_method: str
    recipients: str | None


class AlertHistory(TypedDict):
    alert_id: int
    alert_type: str
    message: str
    severity: str
    triggered_at: str
    status: str


class AutomationWorkflow(TypedDict):
    workflow_id: int
    workflow_name: str
    trigger_event: str
    is_active: bool
    execution_count: int


class WorkerTaskWithDetails(TypedDict):
    task_id: int
    worker_id: int
    order_id: int
    task_type: str
    assigned_date: str
    due_date: str | None
    completed_date: str | None
    status: str
    notes: str | None
    worker_name: str
    customer_name: str
    cloth_type: str