import reflex as rx
from typing import cast, Any
from app.models import Measurement, Customer
from sqlalchemy import text
import datetime


class MeasurementWithCustomer(Measurement):
    customer_name: str


class MeasurementState(rx.State):
    is_loading: bool = False
    measurements: list[MeasurementWithCustomer] = []
    available_customers: list[Customer] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_measurement_id: int | None = None
    show_delete_dialog: bool = False
    measurement_to_delete_id: int | None = None
    selected_customer_id: str = ""
    selected_cloth_type: str = "shirt"
    chest: str = ""
    waist: str = ""
    hip: str = ""
    shoulder_width: str = ""
    sleeve_length: str = ""
    shirt_length: str = ""
    pant_length: str = ""
    inseam: str = ""
    neck: str = ""
    measurement_date: str = ""

    @rx.event(background=True)
    async def get_measurements(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            measurement_result = await session.execute(
                text("""SELECT m.*, c.name as customer_name
                     FROM measurements m
                     JOIN customers c ON m.customer_id = c.customer_id
                     ORDER BY m.measurement_date DESC""")
            )
            measurements = [
                cast(MeasurementWithCustomer, dict(row))
                for row in measurement_result.mappings().all()
            ]
            customer_result = await session.execute(
                text(
                    "SELECT customer_id, name, phone_number FROM customers ORDER BY name"
                )
            )
            customers = [
                cast(Customer, dict(row)) for row in customer_result.mappings().all()
            ]
            async with self:
                self.measurements = measurements
                self.available_customers = customers
                self.is_loading = False

    @rx.event(background=True)
    async def load_customers(self):
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

    @rx.var
    def filtered_measurements(self) -> list[MeasurementWithCustomer]:
        if not self.search_query.strip():
            return self.measurements
        lower_query = self.search_query.lower()
        return [
            m
            for m in self.measurements
            if lower_query in m["customer_name"].lower()
            or lower_query in m["cloth_type"].lower()
        ]

    def _reset_form_fields(self):
        self.is_editing = False
        self.editing_measurement_id = None
        self.selected_customer_id = ""
        self.selected_cloth_type = "shirt"
        self.chest = ""
        self.waist = ""
        self.hip = ""
        self.shoulder_width = ""
        self.sleeve_length = ""
        self.shirt_length = ""
        self.pant_length = ""
        self.inseam = ""
        self.neck = ""
        self.measurement_date = datetime.date.today().isoformat()
        self.measurement_to_delete_id = None

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self._reset_form_fields()
        if self.show_form:
            return MeasurementState.load_customers

    @rx.event
    def start_editing(self, measurement: dict):
        self.is_editing = True
        self.editing_measurement_id = measurement["measurement_id"]
        self.selected_customer_id = str(measurement["customer_id"])
        self.selected_cloth_type = measurement["cloth_type"]
        self.chest = str(measurement.get("chest") or "")
        self.waist = str(measurement.get("waist") or "")
        self.hip = str(measurement.get("hip") or "")
        self.shoulder_width = str(measurement.get("shoulder_width") or "")
        self.sleeve_length = str(measurement.get("sleeve_length") or "")
        self.shirt_length = str(measurement.get("shirt_length") or "")
        self.pant_length = str(measurement.get("pant_length") or "")
        self.inseam = str(measurement.get("inseam") or "")
        self.neck = str(measurement.get("neck") or "")
        self.show_form = True

    @rx.event(background=True)
    async def handle_form_submit(self, form_data: dict):
        async with self:
            is_editing = self.is_editing
        if is_editing:
            yield MeasurementState.update_measurement(form_data)
        else:
            yield MeasurementState.add_measurement(form_data)

    def _parse_measurement_form_data(self, form_data: dict) -> dict:
        import logging

        parsed_data = {}
        for key, value in form_data.items():
            if key in ["customer_id", "cloth_type"]:
                parsed_data[key] = value
            elif value:
                try:
                    parsed_data[key] = float(value)
                except (ValueError, TypeError) as e:
                    logging.exception(f"Error parsing measurement value: {value}: {e}")
                    parsed_data[key] = None
            else:
                parsed_data[key] = None
        parsed_data["measurement_date"] = datetime.date.today()
        return parsed_data

    @rx.event(background=True)
    async def add_measurement(self, form_data: dict):
        parsed_data = self._parse_measurement_form_data(form_data)
        if not parsed_data.get("customer_id"):
            yield rx.toast.error("Customer is required.")
            return
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO measurements (customer_id, cloth_type, chest, waist, hip, shoulder_width, sleeve_length, shirt_length, pant_length, inseam, neck, measurement_date)
                     VALUES (:customer_id, :cloth_type, :chest, :waist, :hip, :shoulder_width, :sleeve_length, :shirt_length, :pant_length, :inseam, :neck, :measurement_date)"""),
                parsed_data,
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield rx.toast.success("Measurement saved successfully!")
        yield MeasurementState.get_measurements

    @rx.event(background=True)
    async def update_measurement(self, form_data: dict):
        async with self:
            editing_id = self.editing_measurement_id
        if not editing_id:
            yield rx.toast.error("No measurement selected for editing.")
            return
        parsed_data = self._parse_measurement_form_data(form_data)
        parsed_data["measurement_id"] = editing_id
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE measurements SET 
                        customer_id = :customer_id, cloth_type = :cloth_type, chest = :chest, waist = :waist, 
                        hip = :hip, shoulder_width = :shoulder_width, sleeve_length = :sleeve_length, 
                        shirt_length = :shirt_length, pant_length = :pant_length, inseam = :inseam, neck = :neck
                     WHERE measurement_id = :measurement_id"""),
                parsed_data,
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield rx.toast.success("Measurement updated successfully!")
        yield MeasurementState.get_measurements

    @rx.event
    def show_delete_confirmation(self, measurement_id: int):
        self.show_delete_dialog = True
        self.measurement_to_delete_id = measurement_id

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.measurement_to_delete_id = None

    @rx.event(background=True)
    async def delete_measurement(self):
        async with self:
            delete_id = self.measurement_to_delete_id
        if not delete_id:
            yield rx.toast.error("No measurement selected for deletion.")
            return
        async with rx.asession() as session:
            await session.execute(
                text("DELETE FROM measurements WHERE measurement_id = :measurement_id"),
                {"measurement_id": delete_id},
            )
            await session.commit()
        async with self:
            self.show_delete_dialog = False
        yield rx.toast.success("Measurement deleted successfully.")
        yield MeasurementState.get_measurements