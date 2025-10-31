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
    is_loading: bool = False
    alert_settings: list[AlertSetting] = []
    alert_history: list[AlertHistory] = []
    editing_setting: dict | None = None
    show_edit_dialog: bool = False

    @rx.var
    def editing_setting_title(self) -> str:
        if self.editing_setting:
            return (
                self.editing_setting.get("alert_type", "")
                .replace("_", " ")
                .capitalize()
            )
        return ""

    @rx.event(background=True)
    async def load_page_data(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            settings_result = await session.execute(
                text("SELECT * FROM alert_settings ORDER BY alert_type")
            )
            history_result = await session.execute(
                text("SELECT * FROM alert_history ORDER BY triggered_at DESC LIMIT 50")
            )
            async with self:
                self.alert_settings = [
                    {
                        **dict(row),
                        "threshold_value": float(row.get("threshold_value") or 0.0),
                        "recipients": row.get("recipients") or "",
                    }
                    for row in settings_result.mappings().all()
                ]
                self.alert_history = [
                    cast(AlertHistory, dict(row))
                    for row in history_result.mappings().all()
                ]
                self.is_loading = False

    @rx.event
    def start_editing(self, setting: dict):
        self.editing_setting = {
            "setting_id": setting.get("setting_id"),
            "alert_type": str(setting.get("alert_type", "")),
            "enabled": bool(setting.get("enabled", False)),
            "threshold_value": float(setting.get("threshold_value") or 0.0),
            "notification_method": str(setting.get("notification_method", "sms")),
            "recipients": str(setting.get("recipients") or ""),
        }
        self.show_edit_dialog = True

    @rx.event
    def cancel_editing(self):
        self.show_edit_dialog = False
        self.editing_setting = None

    @rx.event(background=True)
    async def save_setting(self, form_data: dict):
        if not self.editing_setting:
            return
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE alert_settings 
                     SET enabled = :enabled, 
                         threshold_value = :threshold_value, 
                         notification_method = :notification_method, 
                         recipients = :recipients
                     WHERE setting_id = :setting_id"""),
                {
                    "enabled": form_data.get("enabled") == "on",
                    "threshold_value": float(form_data.get("threshold_value") or 0.0),
                    "notification_method": form_data["notification_method"],
                    "recipients": form_data.get("recipients"),
                    "setting_id": self.editing_setting["setting_id"],
                },
            )
            await session.commit()
        async with self:
            self.show_edit_dialog = False
            self.editing_setting = None
        yield AlertState.load_page_data
        yield rx.toast.success("Alert setting updated successfully!")