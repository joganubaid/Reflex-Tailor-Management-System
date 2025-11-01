import reflex as rx
from app.states.referral_state import ReferralState
from app.components.sidebar import sidebar, mobile_header


def referral_stat_card(title: str, value: rx.Var[str], icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-8 w-8 text-purple-600"),
        rx.el.div(
            rx.el.p(title, class_name="text-sm text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm",
    )


def referrals_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Referral Program",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    referral_stat_card(
                        "Total Referrals",
                        ReferralState.total_referrals.to_string(),
                        "users",
                    ),
                    referral_stat_card(
                        "Completed Referrals",
                        ReferralState.completed_referrals.to_string(),
                        "check_check",
                    ),
                    referral_stat_card(
                        "Conversion Rate",
                        f"{ReferralState.conversion_rate.to_string()}%",
                        "percent",
                    ),
                    referral_stat_card(
                        "Rewards Distributed",
                        f"{ReferralState.total_rewards_distributed.to_string()} pts",
                        "gift",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Top Referrers", class_name="text-xl font-semibold mb-4"
                        ),
                        rx.el.div(
                            rx.foreach(
                                ReferralState.top_referrers,
                                lambda r: rx.el.div(
                                    rx.el.p(r["referrer_name"], class_name="font-bold"),
                                    rx.el.p(f"{r['referral_count']} referrals"),
                                    rx.el.p(
                                        f"{r['total_rewards']} pts earned",
                                        class_name="text-green-600 font-semibold",
                                    ),
                                    class_name="p-4 bg-white rounded-lg shadow-sm border",
                                ),
                            ),
                            class_name="space-y-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Referral History", class_name="text-xl font-semibold mb-4"
                        ),
                        rx.el.input(
                            placeholder="Search by name...",
                            on_change=ReferralState.set_search_query,
                            class_name="w-full p-2 border rounded-lg mb-4",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th("Referrer"),
                                        rx.el.th("Referred"),
                                        rx.el.th("Date"),
                                        rx.el.th("Status"),
                                        rx.el.th("Reward"),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ReferralState.filtered_referrals,
                                        lambda r: rx.el.tr(
                                            rx.el.td(r["referrer_name"]),
                                            rx.el.td(r["referred_name"]),
                                            rx.el.td(
                                                r["referral_date"]
                                                .to_string()
                                                .split("T")[0]
                                            ),
                                            rx.el.td(r["referral_status"].capitalize()),
                                            rx.el.td(f"{r['reward_points']} pts"),
                                        ),
                                    )
                                ),
                            ),
                            class_name="overflow-x-auto",
                        ),
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
                ),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )