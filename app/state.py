import reflex as rx
from typing import Any, cast
from app.models import (
    Customer,
    Order,
    Measurement,
    OrderWithCustomerName,
    Material,
    Transaction,
    Invoice,
)
import datetime
from sqlalchemy import text, func, select


class BaseState(rx.State):
    """The base state for the app."""

    pass


class OrderState(BaseState):
    orders: list[OrderWithCustomerName] = []
    show_order_form: bool = False
    is_editing_order: bool = False
    editing_order_id: int | None = None
    available_customers: list[Customer] = []
    available_workers: list[dict] = []
    selected_customer_id: str = ""
    selected_cloth_type: str = "shirt"
    order_quantity: int = 1
    order_delivery_date: str = ""
    order_status: str = "pending"
    order_total_amount: float = 0.0
    order_advance_payment: float = 0.0
    order_special_instructions: str = ""
    assigned_worker_id: str = ""
    save_measurements: bool = True
    chest: float | None = None
    waist: float | None = None
    hip: float | None = None
    shoulder_width: float | None = None
    sleeve_length: float | None = None
    shirt_length: float | None = None
    pant_length: float | None = None
    inseam: float | None = None
    neck: float | None = None

    @rx.var
    def order_balance_payment(self) -> float:
        return self.order_total_amount - self.order_advance_payment

    @rx.event(background=True)
    async def get_orders(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT o.*, c.name as customer_name 
FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
ORDER BY o.order_date DESC""")
            )
            rows = result.mappings().all()
            async with self:
                self.orders = [cast(OrderWithCustomerName, dict(row)) for row in rows]

    @rx.event
    def toggle_order_form(self):
        self.show_order_form = not self.show_order_form
        self.is_editing_order = False
        self._reset_order_form()
        if self.show_order_form:
            return OrderState.load_form_data

    def _reset_order_form(self):
        self.editing_order_id = None
        self.selected_customer_id = ""
        self.selected_cloth_type = "shirt"
        self.order_quantity = 1
        self.order_delivery_date = ""
        self.order_status = "pending"
        self.order_total_amount = 0.0
        self.order_advance_payment = 0.0
        self.order_special_instructions = ""
        self.assigned_worker_id = ""
        self.save_measurements = True
        self._reset_measurements()

    def _reset_measurements(self):
        self.chest = None
        self.waist = None
        self.hip = None
        self.shoulder_width = None
        self.sleeve_length = None
        self.shirt_length = None
        self.pant_length = None
        self.inseam = None
        self.neck = None

    @rx.event(background=True)
    async def load_form_data(self):
        async with rx.asession() as session:
            customer_result = await session.execute(
                text(
                    "SELECT customer_id, name, phone_number FROM customers ORDER BY name"
                )
            )
            async with self:
                self.available_customers = [
                    cast(Customer, dict(row))
                    for row in customer_result.mappings().all()
                ]

    @rx.event
    def on_cloth_type_changed(self, cloth_type: str):
        self.selected_cloth_type = cloth_type

    @rx.event
    def calculate_balance(self, value: Any):
        pass

    @rx.event(background=True)
    async def handle_order_form_submit(self, form_data: dict):
        """Handle the submission of the order form for both add and edit."""
        if self.is_editing_order:
            async with self:
                self.show_order_form = False
            yield rx.toast.info("Order editing functionality is not yet implemented.")
        else:
            yield OrderState.add_order(form_data)

    @rx.event(background=True)
    async def add_order(self, form_data: dict):
        """Adds a new order to the database and sends a confirmation SMS."""
        from app.utils.sms import send_order_confirmation

        customer_id = int(form_data["customer_id"])
        total_amount = float(form_data.get("total_amount", 0))
        advance_payment = float(form_data.get("advance_payment", 0))
        delivery_date = form_data.get("delivery_date") or None
        async with rx.asession() as session:
            result = await session.execute(
                text("""INSERT INTO orders (customer_id, order_date, delivery_date, status, cloth_type, quantity, total_amount, advance_payment, balance_payment, special_instructions)
                     VALUES (:customer_id, :order_date, :delivery_date, :status, :cloth_type, :quantity, :total_amount, :advance_payment, :balance_payment, :special_instructions)
                     RETURNING order_id"""),
                {
                    "customer_id": customer_id,
                    "order_date": datetime.date.today(),
                    "delivery_date": delivery_date,
                    "status": "pending",
                    "cloth_type": form_data["cloth_type"],
                    "quantity": int(form_data.get("quantity", 1)),
                    "total_amount": total_amount,
                    "advance_payment": advance_payment,
                    "balance_payment": total_amount - advance_payment,
                    "special_instructions": form_data.get("special_instructions"),
                },
            )
            new_order_id = result.scalar_one()
            await session.commit()
        customer = next(
            (c for c in self.available_customers if c["customer_id"] == customer_id),
            None,
        )
        sms_sent = False
        if customer:
            sms_sent = send_order_confirmation(
                customer_phone=customer["phone_number"],
                customer_name=customer["name"],
                order_id=new_order_id,
                delivery_date=str(delivery_date) if delivery_date else "TBA",
                total_amount=total_amount,
            )
        async with self:
            self.show_order_form = False
        yield rx.toast.success("Order added successfully!")
        if customer and (not sms_sent):
            yield rx.toast.error("Failed to send order confirmation SMS.")
        yield OrderState.get_orders

    @rx.event(background=True)
    async def update_order_status(self, order_id: int, new_status: str):
        from app.utils.sms import send_order_ready_notification

        async with self, rx.asession() as session:
            await session.execute(
                text("UPDATE orders SET status = :status WHERE order_id = :order_id"),
                {"status": new_status, "order_id": order_id},
            )
            await session.commit()
        yield OrderState.get_orders
        yield rx.toast.info(f"Order #{order_id} status updated to {new_status}.")
        if new_status.lower() == "ready":
            async with rx.asession() as session:
                result = await session.execute(
                    text("""SELECT c.name, c.phone_number 
                             FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
                             WHERE o.order_id = :order_id"""),
                    {"order_id": order_id},
                )
                customer_info = result.mappings().first()
            if customer_info:
                sms_sent = send_order_ready_notification(
                    customer_phone=customer_info["phone_number"],
                    customer_name=customer_info["name"],
                    order_id=order_id,
                )
                if not sms_sent:
                    yield rx.toast.error(
                        f"Failed to send 'order ready' SMS for order #{order_id}."
                    )
            else:
                yield rx.toast.error(
                    f"Could not find customer details for order #{order_id} to send SMS."
                )


class CustomerState(BaseState):
    customers: list[Customer] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_customer_id: int | None = None
    show_delete_dialog: bool = False
    customer_to_delete: Customer | None = None
    name: str = ""
    phone_number: str = ""
    email: str = ""
    address: str = ""
    notes: str = ""

    @rx.event(background=True)
    async def get_customers(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT c.*, COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY c.name""")
            )
            rows = result.mappings().all()
            async with self:
                self.customers = [cast(Customer, dict(row)) for row in rows]

    @rx.var
    def filtered_customers(self) -> list[Customer]:
        if not self.search_query.strip():
            return self.customers
        lower_query = self.search_query.lower()
        return [
            c
            for c in self.customers
            if lower_query in c["name"].lower() or lower_query in c["phone_number"]
        ]

    @rx.event
    async def add_customer(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text(
                    "INSERT INTO customers (name, phone_number, email, address, notes, registration_date) VALUES (:name, :phone_number, :email, :address, :notes, :registration_date)"
                ),
                {
                    "name": form_data["name"],
                    "phone_number": form_data["phone_number"],
                    "email": form_data.get("email", ""),
                    "address": form_data.get("address", ""),
                    "notes": form_data.get("notes", ""),
                    "registration_date": datetime.date.today(),
                },
            )
            await session.commit()
        self.show_form = False
        yield rx.toast.success("Customer added successfully!")
        yield CustomerState.get_customers
        return

    @rx.event
    async def update_customer(self, form_data: dict):
        if self.editing_customer_id is None:
            yield rx.toast.error("No customer selected for editing.")
            return
        async with rx.asession() as session:
            await session.execute(
                text(
                    "UPDATE customers SET name = :name, phone_number = :phone_number, email = :email, address = :address, notes = :notes WHERE customer_id = :customer_id"
                ),
                {
                    "name": form_data["name"],
                    "phone_number": form_data["phone_number"],
                    "email": form_data.get("email", ""),
                    "address": form_data.get("address", ""),
                    "notes": form_data.get("notes", ""),
                    "customer_id": self.editing_customer_id,
                },
            )
            await session.commit()
        self.show_form = False
        yield rx.toast.success("Customer updated successfully!")
        yield CustomerState.get_customers
        return

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        if self.is_editing:
            return CustomerState.update_customer(form_data)
        else:
            return CustomerState.add_customer(form_data)

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self.is_editing = False
        self._reset_form_fields()

    @rx.event
    def start_editing(self, customer: Customer):
        self.is_editing = True
        self.editing_customer_id = customer["customer_id"]
        self.name = customer["name"]
        self.phone_number = customer["phone_number"]
        self.email = customer["email"] or ""
        self.address = customer["address"] or ""
        self.notes = customer["notes"] or ""
        self.show_form = True

    def _reset_form_fields(self):
        self.name = ""
        self.phone_number = ""
        self.email = ""
        self.address = ""
        self.notes = ""
        self.editing_customer_id = None

    @rx.event
    def show_delete_confirmation(self, customer: Customer):
        self.show_delete_dialog = True
        self.customer_to_delete = customer

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.customer_to_delete = None

    @rx.event
    async def delete_customer(self):
        if self.customer_to_delete:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT COUNT(*) FROM orders WHERE customer_id = :customer_id"
                    ),
                    {"customer_id": self.customer_to_delete["customer_id"]},
                )
                order_count = result.scalar_one()
                if order_count > 0:
                    self.show_delete_dialog = False
                    yield rx.toast.error("Cannot delete customer with existing orders.")
                    return
                await session.execute(
                    text("DELETE FROM customers WHERE customer_id = :customer_id"),
                    {"customer_id": self.customer_to_delete["customer_id"]},
                )
                await session.commit()
            self.show_delete_dialog = False
            self.customer_to_delete = None
            yield rx.toast.success("Customer deleted successfully.")
            yield CustomerState.get_customers
            return
        self.show_delete_dialog = False
        yield rx.toast.error("No customer selected for deletion.")
        return


class BillingState(BaseState):
    orders_for_billing: list[OrderWithCustomerName] = []
    transactions: list[Transaction] = []
    invoices: list[Invoice] = []
    show_invoice_form: bool = False
    show_payment_form: bool = False
    selected_order_for_invoice: OrderWithCustomerName | None = None
    total_revenue: float = 0.0
    today_collection: float = 0.0
    pending_payments: float = 0.0
    month_revenue: float = 0.0

    @rx.event(background=True)
    async def get_orders_for_billing(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT o.*, c.name as customer_name 
FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
ORDER BY o.order_date DESC""")
            )
            rows = result.mappings().all()
            async with self:
                self.orders_for_billing = [
                    cast(OrderWithCustomerName, dict(row)) for row in rows
                ]


class MaterialState(BaseState):
    materials: list[Material] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_material_id: int | None = None
    show_delete_dialog: bool = False
    material_to_delete: Material | None = None
    material_name: str = ""
    material_type: str = "fabric"
    quantity_in_stock: float = 0.0
    unit: str = "meter"
    unit_price: float = 0.0
    reorder_level: float = 0.0
    supplier_name: str = ""
    supplier_contact: str = ""
    last_purchase_date: str = ""

    @rx.event(background=True)
    async def get_materials(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM materials ORDER BY material_name")
            )
            rows = result.mappings().all()
            materials = []
            for row in rows:
                material_dict = dict(row)
                material_dict["quantity_in_stock"] = float(
                    material_dict.get("quantity_in_stock") or 0.0
                )
                material_dict["unit_price"] = float(
                    material_dict.get("unit_price") or 0.0
                )
                material_dict["reorder_level"] = float(
                    material_dict.get("reorder_level") or 0.0
                )
                materials.append(cast(Material, material_dict))
            async with self:
                self.materials = materials

    @rx.var
    def filtered_materials(self) -> list[Material]:
        if not self.search_query.strip():
            return self.materials
        lower_query = self.search_query.lower()
        return [
            m
            for m in self.materials
            if lower_query in m["material_name"].lower()
            or lower_query in m["material_type"].lower()
        ]

    @rx.var
    def total_inventory_value(self) -> float:
        return sum(
            (
                float(m.get("quantity_in_stock", 0) or 0)
                * float(m.get("unit_price", 0) or 0)
                for m in self.materials
            )
        )

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        form_data["last_purchase_date"] = form_data["last_purchase_date"] or None
        form_data["supplier_name"] = form_data["supplier_name"] or None
        form_data["supplier_contact"] = form_data["supplier_contact"] or None
        if self.is_editing:
            return MaterialState.update_material(form_data)
        else:
            return MaterialState.add_material(form_data)

    @rx.event
    async def add_material(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO materials (material_name, material_type, quantity_in_stock, unit, unit_price, reorder_level, supplier_name, supplier_contact, last_purchase_date) 
                     VALUES (:material_name, :material_type, :quantity_in_stock, :unit, :unit_price, :reorder_level, :supplier_name, :supplier_contact, :last_purchase_date)"""),
                form_data,
            )
            await session.commit()
        self.show_form = False
        yield MaterialState.get_materials
        yield rx.toast.success("Material added successfully!")

    @rx.event
    async def update_material(self, form_data: dict):
        if self.editing_material_id is None:
            yield rx.toast.error("No material selected for editing.")
            return
        form_data["material_id"] = self.editing_material_id
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE materials SET material_name = :material_name, material_type = :material_type, 
                     quantity_in_stock = :quantity_in_stock, unit = :unit, unit_price = :unit_price, reorder_level = :reorder_level, 
                     supplier_name = :supplier_name, supplier_contact = :supplier_contact, last_purchase_date = :last_purchase_date
                     WHERE material_id = :material_id"""),
                form_data,
            )
            await session.commit()
        self.show_form = False
        yield MaterialState.get_materials
        yield rx.toast.success("Material updated successfully!")

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self.is_editing = False
        self._reset_form_fields()

    @rx.event
    def start_editing(self, material: Material):
        self.is_editing = True
        self.editing_material_id = material["material_id"]
        self.material_name = material["material_name"]
        self.material_type = material["material_type"]
        self.quantity_in_stock = float(material.get("quantity_in_stock") or 0.0)
        self.unit = material["unit"]
        self.unit_price = float(material.get("unit_price") or 0.0)
        self.reorder_level = float(material.get("reorder_level") or 0.0)
        self.supplier_name = material.get("supplier_name") or ""
        self.supplier_contact = material.get("supplier_contact") or ""
        purchase_date = material.get("last_purchase_date")
        self.last_purchase_date = str(purchase_date) if purchase_date else ""
        self.show_form = True

    def _reset_form_fields(self):
        self.is_editing = False
        self.editing_material_id = None
        self.material_name = ""
        self.material_type = "fabric"
        self.quantity_in_stock = 0.0
        self.unit = "meter"
        self.unit_price = 0.0
        self.reorder_level = 0.0
        self.supplier_name = ""
        self.supplier_contact = ""
        self.last_purchase_date = ""

    @rx.event
    def show_delete_confirmation(self, material: Material):
        self.show_delete_dialog = True
        self.material_to_delete = material

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.material_to_delete = None

    @rx.event
    async def delete_material(self):
        if self.material_to_delete:
            async with rx.asession() as session:
                await session.execute(
                    text("DELETE FROM materials WHERE material_id = :material_id"),
                    {"material_id": self.material_to_delete["material_id"]},
                )
                await session.commit()
            self.show_delete_dialog = False
            self.material_to_delete = None
            yield MaterialState.get_materials
            yield rx.toast.success("Material deleted successfully.")
        else:
            self.show_delete_dialog = False
            yield rx.toast.error("No material selected for deletion.")


class SidebarState(BaseState):
    """State for the sidebar component."""

    pass