import reflex as rx
from typing import cast, Any
from app.models import Measurement, Customer
from sqlalchemy import text
import datetime


class MeasurementWithCustomer(Measurement):
    customer_name: str


class MeasurementState(rx.State):
    measurements: list[MeasurementWithCustomer] = []
    available_customers: list[Customer] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_measurement_id: int | None = None
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

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self._reset_form_fields()
        if self.show_form:
            return MeasurementState.load_customers

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        self.show_form = False
        yield rx.toast.success("Measurement saved successfully!")
        yield MeasurementState.get_measurements