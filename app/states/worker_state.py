import reflex as rx
from typing import cast
from app.models import Worker
from sqlalchemy import text
import datetime


class WorkerState(rx.State):
    workers: list[Worker] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_worker_id: int | None = None
    show_delete_dialog: bool = False
    worker_to_delete: Worker | None = None
    worker_name: str = ""
    phone_number: str = ""
    role: str = "tailor"
    salary: float = 0.0
    active_status: bool = True

    @rx.event(background=True)
    async def get_workers(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT w.*, COUNT(o.order_id) AS orders_assigned
                     FROM workers w
                     LEFT JOIN orders o ON w.worker_id = o.assigned_worker
                     GROUP BY w.worker_id
                     ORDER BY w.worker_name""")
            )
            rows = result.mappings().all()
            async with self:
                self.workers = [cast(Worker, dict(row)) for row in rows]

    @rx.var
    def filtered_workers(self) -> list[Worker]:
        if not self.search_query.strip():
            return self.workers
        lower_query = self.search_query.lower()
        return [
            w
            for w in self.workers
            if lower_query in w["worker_name"].lower()
            or lower_query in w["phone_number"]
        ]

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        form_data["active_status"] = form_data.get("active_status") == "on"
        if self.is_editing:
            return WorkerState.update_worker(form_data)
        else:
            return WorkerState.add_worker(form_data)

    @rx.event
    async def add_worker(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO workers (worker_name, phone_number, role, salary, joining_date, active_status) 
                     VALUES (:worker_name, :phone_number, :role, :salary, :joining_date, :active_status)"""),
                {
                    "worker_name": form_data["worker_name"],
                    "phone_number": form_data["phone_number"],
                    "role": form_data["role"],
                    "salary": float(form_data["salary"]),
                    "joining_date": datetime.date.today(),
                    "active_status": form_data.get("active_status", True),
                },
            )
            await session.commit()
        self.show_form = False
        yield rx.toast.success("Worker added successfully!")
        yield WorkerState.get_workers
        return

    @rx.event
    async def update_worker(self, form_data: dict):
        if self.editing_worker_id is None:
            yield rx.toast.error("No worker selected for editing.")
            return
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE workers SET worker_name = :worker_name, phone_number = :phone_number, 
                     role = :role, salary = :salary, active_status = :active_status
                     WHERE worker_id = :worker_id"""),
                {
                    "worker_name": form_data["worker_name"],
                    "phone_number": form_data["phone_number"],
                    "role": form_data["role"],
                    "salary": float(form_data["salary"]),
                    "active_status": form_data.get("active_status", True),
                    "worker_id": self.editing_worker_id,
                },
            )
            await session.commit()
        self.show_form = False
        yield rx.toast.success("Worker updated successfully!")
        yield WorkerState.get_workers
        return

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self.is_editing = False
        self._reset_form_fields()

    @rx.event
    def start_editing(self, worker: Worker):
        self.is_editing = True
        self.editing_worker_id = worker["worker_id"]
        self.worker_name = worker["worker_name"]
        self.phone_number = worker["phone_number"]
        self.role = worker["role"]
        self.salary = worker["salary"]
        self.active_status = worker["active_status"]
        self.show_form = True

    def _reset_form_fields(self):
        self.is_editing = False
        self.editing_worker_id = None
        self.worker_name = ""
        self.phone_number = ""
        self.role = "tailor"
        self.salary = 0.0
        self.active_status = True

    @rx.event
    def show_delete_confirmation(self, worker: Worker):
        self.show_delete_dialog = True
        self.worker_to_delete = worker

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.worker_to_delete = None

    @rx.event
    async def delete_worker(self):
        if self.worker_to_delete:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT COUNT(*) FROM orders WHERE assigned_worker = :worker_id AND status NOT IN ('delivered', 'cancelled')"
                    ),
                    {"worker_id": self.worker_to_delete["worker_id"]},
                )
                active_order_count = result.scalar_one()
                if active_order_count > 0:
                    self.show_delete_dialog = False
                    yield rx.toast.error(
                        "Cannot delete worker with active orders assigned."
                    )
                    return
                await session.execute(
                    text("DELETE FROM workers WHERE worker_id = :worker_id"),
                    {"worker_id": self.worker_to_delete["worker_id"]},
                )
                await session.commit()
            self.show_delete_dialog = False
            self.worker_to_delete = None
            yield rx.toast.success("Worker deleted successfully.")
            yield WorkerState.get_workers
            return
        self.show_delete_dialog = False
        yield rx.toast.error("No worker selected for deletion.")
        return