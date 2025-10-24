import reflex as rx
from typing import cast
from app.models import OrderWithCustomerName, Material, Transaction
from sqlalchemy import text
import datetime


class DashboardState(rx.State):
    """State for the dashboard page."""

    today_revenue: float = 0.0
    pending_orders_count: int = 0
    ready_orders_count: int = 0
    monthly_sales_data: list[dict] = []
    low_stock_items: list[Material] = []
    top_customers: list[dict] = []
    recent_transactions: list[Transaction] = []

    @rx.event(background=True)
    async def get_dashboard_data(self):
        """Fetch all data needed for the dashboard."""
        today = datetime.date.today()
        start_of_month = today.replace(day=1)
        async with rx.asession() as session:
            revenue_result = await session.execute(
                text(
                    "SELECT SUM(advance_payment + (total_amount - balance_payment - advance_payment)) FROM orders WHERE order_date = :today"
                ),
                {"today": today},
            )
            today_revenue = revenue_result.scalar_one_or_none() or 0.0
            pending_orders_result = await session.execute(
                text("SELECT COUNT(*) FROM orders WHERE status = 'pending'")
            )
            pending_orders_count = pending_orders_result.scalar_one() or 0
            ready_orders_result = await session.execute(
                text("SELECT COUNT(*) FROM orders WHERE status = 'ready'")
            )
            ready_orders_count = ready_orders_result.scalar_one() or 0
            low_stock_result = await session.execute(
                text(
                    "SELECT * FROM materials WHERE quantity_in_stock <= reorder_level LIMIT 5"
                )
            )
            low_stock_items = [
                cast(Material, dict(row)) for row in low_stock_result.mappings().all()
            ]
            sales_result = await session.execute(
                text("""SELECT DATE_TRUNC('day', order_date)::date as day, SUM(total_amount) as sales
                     FROM orders
                     WHERE order_date >= :start_of_month
                     GROUP BY day
                     ORDER BY day"""),
                {"start_of_month": start_of_month},
            )
            monthly_sales_data = [
                {"day": row.day.strftime("%b %d"), "sales": float(row.sales)}
                for row in sales_result.mappings().all()
            ]
            top_customers_result = await session.execute(
                text("""SELECT c.name, SUM(o.total_amount) as total_spent
                     FROM customers c
                     JOIN orders o ON c.customer_id = o.customer_id
                     GROUP BY c.customer_id, c.name
                     ORDER BY total_spent DESC
                     LIMIT 5""")
            )
            top_customers = [dict(row) for row in top_customers_result.mappings().all()]
            recent_transactions_result = await session.execute(
                text(
                    "SELECT * FROM orders ORDER BY order_date DESC, order_id DESC LIMIT 5"
                )
            )
            recent_transactions = [
                cast(Transaction, dict(row))
                for row in recent_transactions_result.mappings().all()
            ]
            async with self:
                self.today_revenue = float(today_revenue)
                self.pending_orders_count = pending_orders_count
                self.ready_orders_count = ready_orders_count
                self.low_stock_items = low_stock_items
                self.monthly_sales_data = monthly_sales_data
                self.top_customers = top_customers
                self.recent_transactions = recent_transactions