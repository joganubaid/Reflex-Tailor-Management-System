import reflex as rx


def loading_spinner(message: str) -> rx.Component:
    """A centered loading spinner with a message."""
    return rx.el.div(
        rx.el.div(
            rx.spinner(size="3"),
            rx.el.p(message, class_name="mt-4 text-lg font-semibold text-gray-600"),
            class_name="flex flex-col items-center justify-center p-8 bg-white rounded-xl shadow-sm",
        ),
        class_name="fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center z-50",
    )