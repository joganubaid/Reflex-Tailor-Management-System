import reflex as rx
from app.states.referral_state import ReferralState
from app.components.sidebar import sidebar, mobile_header


def metric_card(
    icon: str, title: str, value: rx.Var, icon_bg_color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-white"),
            class_name=f"p-3 rounded-full {icon_bg_color}",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm",
    )


def status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status.lower(),
            ("completed", "bg-green-100 text-green-800" + base_classes),
            ("pending", "bg-yellow-100 text-yellow-800" + base_classes),
            ("expired", "bg-red-100 text-red-800" + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def top_referrer_card(referrer: rx.Var[dict], index: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    index + 1,
                    class_name="text-sm font-bold text-purple-600 bg-purple-100 rounded-full h-8 w-8 flex items-center justify-center",
                ),
                rx.el.p(
                    referrer["referrer_name"], class_name="font-semibold text-gray-800"
                ),
                class_name="flex items-center gap-3",
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Referrals", class_name="text-xs text-gray-500"),
                rx.el.p(
                    referrer["referral_count"].to_string(),
                    class_name="font-bold text-lg text-purple-600",
                ),
            ),
            rx.el.div(
                rx.el.p("Rewards", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"{referrer['total_rewards']} pts",
                    class_name="font-bold text-lg text-green-600",
                ),
            ),
            class_name="grid grid-cols-2 gap-4 mt-3 pt-3 border-t text-center",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def top_referrer_row(referrer: rx.Var[dict], index: rx.Var[int]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(index + 1, class_name="px-4 py-3 font-bold text-gray-700 text-center"),
        rx.el.td(referrer["referrer_name"], class_name="px-4 py-3 font-medium"),
        rx.el.td(
            referrer["referral_count"].to_string(),
            class_name="px-4 py-3 text-center font-semibold text-purple-600",
        ),
        rx.el.td(
            f"{referrer['total_rewards'].to_string()} pts",
            class_name="px-4 py-3 text-center font-semibold text-green-600",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def referral_card(referral: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"{referral['referrer_name']} -> {referral['referred_name']}",
                    class_name="font-semibold text-gray-800 truncate",
                ),
                rx.el.p(
                    referral["referral_date"].to_string().split("T")[0],
                    class_name="text-xs text-gray-500",
                ),
            ),
            status_badge(referral["referral_status"]),
            class_name="flex justify-between items-start mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Reward", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"{referral['reward_points']} pts",
                    class_name="font-semibold text-purple-600",
                ),
            ),
            rx.el.div(
                rx.el.p("Order Made", class_name="text-xs text-gray-500"),
                rx.el.p(
                    rx.cond(referral["order_completed"], "Yes", "No"),
                    class_name="font-semibold",
                ),
            ),
            class_name="grid grid-cols-2 gap-4 mt-3 pt-3 border-t text-center",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def referral_row(referral: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(referral["referrer_name"], class_name="px-6 py-4 font-medium"),
        rx.el.td(referral["referred_name"], class_name="px-6 py-4"),
        rx.el.td(
            referral["referral_date"].to_string().split("T")[0], class_name="px-6 py-4"
        ),
        rx.el.td(status_badge(referral["referral_status"]), class_name="px-6 py-4"),
        rx.el.td(
            f"{referral['reward_points']} pts",
            class_name="px-6 py-4 font-semibold text-purple-600",
        ),
        rx.el.td(
            rx.cond(referral["order_completed"], "Yes", "No"),
            class_name="px-6 py-4 text-center",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def referrals_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Referral Program",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Track and manage your customer referral program.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    metric_card(
                        "users",
                        "Total Referrals",
                        ReferralState.total_referrals.to_string(),
                        "bg-blue-500",
                    ),
                    metric_card(
                        "user-check",
                        "Completed",
                        ReferralState.completed_referrals.to_string(),
                        "bg-green-500",
                    ),
                    metric_card(
                        "file_clock",
                        "Pending",
                        ReferralState.pending_referrals.to_string(),
                        "bg-yellow-500",
                    ),
                    metric_card(
                        "gift",
                        "Rewards Distributed",
                        f"{ReferralState.total_rewards_distributed.to_string()} pts",
                        "bg-purple-500",
                    ),
                    metric_card(
                        "trending-up",
                        "Conversion Rate",
                        f"{ReferralState.conversion_rate.to_string()}%",
                        "bg-orange-500",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Top Referrers",
                            class_name="text-xl font-semibold text-gray-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Rank",
                                                class_name="px-4 py-3 text-center text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Customer",
                                                class_name="px-4 py-3 text-left text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Referrals",
                                                class_name="px-4 py-3 text-center text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Total Rewards",
                                                class_name="px-4 py-3 text-center text-xs font-bold uppercase",
                                            ),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            ReferralState.top_referrers,
                                            top_referrer_row,
                                        )
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            class_name="hidden md:block overflow-hidden border rounded-xl",
                        ),
                        rx.el.div(
                            rx.foreach(ReferralState.top_referrers, top_referrer_card),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 md:hidden",
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Recent Referrals",
                                class_name="text-xl font-semibold text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "search",
                                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                                    ),
                                    rx.el.input(
                                        placeholder="Search by name...",
                                        on_change=ReferralState.set_search_query,
                                        class_name="w-full md:w-72 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500",
                                    ),
                                    class_name="relative",
                                ),
                                rx.el.select(
                                    rx.el.option("All Statuses", value="all"),
                                    rx.el.option("Pending", value="pending"),
                                    rx.el.option("Completed", value="completed"),
                                    rx.el.option("Expired", value="expired"),
                                    value=ReferralState.status_filter,
                                    on_change=ReferralState.set_status_filter,
                                    class_name="px-4 py-2 border rounded-lg bg-white focus:ring-purple-500",
                                ),
                                class_name="flex items-center gap-4",
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Referrer",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Referred Customer",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Date",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Status",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Reward",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                            ),
                                            rx.el.th(
                                                "Order Made",
                                                class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                            ),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            ReferralState.filtered_referrals,
                                            referral_row,
                                        )
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            rx.cond(
                                ReferralState.filtered_referrals.length() == 0,
                                rx.el.div(
                                    rx.icon(
                                        "users",
                                        class_name="h-12 w-12 text-gray-400 mb-4",
                                    ),
                                    rx.el.h3(
                                        "No Referrals Found",
                                        class_name="text-lg font-semibold",
                                    ),
                                    rx.el.p(
                                        "Referral data will appear here.",
                                        class_name="text-gray-500 mt-1",
                                    ),
                                    class_name="text-center py-16",
                                ),
                                None,
                            ),
                            class_name="hidden md:block overflow-hidden border rounded-xl",
                        ),
                        rx.el.div(
                            rx.foreach(ReferralState.filtered_referrals, referral_card),
                            class_name="grid grid-cols-1 gap-4 md:hidden",
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-sm",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
                ),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )