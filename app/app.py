import reflex as rx
from app.pages.customers import customers_page
from app.pages.orders import orders_page
from app.pages.inventory import inventory_page
from app.pages.billing import billing_page
from app.pages.dashboard import dashboard_page
from app.pages.workers import workers_page
from app.pages.reports import reports_page
from app.states.report_state import ReportState
from app.pages.measurements import measurements_page
from app.pages.payments import payments_page
from app.pages.profit_analysis import profit_analysis_page
from app.state import CustomerState, OrderState, MaterialState, BillingState
from app.states.dashboard_state import DashboardState
from app.states.worker_state import WorkerState
from app.states.measurement_state import MeasurementState
from app.states.payment_state import PaymentState
from app.states.profit_state import ProfitAnalysisState
from app.states.supplier_state import SupplierState
from app.states.purchase_order_state import PurchaseOrderState
from app.states.loyalty_state import LoyaltyState
from app.states.coupon_state import CouponState
from app.states.referral_state import ReferralState
from app.states.photo_state import PhotoState
from app.states.task_state import TaskState
from app.states.expense_state import ExpenseState
from app.states.alert_state import AlertState
from app.states.mobile_nav_state import MobileNavState
from app.states.order_completion_state import OrderCompletionState
from app.pages.suppliers import suppliers_page
from app.pages.purchase_orders import purchase_orders_page
from app.pages.loyalty import loyalty_page
from app.pages.coupons import coupons_page
from app.pages.referrals import referrals_page
from app.pages.productivity import productivity_page
from app.pages.expenses import expenses_page
from app.pages.alerts import alerts_page
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
app.add_page(reports_page, route="/reports", on_load=ReportState.load_all_reports)
app.add_page(
    measurements_page, route="/measurements", on_load=MeasurementState.get_measurements
)
app.add_page(
    profit_analysis_page,
    route="/profit-analysis",
    on_load=ProfitAnalysisState.get_profit_analysis_data,
)
app.add_page(suppliers_page, route="/suppliers", on_load=SupplierState.get_suppliers)
app.add_page(
    purchase_orders_page,
    route="/purchase-orders",
    on_load=[
        PurchaseOrderState.get_purchase_orders,
        PurchaseOrderState.check_low_stock_materials,
    ],
)
app.add_page(loyalty_page, route="/loyalty", on_load=LoyaltyState.get_loyalty_data)
app.add_page(coupons_page, route="/coupons", on_load=CouponState.get_coupons)
app.add_page(referrals_page, route="/referrals", on_load=ReferralState.get_referrals)
app.add_page(productivity_page, route="/productivity", on_load=TaskState.get_tasks)
app.add_page(
    payments_page,
    route="/payments",
    on_load=[
        PaymentState.get_all_installments,
        PaymentState.check_and_send_payment_reminders,
    ],
)
app.add_page(
    expenses_page,
    route="/expenses",
    on_load=[ExpenseState.get_expenses, ExpenseState.load_form_data],
)
app.add_page(alerts_page, route="/alerts", on_load=AlertState.load_page_data)