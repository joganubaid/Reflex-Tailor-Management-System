import reflex as rx
from typing import cast, TypedDict
from sqlalchemy import text
import datetime
from decimal import Decimal


class WastageData(TypedDict):
    material_name: str
    material_type: str
    unit: str
    total_used: float
    total_wastage: float
    wastage_cost: float
    wastage_percentage: float


class ReportState(rx.State):
    """State for advanced reporting and analytics."""

    report_start_date: str = ""
    report_end_date: str = ""
    top_clv_customers: list[dict] = []
    avg_customer_lifetime_value: float = 0.0
    total_customer_count: int = 0
    wastage_by_material: list[WastageData] = []
    total_wastage_cost: float = 0.0
    avg_wastage_percentage: float = 0.0
    monthly_order_trends: list[dict] = []
    seasonal_revenue_data: list[dict] = []
    gst_summary: dict = {}
    taxable_sales: float = 0.0
    total_gst_collected: float = 0.0
    seasonal_patterns: list[dict] = []
    material_predictions: list[dict] = []
    bulk_purchase_suggestions: list[dict] = []

    @rx.event(background=True)
    async def analyze_seasonal_patterns(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT TO_CHAR(order_date, 'YYYY-MM') as month, COUNT(order_id) as order_count
                     FROM orders
                     WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
                     GROUP BY month
                     ORDER BY month""")
            )
            monthly_data = {
                row["month"]: row["order_count"] for row in result.mappings().all()
            }
            if not monthly_data:
                async with self:
                    self.seasonal_patterns = []
                return
            avg_orders = sum(monthly_data.values()) / len(monthly_data)
            peak_threshold = avg_orders * 1.2
            patterns = []
            for month, count in monthly_data.items():
                patterns.append(
                    {
                        "month": month,
                        "order_count": count,
                        "is_peak": count > peak_threshold,
                        "avg_orders": avg_orders,
                    }
                )
            async with self:
                self.seasonal_patterns = patterns

    @rx.event(background=True)
    async def predict_material_requirements(self, target_month: str):
        year, month = map(int, target_month.split("-"))
        last_year_month = f"{year - 1}-{month:02d}"
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT m.material_name, SUM(om.quantity_used) as total_used
                     FROM order_materials om
                     JOIN orders o ON om.order_id = o.order_id
                     JOIN materials m ON om.material_id = m.material_id
                     WHERE TO_CHAR(o.order_date, 'YYYY-MM') = :last_year_month
                     GROUP BY m.material_name"""),
                {"last_year_month": last_year_month},
            )
            predictions = [dict(row) for row in result.mappings().all()]
            async with self:
                self.material_predictions = predictions

    @rx.event(background=True)
    async def get_bulk_purchase_recommendations(self):
        async with self:
            if not self.seasonal_patterns:
                await self.analyze_seasonal_patterns()
        avg_orders = (
            sum((p["order_count"] for p in self.seasonal_patterns))
            / len(self.seasonal_patterns)
            if self.seasonal_patterns
            else 0
        )
        low_demand_months = [
            p["month"]
            for p in self.seasonal_patterns
            if p["order_count"] < avg_orders * 0.8
        ]
        if not low_demand_months:
            async with self:
                self.bulk_purchase_suggestions = []
            return
        recommendations = [
            {
                "recommendation": f"Consider buying essential materials in bulk during off-peak months: {', '.join(low_demand_months)}.",
                "potential_savings": "5-15% on bulk orders.",
            }
        ]
        async with self:
            self.bulk_purchase_suggestions = recommendations

    @rx.event
    def set_report_dates(self):
        """Set default date range to current month."""
        today = datetime.date.today()
        first_day = today.replace(day=1)
        self.report_start_date = first_day.isoformat()
        self.report_end_date = today.isoformat()

    @rx.event(background=True)
    async def get_clv_analysis(self):
        """Calculate Customer Lifetime Value for all customers."""
        async with rx.asession() as session:
            clv_result = await session.execute(
                text(
                    "SELECT c.customer_id, c.name, c.phone_number, COUNT(o.order_id) as total_orders, SUM(o.total_amount) as total_spent, AVG(o.total_amount) as avg_order_value, MAX(o.order_date) as last_order_date, MIN(o.order_date) as first_order_date, SUM(o.total_amount) / NULLIF(COUNT(o.order_id), 0) as clv FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name, c.phone_number HAVING COUNT(o.order_id) > 0 ORDER BY total_spent DESC LIMIT 10"
                )
            )
            metrics_result = await session.execute(
                text(
                    "SELECT COUNT(DISTINCT c.customer_id) as customer_count, AVG(customer_totals.total_spent) as avg_clv FROM customers c LEFT JOIN ( SELECT customer_id, SUM(total_amount) as total_spent FROM orders GROUP BY customer_id ) customer_totals ON c.customer_id = customer_totals.customer_id WHERE customer_totals.total_spent IS NOT NULL"
                )
            )
            clv_customers = [dict(row) for row in clv_result.mappings().all()]
            metrics = metrics_result.mappings().first()
            async with self:
                self.top_clv_customers = clv_customers
                if metrics:
                    self.total_customer_count = metrics["customer_count"] or 0
                    self.avg_customer_lifetime_value = float(metrics["avg_clv"] or 0.0)

    @rx.event(background=True)
    async def get_wastage_analysis(self):
        """Analyze material wastage across all orders."""
        async with rx.asession() as session:
            wastage_result = await session.execute(
                text(
                    "SELECT m.material_name, m.material_type, m.unit, SUM(om.quantity_used) as total_used, SUM(om.wastage) as total_wastage, SUM(om.wastage * m.unit_price) as wastage_cost, (SUM(om.wastage) / NULLIF(SUM(om.quantity_used), 0) * 100) as wastage_percentage FROM order_materials om JOIN materials m ON om.material_id = m.material_id GROUP BY m.material_id, m.material_name, m.material_type, m.unit HAVING SUM(om.wastage) > 0 ORDER BY wastage_cost DESC"
                )
            )
            totals_result = await session.execute(
                text(
                    "SELECT SUM(om.wastage * m.unit_price) as total_wastage_cost, AVG(om.wastage / NULLIF(om.quantity_used, 0) * 100) as avg_wastage_pct FROM order_materials om JOIN materials m ON om.material_id = m.material_id WHERE om.wastage > 0"
                )
            )
            wastage_data = [
                cast(WastageData, dict(row)) for row in wastage_result.mappings().all()
            ]
            totals = totals_result.mappings().first()
            async with self:
                self.wastage_by_material = wastage_data
                if totals:
                    self.total_wastage_cost = float(totals["total_wastage_cost"] or 0.0)
                    self.avg_wastage_percentage = float(
                        totals["avg_wastage_pct"] or 0.0
                    )

    @rx.event(background=True)
    async def get_seasonal_trends(self):
        """Analyze seasonal order patterns."""
        async with rx.asession() as session:
            monthly_result = await session.execute(
                text(
                    "SELECT TO_CHAR(order_date, 'YYYY-MM') as month, COUNT(order_id) as order_count, SUM(total_amount) as revenue, AVG(total_amount) as avg_order_value FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '12 months' GROUP BY month ORDER BY month"
                )
            )
            seasonal_result = await session.execute(
                text(
                    "SELECT EXTRACT(QUARTER FROM order_date) as quarter, EXTRACT(YEAR FROM order_date) as year, COUNT(order_id) as orders, SUM(total_amount) as revenue FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '2 years' GROUP BY year, quarter ORDER BY year, quarter"
                )
            )
            async with self:
                self.monthly_order_trends = [
                    dict(row) for row in monthly_result.mappings().all()
                ]
                self.seasonal_revenue_data = [
                    dict(row) for row in seasonal_result.mappings().all()
                ]

    @rx.event(background=True)
    async def get_gst_report(self):
        """Generate GST summary for the selected period."""
        async with self:
            if not self.report_start_date or not self.report_end_date:
                today = datetime.date.today()
                first_day = today.replace(day=1)
                self.report_start_date = first_day.isoformat()
                self.report_end_date = today.isoformat()
            start_date = self.report_start_date
            end_date = self.report_end_date
        async with rx.asession() as session:
            gst_result = await session.execute(
                text(
                    "SELECT COUNT(order_id) as total_invoices, SUM(total_amount) as gross_total, SUM(total_amount / 1.18) as taxable_value, SUM(total_amount - (total_amount / 1.18)) as total_gst, SUM((total_amount - (total_amount / 1.18)) / 2) as cgst, SUM((total_amount - (total_amount / 1.18)) / 2) as sgst FROM orders WHERE order_date BETWEEN :start_date AND :end_date AND status = 'delivered'"
                ),
                {"start_date": start_date, "end_date": end_date},
            )
            gst_data = gst_result.mappings().first()
            async with self:
                if gst_data:
                    self.gst_summary = dict(gst_data)
                    self.taxable_sales = float(gst_data["taxable_value"] or 0.0)
                    self.total_gst_collected = float(gst_data["total_gst"] or 0.0)

    @rx.event(background=True)
    async def load_all_reports(self):
        """Load all report data at once."""
        async with self:
            yield ReportState.get_clv_analysis
            yield ReportState.get_wastage_analysis
            yield ReportState.get_seasonal_trends
            yield ReportState.get_gst_report
            yield ReportState.analyze_seasonal_patterns()
            yield ReportState.get_bulk_purchase_recommendations()