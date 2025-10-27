import reflex as rx
from typing import cast, TypedDict
from sqlalchemy import text
import datetime


class AlertSetting(TypedDict):
    setting_id: int
    alert_type: str
    enabled: bool
    threshold_value: float | None
    notification_method: str
    recipients: str | None


class AlertHistory(TypedDict):
    alert_id: int
    alert_type: str
    message: str
    severity: str
    triggered_at: str
    status: str


class AlertState(rx.State):
    alert_settings: list[AlertSetting] = []
    alert_history: list[AlertHistory] = []
    editing_setting: AlertSetting | None = None
    show_edit_dialog: bool = False

    @rx.event
    async def load_page_data(self):
        self.alert_settings = []
        self.alert_history = []

    @rx.event
    def start_editing(self, setting: AlertSetting):
        pass

    @rx.event
    def cancel_editing(self):
        self.show_edit_dialog = False
        self.editing_setting = None

    @rx.event
    async def save_setting(self, form_data: dict):
        pass