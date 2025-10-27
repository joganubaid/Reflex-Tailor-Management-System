import reflex as rx
from app.states.mobile_nav_state import MobileNavState


def nav_item(text: str, href: str, icon: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5"),
            rx.el.span(text, class_name="font-medium text-sm"),
            class_name=rx.cond(
                is_active,
                "flex items-center gap-3 rounded-lg bg-purple-100 px-3 py-2 text-purple-700 transition-all hover:text-purple-700",
                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
        ),
        href=href,
    )


def mobile_sidebar() -> rx.Component:
    nav_items = [
        {"text": "Dashboard", "href": "/dashboard", "icon": "layout-dashboard"},
        {"text": "Customers", "href": "/customers", "icon": "users"},
        {"text": "Orders", "href": "/orders", "icon": "shopping-cart"},
        {"text": "Measurements", "href": "/measurements", "icon": "ruler"},
        {"text": "Inventory", "href": "/inventory", "icon": "package"},
        {"text": "Billing", "href": "/billing", "icon": "file-text"},
        {"text": "Payments", "href": "/payments", "icon": "indian-rupee"},
        {"text": "Profit Analysis", "href": "/profit-analysis", "icon": "line-chart"},
        {"text": "Reports", "href": "/reports", "icon": "bar-chart-2"},
        {"text": "Workers", "href": "/workers", "icon": "contact"},
        {"text": "Suppliers", "href": "/suppliers", "icon": "truck"},
        {"text": "Purchase Orders", "href": "/purchase-orders", "icon": "file-stack"},
        {"text": "Loyalty Program", "href": "/loyalty", "icon": "gem"},
        {"text": "Coupons", "href": "/coupons", "icon": "ticket"},
        {"text": "Referrals", "href": "/referrals", "icon": "link-2"},
        {"text": "Productivity", "href": "/productivity", "icon": "clipboard-check"},
        {"text": "Expenses", "href": "/expenses", "icon": "credit-card"},
        {"text": "Alerts", "href": "/alerts", "icon": "bell-ring"},
    ]
    current_path = rx.State.router.page.path
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("scissors", class_name="h-8 w-8 text-purple-600"),
                rx.el.span("TailorFlow", class_name="text-xl font-semibold"),
                href="/",
                class_name="flex items-center gap-2 font-semibold",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-6 w-6"),
                on_click=MobileNavState.toggle_sidebar,
                variant="ghost",
                class_name="p-2",
            ),
            class_name="flex items-center justify-between p-4 border-b",
        ),
        rx.el.nav(
            rx.foreach(
                nav_items,
                lambda item: nav_item(
                    item["text"],
                    item["href"],
                    item["icon"],
                    current_path == item["href"],
                ),
            ),
            class_name="grid items-start gap-1 p-4 text-sm font-medium",
            on_click=MobileNavState.toggle_sidebar,
        ),
        class_name="fixed inset-0 z-50 bg-gray-50/95 backdrop-blur-sm md:hidden",
    )


def desktop_sidebar() -> rx.Component:
    nav_items = [
        {"text": "Dashboard", "href": "/dashboard", "icon": "layout-dashboard"},
        {"text": "Customers", "href": "/customers", "icon": "users"},
        {"text": "Orders", "href": "/orders", "icon": "shopping-cart"},
        {"text": "Measurements", "href": "/measurements", "icon": "ruler"},
        {"text": "Inventory", "href": "/inventory", "icon": "package"},
        {"text": "Billing", "href": "/billing", "icon": "file-text"},
        {"text": "Payments", "href": "/payments", "icon": "indian-rupee"},
        {"text": "Profit Analysis", "href": "/profit-analysis", "icon": "line-chart"},
        {"text": "Reports", "href": "/reports", "icon": "bar-chart-2"},
        {"text": "Workers", "href": "/workers", "icon": "contact"},
        {"text": "Suppliers", "href": "/suppliers", "icon": "truck"},
        {"text": "Purchase Orders", "href": "/purchase-orders", "icon": "file-stack"},
        {"text": "Loyalty Program", "href": "/loyalty", "icon": "gem"},
        {"text": "Coupons", "href": "/coupons", "icon": "ticket"},
        {"text": "Referrals", "href": "/referrals", "icon": "link-2"},
        {"text": "Productivity", "href": "/productivity", "icon": "clipboard-check"},
        {"text": "Expenses", "href": "/expenses", "icon": "credit-card"},
        {"text": "Alerts", "href": "/alerts", "icon": "bell-ring"},
    ]
    current_path = rx.State.router.page.path
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("scissors", class_name="h-8 w-8 text-purple-600"),
                rx.el.span(
                    "TailorFlow", class_name="text-xl font-semibold text-gray-800"
                ),
                class_name="flex items-center gap-2 font-semibold",
                href="/",
            ),
            class_name="flex h-16 items-center border-b px-6",
        ),
        rx.el.nav(
            rx.foreach(
                nav_items,
                lambda item: nav_item(
                    item["text"],
                    item["href"],
                    item["icon"],
                    current_path == item["href"],
                ),
            ),
            class_name="flex-1 overflow-auto py-4 px-4 grid items-start gap-1 text-sm font-medium",
        ),
        class_name="hidden md:flex flex-col border-r bg-gray-50/40 h-screen w-64 shrink-0",
    )


def sidebar() -> rx.Component:
    return rx.fragment(
        desktop_sidebar(),
        rx.cond(MobileNavState.sidebar_open, mobile_sidebar(), rx.fragment()),
    )


def mobile_header() -> rx.Component:
    return rx.el.header(
        rx.el.button(
            rx.icon("menu", class_name="h-6 w-6"),
            on_click=MobileNavState.toggle_sidebar,
            class_name="md:hidden p-2",
        ),
        rx.el.div(),
        class_name="sticky top-0 z-10 flex h-16 items-center justify-between border-b bg-white px-4 md:hidden",
    )