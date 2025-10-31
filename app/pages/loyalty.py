import reflex as rx
from app.states.loyalty_state import LoyaltyState
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


def tier_badge(tier: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        tier,
        class_name=rx.match(
            tier.lower(),
            (
                "vip",
                "px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-700",
            ),
            (
                "regular",
                "px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-700",
            ),
            (
                "new",
                "px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-700",
            ),
            "px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-700",
        ),
    )


def leaderboard_card(customer: rx.Var[dict], index: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    index + 1,
                    class_name="text-sm font-bold text-purple-600 bg-purple-100 rounded-full h-8 w-8 flex items-center justify-center",
                ),
                rx.el.p(
                    customer["name"], class_name="font-semibold text-gray-800 truncate"
                ),
                class_name="flex items-center gap-3",
            ),
            tier_badge(customer["customer_tier"].capitalize()),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.icon("gem", class_name="h-5 w-5 mr-2 text-purple-500"),
            rx.el.p(
                customer["total_points"].to_string() + " points",
                class_name="text-lg font-bold text-purple-600",
            ),
            class_name="flex items-center justify-center mt-3 pt-3 border-t",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def leaderboard_row(customer: rx.Var[dict], index: rx.Var[int]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(index + 1, class_name="px-6 py-4 font-bold text-gray-700 text-center"),
        rx.el.td(customer["name"], class_name="px-6 py-4 font-medium text-gray-900"),
        rx.el.td(
            rx.el.div(
                rx.icon("gem", class_name="h-4 w-4 mr-2 text-purple-500"),
                customer["total_points"].to_string(),
                class_name="flex items-center font-semibold text-purple-600",
            )
        ),
        rx.el.td(
            tier_badge(customer["customer_tier"].capitalize()), class_name="px-6 py-4"
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def transaction_card(transaction: rx.Var[dict]) -> rx.Component:
    is_earned = transaction["points_change"] > 0
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    transaction["customer_name"],
                    class_name="font-semibold text-gray-800",
                ),
                rx.el.p(
                    transaction["transaction_date"].to_string().split("T")[0],
                    class_name="text-xs text-gray-500",
                ),
            ),
            rx.el.span(
                rx.cond(is_earned, "+", "") + transaction["points_change"].to_string(),
                class_name=rx.cond(
                    is_earned,
                    "text-xl font-bold text-green-600",
                    "text-xl font-bold text-red-600",
                ),
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.p(
                transaction["description"],
                class_name="text-sm text-gray-600 mt-2 truncate",
            )
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def transaction_row(transaction: rx.Var[dict]) -> rx.Component:
    is_earned = transaction["points_change"] > 0
    return rx.el.tr(
        rx.el.td(transaction["customer_name"], class_name="px-6 py-4 font-medium"),
        rx.el.td(
            rx.el.span(
                rx.cond(is_earned, "+", "") + transaction["points_change"].to_string(),
                class_name=rx.cond(
                    is_earned,
                    "text-green-600 font-semibold",
                    "text-red-600 font-semibold",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(transaction["new_balance"].to_string(), class_name="px-6 py-4"),
        rx.el.td(transaction["transaction_type"].capitalize(), class_name="px-6 py-4"),
        rx.el.td(
            transaction["description"], class_name="px-6 py-4 text-sm text-gray-500"
        ),
        rx.el.td(
            transaction["transaction_date"].to_string().split("T")[0],
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def loyalty_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Loyalty Program", class_name="text-3xl font-bold text-gray-800"
                    ),
                    rx.el.p(
                        "Monitor customer points and engagement.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    metric_card(
                        "users",
                        "Active Members",
                        LoyaltyState.total_active_members.to_string(),
                        "bg-blue-500",
                    ),
                    metric_card(
                        "arrow_up",
                        "Total Points Awarded",
                        LoyaltyState.total_points_awarded.to_string(),
                        "bg-green-500",
                    ),
                    metric_card(
                        "arrow_down",
                        "Total Points Redeemed",
                        LoyaltyState.total_points_redeemed.to_string(),
                        "bg-red-500",
                    ),
                    metric_card(
                        "percent",
                        "Avg. Points/Customer",
                        LoyaltyState.avg_points_per_customer.to_string(),
                        "bg-purple-500",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Points Leaderboard",
                            class_name="text-xl font-semibold text-gray-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Rank",
                                                class_name="px-6 py-3 text-center text-xs font-bold uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Customer",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Points",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Tier",
                                                class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                            ),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            LoyaltyState.points_leaderboard,
                                            leaderboard_row,
                                        )
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            class_name="hidden md:block overflow-hidden border rounded-xl",
                        ),
                        rx.el.div(
                            rx.foreach(
                                LoyaltyState.points_leaderboard, leaderboard_card
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 md:hidden",
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Recent Transactions",
                                class_name="text-xl font-semibold text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "search",
                                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                                    ),
                                    rx.el.input(
                                        placeholder="Search by customer name...",
                                        on_change=LoyaltyState.set_search_query,
                                        class_name="w-full md:w-72 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                                    ),
                                    class_name="relative",
                                ),
                                rx.el.select(
                                    rx.el.option("All Transactions", value="all"),
                                    rx.el.option("Purchase", value="purchase"),
                                    rx.el.option("Redemption", value="redemption"),
                                    rx.el.option("Referral", value="referral"),
                                    rx.el.option(
                                        "Birthday Bonus", value="birthday_bonus"
                                    ),
                                    value=LoyaltyState.transaction_filter,
                                    on_change=LoyaltyState.set_transaction_filter,
                                    class_name="px-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500 bg-white",
                                ),
                                class_name="flex items-center gap-4",
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Customer",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Points Change",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "New Balance",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Type",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Description",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Date",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase tracking-wider",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        LoyaltyState.filtered_transactions,
                                        transaction_row,
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            rx.cond(
                                (LoyaltyState.filtered_transactions.length() == 0)
                                & ~LoyaltyState.is_loading,
                                rx.el.div(
                                    rx.icon(
                                        "history",
                                        class_name="h-12 w-12 text-gray-400 mb-4",
                                    ),
                                    rx.el.h3(
                                        "No Transactions Found",
                                        class_name="text-lg font-semibold text-gray-700",
                                    ),
                                    rx.el.p(
                                        "Loyalty point transactions will appear here.",
                                        class_name="text-gray-500 mt-1",
                                    ),
                                    class_name="text-center py-16",
                                ),
                                None,
                            ),
                            class_name="hidden md:block overflow-x-auto border rounded-xl",
                        ),
                        rx.el.div(
                            rx.foreach(
                                LoyaltyState.filtered_transactions, transaction_card
                            ),
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