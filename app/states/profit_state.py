import reflex as rx
from typing import cast
from sqlalchemy import text
import datetime


class ProfitAnalysisState(rx.State):
    total_revenue: float = 0.0
    total_costs: float = 0.0
    net_profit: float = 0.0
    profit_margin: float = 0.0
    monthly_profit_trend: list[dict] = []
    profit_by_cloth_type: list[dict] = []
    top_profitable_customers: list[dict] = []
    profit_by_worker: list[dict] = []

    @rx.event(background=True)
    async def get_profit_analysis_data(self):
        async with rx.asession() as session:
            metrics_result = await session.execute(
                text("""SELECT 
                        SUM(total_amount) as total_revenue, 
                        SUM(material_cost + labor_cost) as total_costs,
                        SUM(profit) as net_profit
                     FROM orders WHERE status = 'delivered'""")
            )
            metrics = metrics_result.mappings().first()
            trend_result = await session.execute(
                text("""SELECT 
                        TO_CHAR(delivery_date, 'YYYY-MM') as month,
                        SUM(total_amount) as revenue,
                        SUM(material_cost + labor_cost) as costs,
                        SUM(profit) as profit
                     FROM orders
                     WHERE status = 'delivered' AND delivery_date IS NOT NULL
                     GROUP BY month
                     ORDER BY month""")
            )
            monthly_profit_trend = [dict(row) for row in trend_result.mappings().all()]
            cloth_type_result = await session.execute(
                text("""SELECT 
                        cloth_type, 
                        SUM(profit) as total_profit
                     FROM orders
                     WHERE status = 'delivered'
                     GROUP BY cloth_type
                     ORDER BY total_profit DESC""")
            )
            profit_by_cloth_type = [
                dict(row) for row in cloth_type_result.mappings().all()
            ]
            customer_result = await session.execute(
                text("""SELECT 
                        c.name as customer_name, 
                        SUM(o.profit) as total_profit
                     FROM orders o
                     JOIN customers c ON o.customer_id = c.customer_id
                     WHERE o.status = 'delivered'
                     GROUP BY c.customer_id, c.name
                     ORDER BY total_profit DESC
                     LIMIT 5""")
            )
            top_profitable_customers = [
                dict(row) for row in customer_result.mappings().all()
            ]
            worker_result = await session.execute(
                text("""SELECT 
                        w.worker_name, 
                        SUM(o.profit) as total_profit
                     FROM orders o
                     JOIN workers w ON o.assigned_worker = w.worker_id
                     WHERE o.status = 'delivered'
                     GROUP BY w.worker_id, w.worker_name
                     ORDER BY total_profit DESC""")
            )
            profit_by_worker = [dict(row) for row in worker_result.mappings().all()]
            async with self:
                self.total_revenue = float(metrics["total_revenue"] or 0.0)
                self.total_costs = float(metrics["total_costs"] or 0.0)
                self.net_profit = float(metrics["net_profit"] or 0.0)
                self.profit_margin = (
                    self.net_profit / self.total_revenue * 100
                    if self.total_revenue > 0
                    else 0.0
                )
                self.monthly_profit_trend = monthly_profit_trend
                self.profit_by_cloth_type = profit_by_cloth_type
                self.top_profitable_customers = top_profitable_customers
                self.profit_by_worker = profit_by_worker