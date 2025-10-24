import reflex as rx
from app.pages.customers import customers_page
from app.pages.orders import orders_page
from app.pages.inventory import inventory_page
from app.pages.billing import billing_page
from app.pages.dashboard import dashboard_page
from app.pages.workers import workers_page
from app.pages.reports import reports_page
from app.pages.measurements import measurements_page
from app.pages.payments import payments_page
from app.state import CustomerState, OrderState, MaterialState, BillingState
from app.states.dashboard_state import DashboardState
from app.states.worker_state import WorkerState
from app.states.measurement_state import MeasurementState
from app.states.payment_state import PaymentState
from app.components.sidebar import sidebar


def index() -> rx.Component:
    return dashboard_page()


@rx.page(route="/dashboard", on_load=DashboardState.get_dashboard_data)
def dashboard() -> rx.Component:
    return dashboard_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=DashboardState.get_dashboard_data)
app.add_page(dashboard, route="/dashboard")
app.add_page(customers_page, route="/customers", on_load=CustomerState.get_customers)
app.add_page(
    orders_page,
    route="/orders",
    on_load=[OrderState.get_orders, OrderState.load_form_data],
)
app.add_page(inventory_page, route="/inventory", on_load=MaterialState.get_materials)
app.add_page(
    billing_page, route="/billing", on_load=BillingState.get_orders_for_billing
)
app.add_page(workers_page, route="/workers", on_load=WorkerState.get_workers)
app.add_page(reports_page, route="/reports")
app.add_page(
    payments_page, route="/payments", on_load=PaymentState.get_all_installments
)
app.add_page(
    measurements_page, route="/measurements", on_load=MeasurementState.get_measurements
)