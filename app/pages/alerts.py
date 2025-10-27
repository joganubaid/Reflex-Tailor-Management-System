import reflex as rx
from app.states.alert_state import AlertState, AlertSetting
from app.components.sidebar import sidebar


def alert_setting_row(setting: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            setting["alert_type"].replace("_", " ").capitalize(),
            class_name="px-6 py-4 font-medium text-gray-900",
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(setting["enabled"], "Enabled", "Disabled"),
                class_name=rx.cond(
                    setting["enabled"],
                    "px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-700",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-700",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.cond(
                setting["threshold_value"] > 0,
                setting["threshold_value"].to_string(),
                "N/A",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(setting["notification_method"].upper(), class_name="px-6 py-4"),
        rx.el.td(setting["recipients"], class_name="px-6 py-4 text-sm text-gray-600"),
        rx.el.td(
            rx.el.button(
                rx.icon("copy", class_name="h-4 w-4"),
                on_click=lambda: AlertState.start_editing(setting),
                class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
            ),
            class_name="px-6 py-4 text-center",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def alert_history_row(history: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            history["alert_type"].replace("_", " ").capitalize(),
            class_name="px-6 py-4 font-medium",
        ),
        rx.el.td(history["message"], class_name="px-6 py-4 text-sm"),
        rx.el.td(history["severity"].capitalize(), class_name="px-6 py-4"),
        rx.el.td(
            history["triggered_at"].to_string().split("T")[0], class_name="px-6 py-4"
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def edit_alert_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    "Edit Alert Setting", class_name="text-2xl font-bold mb-4"
                ),
                rx.el.p(
                    AlertState.editing_setting["alert_type"]
                    .replace("_", " ")
                    .capitalize(),
                    class_name="text-gray-600 mb-6",
                ),
                rx.el.div(
                    rx.el.label("Enabled", class_name="flex items-center gap-2"),
                    rx.el.input(
                        type="checkbox",
                        name="enabled",
                        checked=AlertState.editing_setting["enabled"],
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Threshold Value", class_name="block text-sm font-semibold"
                    ),
                    rx.el.input(
                        name="threshold_value",
                        default_value=AlertState.editing_setting[
                            "threshold_value"
                        ].to_string(),
                        type="number",
                        class_name="w-full p-2 border rounded mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Notification Method", class_name="block text-sm font-semibold"
                    ),
                    rx.el.select(
                        rx.el.option("SMS", value="sms"),
                        rx.el.option("Email", value="email"),
                        rx.el.option("Both", value="both"),
                        name="notification_method",
                        value=AlertState.editing_setting["notification_method"],
                        class_name="w-full p-2 border rounded mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Recipients (comma-separated)",
                        class_name="block text-sm font-semibold",
                    ),
                    rx.el.textarea(
                        name="recipients",
                        default_value=AlertState.editing_setting["recipients"],
                        class_name="w-full p-2 border rounded mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            on_click=AlertState.cancel_editing,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 font-semibold",
                        )
                    ),
                    rx.el.button(
                        "Save Changes",
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white font-semibold",
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                on_submit=AlertState.save_setting,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg w-[32rem]",
        ),
        open=AlertState.show_edit_dialog,
        on_open_change=lambda open: AlertState.cancel_editing(),
    )


def alerts_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Alerts & Automation", class_name="text-3xl font-bold text-gray-800"
                ),
                rx.el.p(
                    "Configure smart alerts and view system notifications.",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Alert Settings",
                    class_name="text-xl font-semibold text-gray-700 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Alert Type",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Threshold",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Method",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Recipients",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Action",
                                    class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(AlertState.alert_settings, alert_setting_row)
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="overflow-hidden border border-gray-200 rounded-xl",
                ),
                class_name="bg-white p-6 rounded-xl shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Alert History",
                    class_name="text-xl font-semibold text-gray-700 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Alert Type",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Message",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Severity",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Triggered At",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(AlertState.alert_history, alert_history_row)
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="overflow-hidden border border-gray-200 rounded-xl",
                ),
                class_name="bg-white p-6 rounded-xl shadow-sm",
            ),
            edit_alert_dialog(),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )