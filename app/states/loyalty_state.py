import reflex as rx
from typing import cast, TypedDict
from sqlalchemy import text
import datetime


class LoyaltyTransaction(TypedDict):
    transaction_id: int
    customer_id: int
    customer_name: str
    points_change: int
    new_balance: int
    transaction_type: str
    transaction_date: str
    description: str


class CustomerPoints(TypedDict):
    customer_id: int
    name: str
    total_points: int
    customer_tier: str


class LoyaltyState(rx.State):
    is_loading: bool = False
    points_leaderboard: list[CustomerPoints] = []
    recent_transactions: list[LoyaltyTransaction] = []
    total_active_members: int = 0
    total_points_awarded: int = 0
    total_points_redeemed: int = 0
    search_query: str = ""
    transaction_filter: str = "all"

    @rx.var
    def avg_points_per_customer(self) -> float:
        return (
            self.total_points_awarded / self.total_active_members
            if self.total_active_members > 0
            else 0.0
        )

    @rx.var
    def filtered_transactions(self) -> list[LoyaltyTransaction]:
        transactions = self.recent_transactions
        if self.transaction_filter != "all":
            transactions = [
                t
                for t in transactions
                if t["transaction_type"].lower() == self.transaction_filter.lower()
            ]
        if self.search_query:
            return [
                t
                for t in transactions
                if self.search_query.lower() in t["customer_name"].lower()
            ]
        return transactions

    @rx.event(background=True)
    async def get_loyalty_data(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            leaderboard_result = await session.execute(
                text("""SELECT customer_id, name, total_points, customer_tier
                     FROM customers 
                     WHERE total_points > 0
                     ORDER BY total_points DESC 
                     LIMIT 10""")
            )
            transactions_result = await session.execute(
                text("""SELECT lt.*, c.name as customer_name 
                     FROM loyalty_points lt
                     JOIN customers c ON lt.customer_id = c.customer_id
                     ORDER BY lt.transaction_date DESC 
                     LIMIT 100""")
            )
            stats_result = await session.execute(
                text("""SELECT
                        (SELECT COUNT(*) FROM customers WHERE total_points > 0) as active_members,
                        (SELECT SUM(points_change) FROM loyalty_points WHERE points_change > 0) as awarded,
                        (SELECT SUM(points_change) FROM loyalty_points WHERE points_change < 0) as redeemed
                    """)
            )
            stats = stats_result.mappings().first()
            async with self:
                self.points_leaderboard = [
                    cast(CustomerPoints, dict(row))
                    for row in leaderboard_result.mappings().all()
                ]
                self.recent_transactions = [
                    cast(LoyaltyTransaction, dict(row))
                    for row in transactions_result.mappings().all()
                ]
                if stats:
                    self.total_active_members = stats["active_members"] or 0
                    self.total_points_awarded = stats["awarded"] or 0
                    self.total_points_redeemed = abs(stats["redeemed"] or 0)
                self.is_loading = False