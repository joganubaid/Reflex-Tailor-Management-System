import reflex as rx


class MobileNavState(rx.State):
    """State for mobile navigation."""

    sidebar_open: bool = False

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open