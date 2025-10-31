import reflex as rx
from typing import cast
from app.models import Supplier
from sqlalchemy import text
import datetime


class SupplierState(rx.State):
    is_loading: bool = False
    suppliers: list[Supplier] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_supplier_id: int | None = None
    show_delete_dialog: bool = False
    supplier_to_delete: Supplier | None = None
    name: str = ""
    contact: str = ""
    email: str = ""
    address: str = ""
    rating: float = 0.0
    notes: str = ""

    @rx.event(background=True)
    async def get_suppliers(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT s.*, COUNT(ms.material_id) as materials_count
                     FROM suppliers s
                     LEFT JOIN material_suppliers ms ON s.supplier_id = ms.supplier_id
                     GROUP BY s.supplier_id
                     ORDER BY s.name""")
            )
            rows = result.mappings().all()
            async with self:
                self.suppliers = [cast(Supplier, dict(row)) for row in rows]
                self.is_loading = False

    @rx.var
    def filtered_suppliers(self) -> list[Supplier]:
        if not self.search_query.strip():
            return self.suppliers
        lower_query = self.search_query.lower()
        return [
            s
            for s in self.suppliers
            if lower_query in s["name"].lower() or lower_query in s["contact"]
        ]

    def _reset_form_fields(self):
        self.is_editing = False
        self.editing_supplier_id = None
        self.name = ""
        self.contact = ""
        self.email = ""
        self.address = ""
        self.rating = 0.0
        self.notes = ""

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self._reset_form_fields()

    @rx.event
    def start_editing(self, supplier: Supplier):
        self.is_editing = True
        self.editing_supplier_id = supplier["supplier_id"]
        self.name = supplier["name"]
        self.contact = supplier["contact"]
        self.email = supplier.get("email") or ""
        self.address = supplier.get("address") or ""
        self.rating = float(supplier.get("rating") or 0.0)
        self.notes = supplier.get("notes") or ""
        self.show_form = True

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        if self.is_editing:
            await self.update_supplier(form_data)
        else:
            await self.add_supplier(form_data)

    @rx.event(background=True)
    async def add_supplier(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO suppliers (name, contact, email, address, rating, notes, registration_date)
                     VALUES (:name, :contact, :email, :address, :rating, :notes, :registration_date)"""),
                {
                    "name": form_data["name"],
                    "contact": form_data["contact"],
                    "email": form_data.get("email"),
                    "address": form_data.get("address"),
                    "rating": float(form_data.get("rating", 0.0)),
                    "notes": form_data.get("notes"),
                    "registration_date": datetime.date.today(),
                },
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield SupplierState.get_suppliers
        yield rx.toast.success("Supplier added successfully!")

    @rx.event(background=True)
    async def update_supplier(self, form_data: dict):
        if not self.editing_supplier_id:
            return
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE suppliers SET name=:name, contact=:contact, email=:email, 
                     address=:address, rating=:rating, notes=:notes
                     WHERE supplier_id=:supplier_id"""),
                {
                    "name": form_data["name"],
                    "contact": form_data["contact"],
                    "email": form_data.get("email"),
                    "address": form_data.get("address"),
                    "rating": float(form_data.get("rating", 0.0)),
                    "notes": form_data.get("notes"),
                    "supplier_id": self.editing_supplier_id,
                },
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield SupplierState.get_suppliers
        yield rx.toast.success("Supplier updated successfully!")

    @rx.event
    def show_delete_confirmation(self, supplier: Supplier):
        self.show_delete_dialog = True
        self.supplier_to_delete = supplier

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.supplier_to_delete = None

    @rx.event(background=True)
    async def delete_supplier(self):
        if not self.supplier_to_delete:
            return
        supplier_id = self.supplier_to_delete["supplier_id"]
        async with rx.asession() as session:
            await session.execute(
                text("DELETE FROM material_suppliers WHERE supplier_id = :supplier_id"),
                {"supplier_id": supplier_id},
            )
            await session.execute(
                text("DELETE FROM suppliers WHERE supplier_id = :supplier_id"),
                {"supplier_id": supplier_id},
            )
            await session.commit()
        async with self:
            self.show_delete_dialog = False
            self.supplier_to_delete = None
        yield SupplierState.get_suppliers
        yield rx.toast.success("Supplier deleted successfully.")