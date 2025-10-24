import reflex as rx
from app.states.worker_state import WorkerState
from app.components.sidebar import sidebar
from app.components.worker_form import worker_form, delete_worker_dialog


def status_badge(is_active: rx.Var[bool]) -> rx.Component:
    return rx.el.span(
        rx.cond(is_active, "Active", "Inactive"),
        class_name=rx.cond(
            is_active,
            "px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize bg-green-100 text-green-800",
            "px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize bg-red-100 text-red-800",
        ),
    )


def worker_row(worker: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            worker["worker_name"], class_name="px-6 py-4 font-medium text-gray-900"
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("phone", class_name="h-4 w-4 mr-2 text-gray-400"),
                rx.el.span(worker["phone_number"]),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 text-gray-600",
        ),
        rx.el.td(worker["role"].capitalize(), class_name="px-6 py-4 text-gray-600"),
        rx.el.td(
            f"₹{worker['salary'].to_string()}", class_name="px-6 py-4 text-gray-600"
        ),
        rx.el.td(status_badge(worker["active_status"]), class_name="px-6 py-4"),
        rx.el.td(
            worker["orders_assigned"].to_string(),
            class_name="px-6 py-4 text-center text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: WorkerState.start_editing(worker),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: WorkerState.show_delete_confirmation(worker),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def workers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Worker Management", class_name="text-3xl font-bold text-gray-800"
                ),
                rx.el.p(
                    "Manage all your staff and their assignments.",
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
                        placeholder="Search by name or phone...",
                        on_change=WorkerState.set_search_query,
                        class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                        default_value=WorkerState.search_query,
                    ),
                    class_name="relative",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-5 w-5"),
                    "Add Worker",
                    on_click=WorkerState.toggle_form,
                    class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Name",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Phone",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Role",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Salary",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Active Orders",
                                    class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(WorkerState.filtered_workers, worker_row)
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    rx.cond(
                        WorkerState.filtered_workers.length() == 0,
                        rx.el.div(
                            rx.icon("users", class_name="h-12 w-12 text-gray-400 mb-4"),
                            rx.el.h3(
                                "No Workers Found",
                                class_name="text-lg font-semibold text-gray-700",
                            ),
                            rx.el.p(
                                "Add your first worker to get started.",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="text-center py-16",
                        ),
                        None,
                    ),
                    class_name="overflow-hidden border border-gray-200 rounded-xl",
                ),
                class_name="bg-white p-6 rounded-xl shadow-sm",
            ),
            worker_form(),
            delete_worker_dialog(),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )