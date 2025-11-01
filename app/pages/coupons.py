import reflex as rx
from app.states.coupon_state import CouponState
from app.components.sidebar import sidebar, mobile_header
from app.components.coupon_form import coupon_form, delete_coupon_dialog


def coupon_card(coupon: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                coupon["coupon_code"], class_name="font-bold text-lg text-gray-800"
            ),
            rx.el.p(
                rx.cond(
                    coupon["discount_type"] == "percentage",
                    f"{coupon['discount_value']}% OFF",
                    f"₹{coupon['discount_value']} OFF",
                ),
                class_name="text-sm text-purple-600 font-semibold",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(coupon["description"], class_name="text-sm text-gray-500 mt-1"),
        rx.el.div(
            rx.el.span(
                rx.cond(coupon["is_active"], "Active", "Inactive"),
                class_name=rx.cond(
                    coupon["is_active"],
                    "px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-700",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-700",
                ),
            ),
            rx.el.p(
                f"Used: {coupon['used_count']}/{coupon['usage_limit']}",
                class_name="text-xs",
            ),
            class_name="flex justify-between items-center mt-3 pt-3 border-t",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
    )


def coupons_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.h1(
                    "Coupons & Discounts",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search coupons...",
                        on_change=CouponState.set_search_query,
                        class_name="w-full md:w-72 p-2 border rounded-lg",
                    ),
                    rx.el.button(
                        "Add Coupon",
                        on_click=CouponState.toggle_form,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    CouponState.is_loading,
                    rx.el.p("Loading coupons..."),
                    rx.el.div(
                        rx.foreach(CouponState.filtered_coupons, coupon_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                ),
                coupon_form(),
                delete_coupon_dialog(),
                class_name="p-4 md:p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )