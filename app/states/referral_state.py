import reflex as rx
from typing import cast, TypedDict
from sqlalchemy import text


class Referral(TypedDict):
    referral_id: int
    referrer_customer_id: int
    referred_customer_id: int
    referral_date: str
    referral_status: str
    reward_points: int
    order_completed: bool
    completed_date: str | None
    referrer_name: str
    referred_name: str


class TopReferrer(TypedDict):
    referrer_customer_id: int
    referrer_name: str
    referral_count: int
    total_rewards: int


class ReferralState(rx.State):
    referrals: list[Referral] = []
    top_referrers: list[TopReferrer] = []
    search_query: str = ""
    status_filter: str = "all"

    @rx.var
    def total_referrals(self) -> int:
        return len(self.referrals)

    @rx.var
    def completed_referrals(self) -> int:
        return sum((1 for r in self.referrals if r["referral_status"] == "completed"))

    @rx.var
    def pending_referrals(self) -> int:
        return sum((1 for r in self.referrals if r["referral_status"] == "pending"))

    @rx.var
    def conversion_rate(self) -> float:
        if not self.total_referrals:
            return 0.0
        return self.completed_referrals / self.total_referrals * 100

    @rx.var
    def total_rewards_distributed(self) -> int:
        return sum(
            (
                r["reward_points"]
                for r in self.referrals
                if r["referral_status"] == "completed"
            )
        )

    @rx.var
    def filtered_referrals(self) -> list[Referral]:
        referrals = self.referrals
        if self.status_filter != "all":
            referrals = [
                r for r in referrals if r["referral_status"] == self.status_filter
            ]
        if self.search_query:
            lower_query = self.search_query.lower()
            return [
                r
                for r in referrals
                if lower_query in r["referrer_name"].lower()
                or lower_query in r["referred_name"].lower()
            ]
        return referrals

    @rx.event(background=True)
    async def get_referrals(self):
        async with rx.asession() as session:
            referrals_result = await session.execute(
                text("""SELECT cr.*, c1.name as referrer_name, c2.name as referred_name 
                     FROM customer_referrals cr
                     JOIN customers c1 ON cr.referrer_customer_id = c1.customer_id
                     JOIN customers c2 ON cr.referred_customer_id = c2.customer_id
                     ORDER BY cr.referral_date DESC""")
            )
            top_referrers_result = await session.execute(
                text("""SELECT 
                         cr.referrer_customer_id, 
                         c.name as referrer_name, 
                         COUNT(cr.referral_id) as referral_count, 
                         SUM(CASE WHEN cr.referral_status = 'completed' THEN cr.reward_points ELSE 0 END) as total_rewards
                     FROM customer_referrals cr
                     JOIN customers c ON cr.referrer_customer_id = c.customer_id
                     GROUP BY cr.referrer_customer_id, c.name
                     ORDER BY referral_count DESC, total_rewards DESC
                     LIMIT 10""")
            )
            async with self:
                self.referrals = [
                    cast(Referral, dict(row))
                    for row in referrals_result.mappings().all()
                ]
                self.top_referrers = [
                    cast(TopReferrer, dict(row))
                    for row in top_referrers_result.mappings().all()
                ]