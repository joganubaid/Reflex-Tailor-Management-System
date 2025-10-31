import reflex as rx
from typing import cast, TypedDict
from sqlalchemy import text
import datetime
import random
import string


class Coupon(TypedDict):
    coupon_id: int
    coupon_code: str
    discount_type: str
    discount_value: float
    min_order_value: float
    valid_from: str | None
    valid_until: str | None
    usage_limit: int
    used_count: int
    is_active: bool
    description: str | None


class CouponState(rx.State):
    is_loading: bool = False
    coupons: list[Coupon] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_coupon_id: int | None = None
    show_delete_dialog: bool = False
    coupon_to_delete: Coupon | None = None
    coupon_code: str = ""
    discount_type: str = "percentage"
    discount_value: float = 0.0
    min_order_value: float = 0.0
    valid_from: str = ""
    valid_until: str = ""
    usage_limit: int = 100
    description: str = ""
    is_active: bool = True

    @rx.var
    def filtered_coupons(self) -> list[Coupon]:
        if not self.search_query.strip():
            return self.coupons
        lower_query = self.search_query.lower()
        return [c for c in self.coupons if lower_query in c["coupon_code"].lower()]

    @rx.var
    def active_coupons_count(self) -> int:
        return sum((1 for c in self.coupons if c["is_active"]))

    @rx.var
    def total_redemptions(self) -> int:
        return sum((c.get("used_count", 0) for c in self.coupons))

    @rx.var
    def avg_discount_value(self) -> float:
        percentage_coupons = [
            c for c in self.coupons if c["discount_type"] == "percentage"
        ]
        if not percentage_coupons:
            return 0.0
        return sum((c["discount_value"] for c in percentage_coupons)) / len(
            percentage_coupons
        )

    @rx.event(background=True)
    async def get_coupons(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM discount_coupons ORDER BY created_date DESC")
            )
            rows = result.mappings().all()
            async with self:
                self.coupons = [cast(Coupon, dict(row)) for row in rows]
                self.is_loading = False

    def _reset_form_fields(self):
        self.is_editing = False
        self.editing_coupon_id = None
        self.coupon_code = ""
        self.discount_type = "percentage"
        self.discount_value = 0.0
        self.min_order_value = 0.0
        self.valid_from = ""
        self.valid_until = ""
        self.usage_limit = 100
        self.description = ""
        self.is_active = True

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self._reset_form_fields()

    @rx.event
    def start_editing(self, coupon: Coupon):
        self.is_editing = True
        self.editing_coupon_id = coupon["coupon_id"]
        self.coupon_code = coupon["coupon_code"]
        self.discount_type = coupon["discount_type"]
        self.discount_value = float(coupon.get("discount_value", 0.0))
        self.min_order_value = float(coupon.get("min_order_value", 0.0))
        self.valid_from = (
            str(coupon["valid_from"]).split(" ")[0] if coupon["valid_from"] else ""
        )
        self.valid_until = (
            str(coupon["valid_until"]).split(" ")[0] if coupon["valid_until"] else ""
        )
        self.usage_limit = coupon["usage_limit"]
        self.description = coupon.get("description") or ""
        self.is_active = coupon["is_active"]
        self.show_form = True

    @rx.event
    def generate_coupon_code(self):
        self.coupon_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        form_data["is_active"] = form_data.get("is_active") == "on"
        if self.is_editing:
            yield CouponState.update_coupon(form_data)
        else:
            yield CouponState.add_coupon(form_data)

    @rx.event(background=True)
    async def add_coupon(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO discount_coupons (coupon_code, discount_type, discount_value, min_order_value, valid_from, valid_until, usage_limit, description, is_active, created_date)
                     VALUES (:coupon_code, :discount_type, :discount_value, :min_order_value, :valid_from, :valid_until, :usage_limit, :description, :is_active, :created_date)"""),
                {
                    "coupon_code": form_data["coupon_code"],
                    "discount_type": form_data["discount_type"],
                    "discount_value": float(form_data.get("discount_value", 0.0)),
                    "min_order_value": float(form_data.get("min_order_value", 0.0)),
                    "valid_from": form_data.get("valid_from") or None,
                    "valid_until": form_data.get("valid_until") or None,
                    "usage_limit": int(form_data.get("usage_limit", 100)),
                    "description": form_data.get("description"),
                    "is_active": form_data.get("is_active", True),
                    "created_date": datetime.date.today(),
                },
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield CouponState.get_coupons
        yield rx.toast.success("Coupon created successfully!")

    @rx.event(background=True)
    async def update_coupon(self, form_data: dict):
        if not self.editing_coupon_id:
            return
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE discount_coupons SET 
                        coupon_code = :coupon_code, 
                        discount_type = :discount_type, 
                        discount_value = :discount_value, 
                        min_order_value = :min_order_value, 
                        valid_from = :valid_from, 
                        valid_until = :valid_until, 
                        usage_limit = :usage_limit, 
                        description = :description, 
                        is_active = :is_active
                     WHERE coupon_id = :coupon_id"""),
                {
                    "coupon_code": form_data["coupon_code"],
                    "discount_type": form_data["discount_type"],
                    "discount_value": float(form_data.get("discount_value", 0.0)),
                    "min_order_value": float(form_data.get("min_order_value", 0.0)),
                    "valid_from": form_data.get("valid_from") or None,
                    "valid_until": form_data.get("valid_until") or None,
                    "usage_limit": int(form_data.get("usage_limit", 100)),
                    "description": form_data.get("description"),
                    "is_active": form_data.get("is_active", True),
                    "coupon_id": self.editing_coupon_id,
                },
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield CouponState.get_coupons
        yield rx.toast.success("Coupon updated successfully!")

    @rx.event
    async def toggle_coupon_status(self, coupon: Coupon):
        new_status = not coupon["is_active"]
        async with rx.asession() as session:
            await session.execute(
                text(
                    "UPDATE discount_coupons SET is_active = :status WHERE coupon_id = :id"
                ),
                {"status": new_status, "id": coupon["coupon_id"]},
            )
            await session.commit()
        yield CouponState.get_coupons
        yield rx.toast.info(
            f"Coupon status changed to {('active' if new_status else 'inactive')}."
        )

    @rx.event
    def show_delete_confirmation(self, coupon: Coupon):
        self.show_delete_dialog = True
        self.coupon_to_delete = coupon

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.coupon_to_delete = None

    @rx.event(background=True)
    async def delete_coupon(self):
        if not self.coupon_to_delete:
            return
        async with rx.asession() as session:
            await session.execute(
                text("DELETE FROM discount_coupons WHERE coupon_id = :id"),
                {"id": self.coupon_to_delete["coupon_id"]},
            )
            await session.commit()
        async with self:
            self.show_delete_dialog = False
            self.coupon_to_delete = None
        yield CouponState.get_coupons
        yield rx.toast.success("Coupon deleted successfully!")