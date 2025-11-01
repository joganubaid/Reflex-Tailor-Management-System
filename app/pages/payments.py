import reflex as rx
from app.states.payment_state import PaymentState
from app.components.sidebar import sidebar, mobile_header
from app.components.payment_form import payment_installment_form


def installment_card(installment: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(f"Order #{installment['order_id']}", class_name="font-bold"),
            rx.el.p(installment["customer_name"], class_name="text-sm text-gray-600"),
        ),
        rx.el.div(
            rx.el.p(
                f"₹{installment['amount']}", class_name="font-bold text-xl text-red-600"
            ),
            rx.el.p(
                f"Due: {installment['due_date'].to_string().split('T')[0]}",
                class_name="text-xs",
            ),
            class_name="text-right",
        ),
        class_name="flex justify-between items-start bg-white p-4 rounded-xl shadow-sm border",
    )


def payments_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1("Payment Management", class_name="text-3xl font-bold mb-6"),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search by customer or order ID...",
                        on_change=PaymentState.set_search_query,
                        class_name="w-full md:w-72 p-2 border rounded-lg",
                    ),
                    rx.el.button(
                        "Add Installment",
                        on_click=PaymentState.toggle_installment_form,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    PaymentState.is_loading,
                    rx.el.p("Loading payments..."),
                    rx.el.div(
                        rx.foreach(
                            PaymentState.filtered_installments, installment_card
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                ),
                payment_installment_form(),
                class_name="p-4 md:p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50",
    )