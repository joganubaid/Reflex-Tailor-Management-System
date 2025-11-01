import reflex as rx
from app.states.loyalty_state import LoyaltyState
from app.components.sidebar import sidebar, mobile_header


def stat_card(title: str, value: rx.Var[str], icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-white"),
            class_name=f"p-3 rounded-full {color}",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm",
    )


def loyalty_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Loyalty Program",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    stat_card(
                        "Active Members",
                        LoyaltyState.total_active_members.to_string(),
                        "users",
                        "bg-blue-500",
                    ),
                    stat_card(
                        "Total Points Awarded",
                        LoyaltyState.total_points_awarded.to_string(),
                        "gem",
                        "bg-purple-500",
                    ),
                    stat_card(
                        "Avg Pts / Customer",
                        LoyaltyState.avg_points_per_customer.to_string(),
                        "star",
                        "bg-yellow-500",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Points Leaderboard",
                            class_name="text-xl font-semibold mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                LoyaltyState.points_leaderboard,
                                lambda item, index: rx.el.div(
                                    rx.el.div(
                                        rx.el.p(
                                            f"#{index + 1}",
                                            class_name="text-lg font-bold text-purple-600",
                                        ),
                                        rx.el.p(
                                            item["name"], class_name="font-semibold"
                                        ),
                                    ),
                                    rx.el.p(
                                        f"{item['total_points']} pts",
                                        class_name="font-bold text-lg",
                                    ),
                                    class_name="flex items-center justify-between p-3 rounded-lg",
                                    bg=rx.cond(index % 2 == 0, "gray-50", "white"),
                                ),
                            ),
                            class_name="space-y-2",
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Recent Transactions",
                            class_name="text-xl font-semibold mb-4",
                        ),
                        rx.el.input(
                            placeholder="Search by customer name...",
                            on_change=LoyaltyState.set_search_query,
                            class_name="w-full p-2 border rounded-lg mb-4",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th("Customer"),
                                        rx.el.th("Type"),
                                        rx.el.th("Points"),
                                        rx.el.th("Date"),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        LoyaltyState.filtered_transactions,
                                        lambda tx: rx.el.tr(
                                            rx.el.td(tx["customer_name"]),
                                            rx.el.td(
                                                tx["transaction_type"].capitalize()
                                            ),
                                            rx.el.td(
                                                tx["points_change"].to_string(),
                                                color=rx.cond(
                                                    tx["points_change"] > 0,
                                                    "green.500",
                                                    "red.500",
                                                ),
                                            ),
                                            rx.el.td(
                                                tx["transaction_date"]
                                                .to_string()
                                                .split("T")[0]
                                            ),
                                        ),
                                    )
                                ),
                            ),
                            class_name="overflow-x-auto",
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-sm",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
                ),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )