import reflex as rx
from app.states.worker_state import WorkerState


def worker_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(WorkerState.is_editing, "Edit Worker", "Add New Worker"),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Worker Name",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="worker_name",
                        default_value=WorkerState.worker_name,
                        required=True,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone Number",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.input(
                        name="phone_number",
                        default_value=WorkerState.phone_number,
                        required=True,
                        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Role",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.el.option("Tailor", value="tailor"),
                            rx.el.option("Cutter", value="cutter"),
                            rx.el.option("Helper", value="helper"),
                            name="role",
                            value=WorkerState.role,
                            on_change=WorkerState.set_role,
                            class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Salary",
                            class_name="block text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="salary",
                            type="number",
                            default_value=WorkerState.salary.to_string(),
                            required=True,
                            class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Active Status",
                        class_name="flex items-center gap-2 text-sm font-semibold text-gray-700",
                    ),
                    rx.el.input(
                        type="checkbox",
                        name="active_status",
                        checked=WorkerState.active_status,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=WorkerState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(WorkerState.is_editing, "Save Changes", "Add Worker"),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4",
                ),
                on_submit=WorkerState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[32rem] max-w-[90vw]",
        ),
        open=WorkerState.show_form,
        on_open_change=WorkerState.set_show_form,
    )


def delete_worker_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirm Deletion", class_name="text-xl font-bold text-gray-800"
            ),
            rx.dialog.description(
                "Are you sure you want to delete this worker? This action cannot be undone.",
                class_name="my-4 text-gray-600",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=WorkerState.cancel_delete,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Delete",
                        on_click=WorkerState.delete_worker,
                        class_name="py-2 px-4 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold",
                    )
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-100 w-96",
        ),
        open=WorkerState.show_delete_dialog,
        on_open_change=WorkerState.set_show_delete_dialog,
    )