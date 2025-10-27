import reflex as rx
from app.states.task_state import TaskState
from app.components.sidebar import sidebar, mobile_header

STATUS_COLORS = {
    "pending": "bg-yellow-100 text-yellow-800",
    "in_progress": "bg-blue-100 text-blue-800",
    "completed": "bg-green-100 text-green-800",
}


def status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status.replace("_", " "),
        class_name=rx.match(
            status.lower(),
            ("pending", STATUS_COLORS["pending"] + base_classes),
            ("in_progress", STATUS_COLORS["in_progress"] + base_classes),
            ("completed", STATUS_COLORS["completed"] + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def task_card(task: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"Order #{task['order_id']}", class_name="font-bold text-gray-800"
                ),
                rx.el.p(task["customer_name"], class_name="text-sm text-gray-600"),
            ),
            status_badge(task["status"]),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.div(
            rx.el.p(task["worker_name"], class_name="font-semibold"),
            rx.el.p(
                task["task_type"].capitalize(), class_name="text-sm text-purple-600"
            ),
            class_name="mt-2 pt-2 border-t",
        ),
        rx.el.div(
            rx.el.p(
                f"Due: {rx.cond(task['due_date'], task['due_date'].to_string().split('T')[0], 'N/A')}",
                class_name="text-xs text-gray-500",
            ),
            rx.el.div(
                rx.cond(
                    task["status"] == "pending",
                    rx.el.button(
                        "Start",
                        on_click=lambda: TaskState.update_task_status(
                            task["task_id"], "in_progress"
                        ),
                        class_name="px-3 py-1.5 text-xs bg-blue-100 text-blue-700 rounded-md font-semibold",
                    ),
                    None,
                ),
                rx.cond(
                    task["status"] == "in_progress",
                    rx.el.button(
                        "Complete",
                        on_click=lambda: TaskState.update_task_status(
                            task["task_id"], "completed"
                        ),
                        class_name="px-3 py-1.5 text-xs bg-green-100 text-green-700 rounded-md font-semibold",
                    ),
                    None,
                ),
                class_name="flex gap-2 justify-end",
            ),
            class_name="flex justify-between items-center mt-3 pt-3 border-t",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def task_row(task: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(f"#{task['order_id']}", class_name="px-6 py-4 font-medium"),
        rx.el.td(task["customer_name"], class_name="px-6 py-4"),
        rx.el.td(task["worker_name"], class_name="px-6 py-4"),
        rx.el.td(task["task_type"].capitalize(), class_name="px-6 py-4"),
        rx.el.td(status_badge(task["status"]), class_name="px-6 py-4"),
        rx.el.td(
            rx.cond(
                task["due_date"], task["due_date"].to_string().split("T")[0], "N/A"
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Start",
                    on_click=lambda: TaskState.update_task_status(
                        task["task_id"], "in_progress"
                    ),
                    class_name=rx.cond(
                        task["status"] == "pending",
                        "px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded",
                        "hidden",
                    ),
                ),
                rx.el.button(
                    "Complete",
                    on_click=lambda: TaskState.update_task_status(
                        task["task_id"], "completed"
                    ),
                    class_name=rx.cond(
                        task["status"] == "in_progress",
                        "px-2 py-1 text-xs bg-green-100 text-green-700 rounded",
                        "hidden",
                    ),
                ),
                class_name="flex gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def productivity_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Worker Productivity",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Assign and track tasks for all workers.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search by worker, customer, or order ID...",
                            on_change=TaskState.set_search_query,
                            class_name="w-full md:w-96 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500",
                        ),
                        class_name="relative",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(TaskState.filtered_tasks, task_card),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:hidden",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Order ID",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Customer",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Worker",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Task",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Due Date",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(TaskState.filtered_tasks, task_row)
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            TaskState.filtered_tasks.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "clipboard-check",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "No Tasks Found", class_name="text-lg font-semibold"
                                ),
                                rx.el.p(
                                    "Tasks assigned to workers will appear here.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="hidden md:block overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="md:bg-white md:p-4 md:p-6 rounded-xl shadow-sm",
                ),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )