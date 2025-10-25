import reflex as rx
from typing import cast, Any
from app.models import Supplier, Material
from sqlalchemy import text
import datetime


class PurchaseOrderItem(rx.Base):
    material_id: int
    material_name: str
    quantity: float
    unit_price: float


class PurchaseOrder(rx.Base):
    po_id: int
    supplier_name: str
    po_date: str
    expected_delivery_date: str | None
    status: str
    total_amount: float


class PurchaseOrderState(rx.State):
    purchase_orders: list[PurchaseOrder] = []
    available_suppliers: list[Supplier] = []
    available_materials: list[Material] = []
    low_stock_materials: list[Material] = []
    show_po_form: bool = False
    selected_supplier_id: str = ""
    expected_delivery_date: str = ""
    po_notes: str = ""
    po_items: list[PurchaseOrderItem] = []
    selected_material_id: str = ""
    item_quantity: float = 1.0
    item_unit_price: float = 0.0

    @rx.var
    def po_total(self) -> float:
        return sum((item.quantity * item.unit_price for item in self.po_items))

    @rx.event(background=True)
    async def get_purchase_orders(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT po.po_id, po.po_date, po.expected_delivery_date, po.status, po.total_amount, s.name as supplier_name 
                     FROM purchase_orders po
                     JOIN suppliers s ON po.supplier_id = s.supplier_id
                     ORDER BY po.po_date DESC""")
            )
            async with self:
                self.purchase_orders = [
                    cast(PurchaseOrder, dict(row)) for row in result.mappings().all()
                ]

    @rx.event(background=True)
    async def load_po_form_data(self):
        async with rx.asession() as session:
            suppliers_result = await session.execute(
                text("SELECT * FROM suppliers ORDER BY name")
            )
            materials_result = await session.execute(
                text(
                    "SELECT material_id, material_name, unit, unit_price FROM materials ORDER BY material_name"
                )
            )
            async with self:
                self.available_suppliers = [
                    cast(Supplier, dict(row))
                    for row in suppliers_result.mappings().all()
                ]
                self.available_materials = [
                    cast(Material, dict(row))
                    for row in materials_result.mappings().all()
                ]

    @rx.event(background=True)
    async def check_low_stock_materials(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM materials WHERE quantity_in_stock <= reorder_level")
            )
            async with self:
                self.low_stock_materials = [
                    cast(Material, dict(row)) for row in result.mappings().all()
                ]

    @rx.event
    def toggle_po_form(self):
        self.show_po_form = not self.show_po_form
        self._reset_po_form()
        if self.show_po_form:
            return PurchaseOrderState.load_po_form_data

    def _reset_po_form(self):
        self.selected_supplier_id = ""
        self.expected_delivery_date = ""
        self.po_notes = ""
        self.po_items = []
        self._reset_item_fields()

    def _reset_item_fields(self):
        self.selected_material_id = ""
        self.item_quantity = 1.0
        self.item_unit_price = 0.0

    @rx.event
    def on_material_select(self, material_id_str: str):
        self.selected_material_id = material_id_str
        material_id = int(material_id_str)
        material = next(
            (m for m in self.available_materials if m["material_id"] == material_id),
            None,
        )
        if material:
            self.item_unit_price = float(material.get("unit_price") or 0.0)

    @rx.event
    def add_po_item(self, form_data: dict):
        if not self.selected_material_id:
            return rx.toast.warning("Please select a material.")
        material_id = int(self.selected_material_id)
        material = next(
            (m for m in self.available_materials if m["material_id"] == material_id),
            None,
        )
        if not material:
            return rx.toast.error("Selected material not found.")
        quantity = float(form_data.get("item_quantity", 1.0))
        unit_price = float(form_data.get("item_unit_price", 0.0))
        new_item = PurchaseOrderItem(
            material_id=material_id,
            material_name=material["material_name"],
            quantity=quantity,
            unit_price=unit_price,
        )
        self.po_items.append(new_item)
        self._reset_item_fields()

    @rx.event
    def remove_po_item(self, index: int):
        if 0 <= index < len(self.po_items):
            self.po_items.pop(index)

    @rx.event(background=True)
    async def create_purchase_order(self, form_data: dict):
        if not self.selected_supplier_id or not self.po_items:
            yield rx.toast.error("Supplier and at least one item are required.")
            return
        expected_delivery_date = form_data.get("expected_delivery_date") or None
        async with rx.asession() as session:
            po_number = f"PO-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            po_result = await session.execute(
                text("""INSERT INTO purchase_orders (po_number, supplier_id, po_date, expected_delivery_date, status, total_amount, notes, created_at)
                     VALUES (:po_number, :supplier_id, :po_date, :expected_delivery_date, :status, :total_amount, :notes, :created_at)
                     RETURNING po_id"""),
                {
                    "po_number": po_number,
                    "supplier_id": int(self.selected_supplier_id),
                    "po_date": datetime.date.today(),
                    "expected_delivery_date": expected_delivery_date,
                    "status": "pending",
                    "total_amount": self.po_total,
                    "notes": self.po_notes,
                    "created_at": datetime.datetime.now(),
                },
            )
            new_po_id = po_result.scalar_one()
            for item in self.po_items:
                await session.execute(
                    text("""INSERT INTO purchase_order_items (po_id, material_id, quantity, unit_price, total_price)
                         VALUES (:po_id, :mat_id, :qty, :price, :total)"""),
                    {
                        "po_id": new_po_id,
                        "mat_id": item.material_id,
                        "qty": item.quantity,
                        "price": item.unit_price,
                        "total": item.quantity * item.unit_price,
                    },
                )
            await session.commit()
        async with self:
            self.show_po_form = False
        yield PurchaseOrderState.get_purchase_orders
        yield rx.toast.success(f"Purchase Order #{new_po_id} created successfully!")

    @rx.event
    async def update_po_status(self, po_id: int, new_status: str):
        if new_status == "received":
            yield PurchaseOrderState.receive_purchase_order(po_id)
        else:
            async with rx.asession() as session:
                await session.execute(
                    text(
                        "UPDATE purchase_orders SET status = :status WHERE po_id = :po_id"
                    ),
                    {"status": new_status, "po_id": po_id},
                )
                await session.commit()
            yield PurchaseOrderState.get_purchase_orders
            yield rx.toast.info(f"PO #{po_id} status updated to {new_status}.")

    @rx.event
    async def receive_purchase_order(self, po_id: int):
        async with rx.asession() as session, session.begin():
            items_result = await session.execute(
                text(
                    "SELECT material_id, quantity FROM purchase_order_items WHERE po_id = :po_id"
                ),
                {"po_id": po_id},
            )
            items = items_result.mappings().all()
            for item in items:
                await session.execute(
                    text(
                        "UPDATE materials SET quantity_in_stock = quantity_in_stock + :qty WHERE material_id = :mat_id"
                    ),
                    {"qty": item["quantity"], "mat_id": item["material_id"]},
                )
            await session.execute(
                text(
                    "UPDATE purchase_orders SET status = 'received', actual_delivery_date = :today WHERE po_id = :po_id"
                ),
                {"po_id": po_id, "today": datetime.date.today()},
            )
        yield PurchaseOrderState.get_purchase_orders
        yield rx.toast.success(f"PO #{po_id} received and stock updated.")

    @rx.event
    async def generate_auto_restock_po(self):
        yield rx.toast.info("Auto-restock PO generation is not yet implemented.")