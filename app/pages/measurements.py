import reflex as rx
from app.states.measurement_state import MeasurementState
from app.components.sidebar import sidebar, mobile_header


def _form_label(text: str) -> rx.Component:
    return rx.el.label(
        text, class_name="block text-sm font-semibold text-gray-700 mb-2"
    )


def _form_input(**props) -> rx.Component:
    return rx.el.input(
        **props,
        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
    )


def _form_select(*children, **props) -> rx.Component:
    return rx.el.select(
        *children,
        **props,
        class_name="w-full p-3 bg-white border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500",
    )


def measurement_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(
                        MeasurementState.is_editing,
                        "Edit Measurement",
                        "Add New Measurement",
                    ),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    _form_label("Customer"),
                    _form_select(
                        rx.el.option("Select a customer", value="", disabled=True),
                        rx.foreach(
                            MeasurementState.available_customers,
                            lambda customer: rx.el.option(
                                f"{customer['name']} ({customer['phone_number']})",
                                value=customer["customer_id"].to_string(),
                            ),
                        ),
                        name="customer_id",
                        value=MeasurementState.selected_customer_id,
                        on_change=MeasurementState.set_selected_customer_id,
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    _form_label("Cloth Type"),
                    _form_select(
                        rx.el.option("Shirt", value="shirt"),
                        rx.el.option("Pant", value="pant"),
                        rx.el.option("Suit", value="suit"),
                        rx.el.option("Blouse", value="blouse"),
                        rx.el.option("Dress", value="dress"),
                        name="cloth_type",
                        value=MeasurementState.selected_cloth_type,
                        on_change=MeasurementState.set_selected_cloth_type,
                    ),
                    class_name="mb-4",
                ),
                rx.el.h3(
                    "Measurements (in inches)",
                    class_name="text-lg font-bold text-gray-800 mb-4 border-t pt-6 mt-6",
                ),
                rx.el.div(
                    rx.el.div(
                        _form_label("Chest"),
                        _form_input(
                            name="chest",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.chest,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Waist"),
                        _form_input(
                            name="waist",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.waist,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Hip"),
                        _form_input(
                            name="hip",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.hip,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Shoulder Width"),
                        _form_input(
                            name="shoulder_width",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.shoulder_width,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Sleeve Length"),
                        _form_input(
                            name="sleeve_length",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.sleeve_length,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Shirt Length"),
                        _form_input(
                            name="shirt_length",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.shirt_length,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Pant Length"),
                        _form_input(
                            name="pant_length",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.pant_length,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Inseam"),
                        _form_input(
                            name="inseam",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.inseam,
                        ),
                    ),
                    rx.el.div(
                        _form_label("Neck"),
                        _form_input(
                            name="neck",
                            type="number",
                            step="0.01",
                            default_value=MeasurementState.neck,
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=MeasurementState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            MeasurementState.is_editing,
                            "Save Changes",
                            "Save Measurement",
                        ),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-semibold",
                    ),
                    class_name="flex justify-end gap-4 mt-8",
                ),
                on_submit=MeasurementState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[48rem] max-w-[95vw]",
        ),
        open=MeasurementState.show_form,
        on_open_change=MeasurementState.set_show_form,
    )


def delete_measurement_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Confirm Deletion", class_name="text-xl font-bold text-gray-800"
            ),
            rx.dialog.description(
                "Are you sure you want to delete this measurement? This action cannot be undone.",
                class_name="my-4 text-gray-600",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=MeasurementState.cancel_delete,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                rx.el.button(
                    "Delete",
                    on_click=MeasurementState.delete_measurement,
                    class_name="py-2 px-4 rounded-lg bg-red-600 text-white hover:bg-red-700 font-semibold",
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-100 w-96",
        ),
        open=MeasurementState.show_delete_dialog,
        on_open_change=MeasurementState.set_show_delete_dialog,
    )


def measurement_row(measurement: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            measurement["customer_name"],
            class_name="px-6 py-4 font-medium text-gray-900",
        ),
        rx.el.td(measurement["cloth_type"].capitalize(), class_name="px-6 py-4"),
        rx.el.td(measurement["chest"].to_string(), class_name="px-6 py-4 text-center"),
        rx.el.td(measurement["waist"].to_string(), class_name="px-6 py-4 text-center"),
        rx.el.td(measurement["hip"].to_string(), class_name="px-6 py-4 text-center"),
        rx.el.td(
            measurement["shoulder_width"].to_string(),
            class_name="px-6 py-4 text-center",
        ),
        rx.el.td(
            measurement["sleeve_length"].to_string(), class_name="px-6 py-4 text-center"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: MeasurementState.start_editing(measurement),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: MeasurementState.show_delete_confirmation(
                        measurement["measurement_id"]
                    ),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-2",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50 transition-colors duration-150",
    )


def measurement_card(measurement: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                measurement["customer_name"],
                class_name="font-bold text-lg text-gray-800",
            ),
            rx.el.p(
                measurement["cloth_type"].capitalize(),
                class_name="text-sm font-medium text-purple-600",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.p(
                f"Measured: {measurement['measurement_date'].to_string().split('T')[0]}",
                class_name="text-xs text-gray-500 mt-2",
            ),
            class_name="border-b pb-3 mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Chest", class_name="text-xs text-gray-500"),
                rx.el.p(measurement["chest"].to_string(), class_name="font-semibold"),
            ),
            rx.el.div(
                rx.el.p("Waist", class_name="text-xs text-gray-500"),
                rx.el.p(measurement["waist"].to_string(), class_name="font-semibold"),
            ),
            rx.el.div(
                rx.el.p("Hip", class_name="text-xs text-gray-500"),
                rx.el.p(measurement["hip"].to_string(), class_name="font-semibold"),
            ),
            rx.el.div(
                rx.el.p("Shoulder", class_name="text-xs text-gray-500"),
                rx.el.p(
                    measurement["shoulder_width"].to_string(),
                    class_name="font-semibold",
                ),
            ),
            rx.el.div(
                rx.el.p("Sleeve", class_name="text-xs text-gray-500"),
                rx.el.p(
                    measurement["sleeve_length"].to_string(), class_name="font-semibold"
                ),
            ),
            class_name="grid grid-cols-3 gap-y-2 text-center text-sm",
        ),
        rx.el.div(
            rx.el.div(),
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: MeasurementState.start_editing(measurement),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: MeasurementState.show_delete_confirmation(
                        measurement["measurement_id"]
                    ),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center gap-2 justify-end",
            ),
            class_name="flex justify-between items-center mt-4 pt-3 border-t",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def measurements_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Measurements", class_name="text-3xl font-bold text-gray-800"
                    ),
                    rx.el.p(
                        "Manage all customer measurements.",
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
                            placeholder="Search by customer or cloth type...",
                            type="search",
                            on_change=MeasurementState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            default_value=MeasurementState.search_query,
                        ),
                        class_name="relative",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Add Measurement",
                        on_click=MeasurementState.toggle_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(
                            MeasurementState.filtered_measurements, measurement_card
                        ),
                        class_name="grid grid-cols-1 gap-4 md:hidden",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Customer",
                                            scope="col",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Cloth Type",
                                            scope="col",
                                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Chest",
                                            scope="col",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Waist",
                                            scope="col",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Hip",
                                            scope="col",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Shoulder",
                                            scope="col",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Sleeve",
                                            scope="col",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            scope="col",
                                            class_name="px-6 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        MeasurementState.filtered_measurements,
                                        measurement_row,
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        class_name="hidden md:block overflow-x-auto border border-gray-200 rounded-xl",
                    ),
                    rx.cond(
                        MeasurementState.filtered_measurements.length() == 0,
                        rx.el.div(
                            rx.icon("ruler", class_name="h-12 w-12 text-gray-400 mb-4"),
                            rx.el.h3(
                                "No Measurements Found",
                                class_name="text-lg font-semibold text-gray-700",
                            ),
                            rx.el.p(
                                "Add your first measurement to get started.",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="text-center py-16 bg-white rounded-xl shadow-sm",
                        ),
                        None,
                    ),
                    class_name="md:bg-white md:p-6 rounded-xl shadow-sm",
                ),
                measurement_form(),
                delete_measurement_dialog(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )