import reflex as rx
from typing import cast
from app.models import WorkerTaskWithDetails
from sqlalchemy import text
import datetime


class TaskState(rx.State):
    is_loading: bool = False
    tasks: list[WorkerTaskWithDetails] = []
    search_query: str = ""

    @rx.event(background=True)
    async def get_tasks(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT 
                        wt.*,
                        w.worker_name,
                        c.name as customer_name,
                        o.cloth_type
                     FROM worker_tasks wt
                     JOIN workers w ON wt.worker_id = w.worker_id
                     JOIN orders o ON wt.order_id = o.order_id
                     JOIN customers c ON o.customer_id = c.customer_id
                     ORDER BY wt.assigned_date DESC""")
            )
            tasks = [
                cast(WorkerTaskWithDetails, dict(row))
                for row in result.mappings().all()
            ]
            async with self:
                self.tasks = tasks
                self.is_loading = False

    @rx.var
    def filtered_tasks(self) -> list[WorkerTaskWithDetails]:
        if not self.search_query.strip():
            return self.tasks
        lower_query = self.search_query.lower()
        return [
            t
            for t in self.tasks
            if lower_query in t["worker_name"].lower()
            or lower_query in t["customer_name"].lower()
            or str(t["order_id"]) == lower_query
        ]

    @rx.event(background=True)
    async def update_task_status(self, task_id: int, new_status: str):
        completed_at = datetime.datetime.now() if new_status == "completed" else None
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE worker_tasks 
                     SET status = :status, completed_date = :completed_at
                     WHERE task_id = :task_id"""),
                {
                    "status": new_status,
                    "task_id": task_id,
                    "completed_at": completed_at,
                },
            )
            await session.commit()
        async with self:
            yield TaskState.get_tasks
            yield rx.toast.info(
                f"Task #{task_id} status updated to {new_status.replace('_', ' ')}."
            )