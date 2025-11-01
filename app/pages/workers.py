import reflex as rx
from app.states.worker_state import WorkerState
from app.components.sidebar import sidebar, mobile_header
from app.components.worker_form import worker_form, delete_worker_dialog


def worker_card(worker: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(worker["worker_name"], class_name="font-bold text-lg"),
            rx.el.span(
                worker["role"].capitalize(),
                class_name="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-700",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(worker["phone_number"], class_name="text-sm text-gray-600"),
        rx.el.div(
            rx.el.button(
                "Edit",
                on_click=lambda: WorkerState.start_editing(worker),
                class_name="text-xs p-1",
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: WorkerState.show_delete_confirmation(worker),
                class_name="text-xs p-1 text-red-600",
            ),
            class_name="flex justify-end gap-2 mt-2",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border",
    )


def workers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1("Worker Management", class_name="text-3xl font-bold mb-6"),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search workers...",
                        on_change=WorkerState.set_search_query,
                        class_name="w-full md:w-72 p-2 border rounded-lg",
                    ),
                    rx.el.button(
                        "Add Worker",
                        on_click=WorkerState.toggle_form,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    WorkerState.is_loading,
                    rx.el.p("Loading workers..."),
                    rx.el.div(
                        rx.foreach(WorkerState.filtered_workers, worker_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
                    ),
                ),
                worker_form(),
                delete_worker_dialog(),
                class_name="p-4 md:p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )