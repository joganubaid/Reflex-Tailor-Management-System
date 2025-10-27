import reflex as rx
from app.states.coupon_state import CouponState
from app.components.sidebar import sidebar, mobile_header
from app.components.coupon_form import coupon_form, delete_coupon_dialog
import datetime


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


def status_badge(coupon: rx.Var[dict]) -> rx.Component:
    is_expired = rx.cond(
        coupon["valid_until"],
        coupon["valid_until"] < datetime.date.today().isoformat(),
        False,
    )
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        rx.cond(
            is_expired, "Expired", rx.cond(coupon["is_active"], "Active", "Inactive")
        ),
        class_name=rx.match(
            rx.cond(
                is_expired,
                "expired",
                rx.cond(coupon["is_active"], "active", "inactive"),
            ),
            ("active", "bg-green-100 text-green-800" + base_classes),
            ("inactive", "bg-gray-100 text-gray-800" + base_classes),
            ("expired", "bg-red-100 text-red-800" + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def coupon_row(coupon: rx.Var[dict]) -> rx.Component:
    usage_percentage = rx.cond(
        coupon["usage_limit"] > 0, coupon["used_count"] / coupon["usage_limit"] * 100, 0
    )
    return rx.el.tr(
        rx.el.td(
            coupon["coupon_code"],
            class_name="px-6 py-4 font-bold text-gray-900 uppercase",
        ),
        rx.el.td(
            rx.cond(
                coupon["discount_type"] == "percentage",
                coupon["discount_value"].to_string() + "% OFF",
                "₹" + coupon["discount_value"].to_string() + " OFF",
            ),
            class_name="px-6 py-4 font-semibold text-purple-600",
        ),
        rx.el.td(f"₹{coupon['min_order_value'].to_string()}", class_name="px-6 py-4"),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    coupon["valid_from"],
                    coupon["valid_from"].to_string().split("T")[0],
                    "N/A",
                )
                + " to "
                + rx.cond(
                    coupon["valid_until"],
                    coupon["valid_until"].to_string().split("T")[0],
                    "N/A",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="w-full bg-gray-200 rounded-full h-2.5"),
                    rx.el.div(
                        class_name="bg-purple-600 h-2.5 rounded-full",
                        style={"width": usage_percentage.to_string() + "%"},
                    ),
                    class_name="relative w-24",
                ),
                rx.el.span(
                    f"{coupon['used_count']}/{coupon['usage_limit']}",
                    class_name="text-xs ml-2",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(status_badge(coupon), class_name="px-6 py-4"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("file-pen-line", class_name="h-4 w-4"),
                    on_click=lambda: CouponState.start_editing(coupon),
                    class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("toggle-right", class_name="h-4 w-4"),
                    on_click=lambda: CouponState.toggle_coupon_status(coupon),
                    class_name="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: CouponState.show_delete_confirmation(coupon),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center justify-center gap-1",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def coupons_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Coupon Management",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Create and manage discount coupons for your customers.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    metric_card(
                        "ticket",
                        "Total Coupons",
                        CouponState.coupons.length().to_string(),
                        "bg-blue-500",
                    ),
                    metric_card(
                        "check_check",
                        "Active Coupons",
                        CouponState.active_coupons_count.to_string(),
                        "bg-green-500",
                    ),
                    metric_card(
                        "hand-coins",
                        "Total Redemptions",
                        CouponState.total_redemptions.to_string(),
                        "bg-purple-500",
                    ),
                    metric_card(
                        "circle_percent",
                        "Avg. % Discount",
                        CouponState.avg_discount_value.to_string() + "%",
                        "bg-orange-500",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search by coupon code...",
                            type="search",
                            on_change=CouponState.set_search_query,
                            class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500",
                            default_value=CouponState.search_query,
                        ),
                        class_name="relative",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Create Coupon",
                        on_click=CouponState.toggle_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Code",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Discount",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Min Order",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Valid Period",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Usage",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(CouponState.filtered_coupons, coupon_row)
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            CouponState.filtered_coupons.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "ticket-slash",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "No Coupons Found",
                                    class_name="text-lg font-semibold",
                                ),
                                rx.el.p(
                                    "Create your first coupon to get started.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="bg-white p-6 rounded-xl shadow-sm",
                ),
                coupon_form(),
                delete_coupon_dialog(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )