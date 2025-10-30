import reflex as rx
from typing import Any, cast
from app.models import (
    Customer,
    Order,
    Measurement,
    OrderWithCustomerName,
    Material,
    Transaction,
    Invoice,
)
import datetime
from sqlalchemy import text, func, select
import logging

MATERIAL_REQUIREMENTS = {
    "shirt": {"fabric": 2.5, "button": 8, "thread": 1},
    "pant": {"fabric": 1.8, "zipper": 1, "thread": 1},
    "suit": {"fabric": 4.0, "button": 12, "zipper": 1, "thread": 2},
    "blouse": {"fabric": 1.5, "button": 6, "thread": 1},
    "dress": {"fabric": 3.5, "zipper": 1, "thread": 1},
}


class BaseState(rx.State):
    """The base state for the app."""

    pass


class OrderState(BaseState):
    orders: list[OrderWithCustomerName] = []
    search_query: str = ""
    priority_filter: str = "all"
    show_order_form: bool = False
    is_editing_order: bool = False
    editing_order_id: int | None = None
    available_customers: list[Customer] = []
    available_workers: list[dict] = []
    selected_customer_id: str = ""
    selected_cloth_type: str = "shirt"
    order_quantity: int = 1
    order_delivery_date: str = ""
    order_status: str = "pending"
    order_total_amount: float = 0.0
    order_advance_payment: float = 0.0
    order_special_instructions: str = ""
    assigned_worker_id: str = ""
    save_measurements: bool = True
    chest: float | None = None
    waist: float | None = None
    hip: float | None = None
    shoulder_width: float | None = None
    sleeve_length: float | None = None
    shirt_length: float | None = None
    pant_length: float | None = None
    inseam: float | None = None
    neck: float | None = None
    order_priority: str = "standard"
    show_template_manager: bool = False
    workers_with_workload: list[dict] = []
    applied_coupon_code: str = ""
    coupon_discount: float = 0.0
    coupon_message: str = ""

    @rx.var
    def final_total_amount(self) -> float:
        """Calculate final amount after coupon discount"""
        return max(0, self.order_total_amount - self.coupon_discount)

    @rx.var
    def final_balance_payment(self) -> float:
        """Calculate final balance after discount and advance"""
        return max(0, self.final_total_amount - self.order_advance_payment)

    @rx.var
    def order_balance_payment(self) -> float:
        return self.order_total_amount - self.order_advance_payment

    @rx.event
    def set_applied_coupon_code(self, code: str):
        self.applied_coupon_code = code

    @rx.event(background=True)
    async def validate_and_apply_coupon(self):
        """Validate and apply coupon discount"""
        async with self:
            coupon_code = self.applied_coupon_code
        if not coupon_code:
            yield rx.toast.error("Please enter a coupon code.")
            return
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT * FROM discount_coupons 
                       WHERE coupon_code = :code 
                       AND is_active = TRUE 
                       AND (valid_from IS NULL OR valid_from <= CURRENT_DATE)
                       AND (valid_until IS NULL OR valid_until >= CURRENT_DATE)"""),
                {"code": coupon_code.upper()},
            )
            coupon = result.mappings().first()
        async with self:
            if not coupon:
                self.coupon_message = "Invalid or expired coupon"
                yield rx.toast.error("Invalid or expired coupon")
                return
            if coupon["usage_limit"] and coupon["used_count"] >= coupon["usage_limit"]:
                self.coupon_message = "Coupon usage limit reached"
                yield rx.toast.error("Coupon usage limit reached")
                return
            if self.order_total_amount < coupon["min_order_value"]:
                self.coupon_message = (
                    f"Minimum order ₹{coupon['min_order_value']} required"
                )
                yield rx.toast.error(
                    f"Minimum order value: ₹{coupon['min_order_value']}"
                )
                return
            if coupon["discount_type"] == "percentage":
                discount = self.order_total_amount * coupon["discount_value"] / 100
            else:
                discount = coupon["discount_value"]
            self.applied_coupon_code = coupon_code.upper()
            self.coupon_discount = float(discount)
            self.coupon_message = f"Coupon applied! You saved ₹{discount:.2f}"
        yield rx.toast.success(f"Coupon applied! Discount: ₹{discount:.2f}")

    @rx.event
    def remove_coupon(self):
        """Remove applied coupon"""
        self.applied_coupon_code = ""
        self.coupon_discount = 0.0
        self.coupon_message = ""

    @rx.var
    def filtered_orders(self) -> list[OrderWithCustomerName]:
        orders = self.orders
        if self.priority_filter != "all":
            orders = [o for o in orders if o["priority"] == self.priority_filter]
        if self.search_query:
            lower_query = self.search_query.lower()
            orders = [
                o
                for o in orders
                if lower_query in o["customer_name"].lower()
                or str(o["order_id"]) == lower_query
            ]
        return orders

    @rx.event
    def open_template_manager(self):
        return rx.toast.info("Order template manager is not yet implemented.")

    @rx.event(background=True)
    async def get_orders(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT o.*, c.name as customer_name 
FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
ORDER BY o.order_date DESC""")
            )
            rows = result.mappings().all()
            async with self:
                self.orders = [cast(OrderWithCustomerName, dict(row)) for row in rows]

    @rx.event
    def toggle_order_form(self):
        self.show_order_form = not self.show_order_form
        self.is_editing_order = False
        self._reset_order_form()
        if self.show_order_form:
            return OrderState.load_form_data

    def _reset_order_form(self):
        self.editing_order_id = None
        self.selected_customer_id = ""
        self.selected_cloth_type = "shirt"
        self.order_quantity = 1
        self.order_delivery_date = ""
        self.order_status = "pending"
        self.order_total_amount = 0.0
        self.order_advance_payment = 0.0
        self.order_special_instructions = ""
        self.assigned_worker_id = ""
        self.save_measurements = True
        self._reset_measurements()

    def _reset_measurements(self):
        self.chest = None
        self.waist = None
        self.hip = None
        self.shoulder_width = None
        self.sleeve_length = None
        self.shirt_length = None
        self.pant_length = None
        self.inseam = None
        self.neck = None

    @rx.event(background=True)
    async def on_customer_selected(self, customer_id_str: str):
        """Load customer's latest measurements when selected"""
        from app.state import CustomerState

        if not customer_id_str:
            return
        customer_id = int(customer_id_str)
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT * FROM measurements 
                   WHERE customer_id = :customer_id 
                   ORDER BY measurement_date DESC LIMIT 1"""),
                {"customer_id": customer_id},
            )
            latest = result.mappings().first()
        async with self:
            if latest:
                self.chest = (
                    float(latest.get("chest") or 0) if latest.get("chest") else None
                )
                self.waist = (
                    float(latest.get("waist") or 0) if latest.get("waist") else None
                )
                self.hip = float(latest.get("hip") or 0) if latest.get("hip") else None
                self.shoulder_width = (
                    float(latest.get("shoulder_width") or 0)
                    if latest.get("shoulder_width")
                    else None
                )
                self.sleeve_length = (
                    float(latest.get("sleeve_length") or 0)
                    if latest.get("sleeve_length")
                    else None
                )
                self.shirt_length = (
                    float(latest.get("shirt_length") or 0)
                    if latest.get("shirt_length")
                    else None
                )
                self.pant_length = (
                    float(latest.get("pant_length") or 0)
                    if latest.get("pant_length")
                    else None
                )
                self.inseam = (
                    float(latest.get("inseam") or 0) if latest.get("inseam") else None
                )
                self.neck = (
                    float(latest.get("neck") or 0) if latest.get("neck") else None
                )
                yield rx.toast.info("Previous measurements loaded!")
            else:
                self._reset_measurements()
        async with self:
            customer_state = await self.get_state(CustomerState)
            yield customer_state.get_pricing_suggestion(
                customer_id, self.order_total_amount
            )

    @rx.event(background=True)
    async def load_workers_with_workload(self):
        """Load workers with their current workload"""
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT
                    w.worker_id,
                    w.worker_name,
                    w.role,
                    w.active_status,
                    COUNT(o.order_id) as current_orders
                FROM workers w
                LEFT JOIN orders o ON w.worker_id = o.assigned_worker
                    AND o.status NOT IN ('delivered', 'cancelled')
                WHERE w.active_status = TRUE
                GROUP BY w.worker_id, w.worker_name, w.role, w.active_status
                ORDER BY current_orders ASC, w.worker_name""")
            )
            workers = [dict(row) for row in result.mappings().all()]
        async with self:
            self.workers_with_workload = workers

    @rx.event(background=True)
    async def load_form_data(self):
        async with rx.asession() as session:
            customer_result = await session.execute(
                text(
                    "SELECT customer_id, name, phone_number, prefer_whatsapp, opt_in_whatsapp FROM customers ORDER BY name"
                )
            )
            async with self:
                self.available_customers = [
                    cast(Customer, dict(row))
                    for row in customer_result.mappings().all()
                ]
        yield OrderState.load_workers_with_workload

    @rx.event
    def on_cloth_type_changed(self, cloth_type: str):
        self.selected_cloth_type = cloth_type

    @rx.event
    def start_editing_order(self, order: dict):
        self.is_editing_order = True
        self.editing_order_id = order["order_id"]
        self.selected_customer_id = str(order["customer_id"])
        self.selected_cloth_type = order["cloth_type"]
        self.order_quantity = order["quantity"]
        self.order_delivery_date = (
            str(order["delivery_date"]).split(" ")[0] if order["delivery_date"] else ""
        )
        self.order_total_amount = float(order.get("total_amount", 0.0))
        self.order_advance_payment = float(order.get("advance_payment", 0.0))
        self.order_special_instructions = order.get("special_instructions") or ""
        self.order_priority = order.get("priority", "standard")
        self.applied_coupon_code = order.get("coupon_code") or ""
        self.coupon_discount = float(order.get("discount_amount") or 0.0)
        self.show_order_form = True
        return OrderState.on_customer_selected(order["customer_id"])

    @rx.event
    def calculate_balance(self, value: Any):
        pass

    @rx.event(background=True)
    async def handle_order_form_submit(self, form_data: dict):
        """Handle the submission of the order form for both add and edit."""
        async with self:
            if form_data.get("coupon_code"):
                self.applied_coupon_code = form_data["coupon_code"]
        if self.is_editing_order:
            async with self:
                self.show_order_form = False
            yield rx.toast.info("Order editing functionality is not yet implemented.")
        else:
            yield OrderState.add_order(form_data)

    @rx.event(background=True)
    async def add_order(self, form_data: dict):
        """Adds a new order to the database and sends a confirmation SMS."""
        from app.utils.sms import send_order_confirmation
        from app.utils.whatsapp import send_whatsapp_order_confirmation

        cloth_type = form_data["cloth_type"]
        quantity = int(form_data.get("quantity", 1))
        required_mats = MATERIAL_REQUIREMENTS.get(cloth_type, {})
        async with rx.asession() as session:
            for material_type, req_qty in required_mats.items():
                total_req = req_qty * quantity
                result = await session.execute(
                    text(
                        "SELECT quantity_in_stock, material_name FROM materials WHERE material_type = :type AND material_name ILIKE :name_pattern LIMIT 1"
                    ),
                    {"type": material_type, "name_pattern": f"%{material_type}%"},
                )
                material = result.mappings().first()
                if not material or material["quantity_in_stock"] < total_req:
                    available_qty = material["quantity_in_stock"] if material else 0
                    material_name = (
                        material["material_name"] if material else material_type
                    )
                    yield rx.toast.error(
                        f"Insufficient stock for {material_name.capitalize()}. Required: {total_req}, Available: {available_qty}"
                    )
                    return
        customer_id = int(form_data["customer_id"])
        total_amount = float(form_data.get("total_amount", 0))
        advance_payment = float(form_data.get("advance_payment", 0))
        delivery_date = form_data.get("delivery_date") or None
        priority = self.order_priority
        final_total = self.final_total_amount
        balance = self.final_balance_payment
        async with rx.asession() as session:
            result = await session.execute(
                text("""INSERT INTO orders (customer_id, order_date, delivery_date, status, 
            cloth_type, quantity, total_amount, advance_payment, balance_payment, 
            special_instructions, priority, coupon_code, discount_amount, points_earned)
         VALUES (:customer_id, :order_date, :delivery_date, :status, :cloth_type, 
                 :quantity, :total_amount, :advance_payment, :balance_payment, 
                 :special_instructions, :priority, :coupon_code, :discount_amount, :points_earned)
         RETURNING order_id"""),
                {
                    "customer_id": customer_id,
                    "order_date": datetime.date.today(),
                    "delivery_date": delivery_date,
                    "status": "pending",
                    "cloth_type": form_data["cloth_type"],
                    "quantity": int(form_data.get("quantity", 1)),
                    "total_amount": total_amount,
                    "advance_payment": advance_payment,
                    "balance_payment": balance,
                    "special_instructions": form_data.get("special_instructions"),
                    "priority": priority,
                    "coupon_code": self.applied_coupon_code or None,
                    "discount_amount": self.coupon_discount,
                    "points_earned": int(final_total / 100),
                },
            )
            new_order_id = result.scalar_one()
            if self.applied_coupon_code:
                await session.execute(
                    text(
                        "UPDATE discount_coupons SET used_count = used_count + 1 WHERE coupon_code = :code"
                    ),
                    {"code": self.applied_coupon_code},
                )
            await session.commit()
        customer = next(
            (c for c in self.available_customers if c["customer_id"] == customer_id),
            None,
        )
        if customer:
            notification_preference = customer.get("prefer_whatsapp", "sms")
            if notification_preference in ["sms", "both"]:
                sms_sent = send_order_confirmation(
                    customer_phone=customer["phone_number"],
                    customer_name=customer["name"],
                    order_id=new_order_id,
                    delivery_date=str(delivery_date) if delivery_date else "TBA",
                    total_amount=total_amount,
                )
                if not sms_sent:
                    yield rx.toast.error("Failed to send order confirmation SMS.")
            if customer.get("opt_in_whatsapp") and notification_preference in [
                "whatsapp",
                "both",
            ]:
                wa_sent = send_whatsapp_order_confirmation(
                    customer_phone=customer["phone_number"],
                    customer_name=customer["name"],
                    order_id=new_order_id,
                    delivery_date=str(delivery_date) if delivery_date else "TBA",
                    total_amount=total_amount,
                )
                if not wa_sent:
                    yield rx.toast.error(
                        "Failed to send order confirmation via WhatsApp."
                    )
        async with self:
            self.show_order_form = False
        yield rx.toast.success("Order added successfully!")
        yield OrderState.get_orders

    @rx.event(background=True)
    async def update_order_status(self, order_id: int, new_status: str):
        from app.utils.sms import (
            send_order_ready_notification,
            send_status_update_notification,
        )
        from app.utils.whatsapp import (
            send_whatsapp_order_ready,
            send_whatsapp_status_update,
        )

        if new_status == "cutting":
            async with rx.asession() as session:
                order_res = await session.execute(
                    text(
                        "SELECT cloth_type, quantity, assigned_worker FROM orders WHERE order_id = :order_id"
                    ),
                    {"order_id": order_id},
                )
                order = order_res.mappings().first()
                if not order:
                    yield rx.toast.error(f"Order #{order_id} not found.")
                    return
                labor_cost = 0.0
                if order["assigned_worker"]:
                    worker_res = await session.execute(
                        text("SELECT salary FROM workers WHERE worker_id = :worker_id"),
                        {"worker_id": order["assigned_worker"]},
                    )
                    worker = worker_res.mappings().first()
                    if worker:
                        labor_cost = float(worker["salary"]) * 0.01
                required_mats = MATERIAL_REQUIREMENTS.get(order["cloth_type"], {})
                total_material_cost = 0.0
                for material_type, req_qty in required_mats.items():
                    total_req = req_qty * order["quantity"]
                    mat_res = await session.execute(
                        text(
                            "SELECT material_id, quantity_in_stock, unit_price, material_name FROM materials WHERE material_type = :type AND material_name ILIKE :name_pattern LIMIT 1"
                        ),
                        {"type": material_type, "name_pattern": f"%{material_type}%"},
                    )
                    material = mat_res.mappings().first()
                    if not material or material["quantity_in_stock"] < total_req:
                        available = material["quantity_in_stock"] if material else 0
                        mat_name = (
                            material["material_name"] if material else material_type
                        )
                        yield rx.toast.error(
                            f"Cannot start cutting. Insufficient {mat_name.capitalize()}. Required: {total_req}, Available: {available}"
                        )
                        return
                for material_type, req_qty in required_mats.items():
                    total_req = req_qty * order["quantity"]
                    mat_res = await session.execute(
                        text(
                            "SELECT material_id, quantity_in_stock, unit_price, reorder_level FROM materials WHERE material_type = :type AND material_name ILIKE :name_pattern LIMIT 1"
                        ),
                        {"type": material_type, "name_pattern": f"%{material_type}%"},
                    )
                    material = mat_res.mappings().first()
                    await session.execute(
                        text(
                            "UPDATE materials SET quantity_in_stock = quantity_in_stock - :used WHERE material_id = :mat_id"
                        ),
                        {"used": total_req, "mat_id": material["material_id"]},
                    )
                    wastage = total_req * 0.05
                    cost = total_req * material["unit_price"]
                    total_material_cost += cost
                    await session.execute(
                        text(
                            "INSERT INTO order_materials (order_id, material_id, quantity_used, wastage, cost) VALUES (:oid, :mid, :qty, :wst, :cst)"
                        ),
                        {
                            "oid": order_id,
                            "mid": material["material_id"],
                            "qty": total_req,
                            "wst": wastage,
                            "cst": cost,
                        },
                    )
                    if (
                        material["quantity_in_stock"] - total_req
                        < material["reorder_level"]
                    ):
                        yield rx.toast.warning(
                            f"{material_type.capitalize()} stock is now below reorder level!"
                        )
                await session.execute(
                    text(
                        "UPDATE orders SET material_cost = :material_cost, labor_cost = :labor_cost, profit = total_amount - :material_cost - :labor_cost WHERE order_id = :id"
                    ),
                    {
                        "material_cost": total_material_cost,
                        "labor_cost": labor_cost,
                        "id": order_id,
                    },
                )
                await session.commit()
                yield rx.toast.success("Materials deducted and costs updated.")
        async with rx.asession() as session, session.begin():
            await session.execute(
                text("UPDATE orders SET status = :status WHERE order_id = :order_id"),
                {"status": new_status, "order_id": order_id},
            )
            if new_status.lower() == "delivered":
                order_res = await session.execute(
                    text(
                        "SELECT customer_id, total_amount FROM orders WHERE order_id = :id"
                    ),
                    {"id": order_id},
                )
                order_info = order_res.mappings().first()
                if order_info:
                    customer_id = order_info["customer_id"]
                    total_amount = float(order_info["total_amount"])
                    points_earned = int(total_amount / 100)
                    cust_res = await session.execute(
                        text(
                            "SELECT total_points, customer_tier, referred_by FROM customers WHERE customer_id = :cid"
                        ),
                        {"cid": customer_id},
                    )
                    customer_data = cust_res.mappings().first()
                    current_points = customer_data["total_points"]
                    new_total_points = current_points + points_earned
                    current_tier = customer_data["customer_tier"]
                    new_tier = current_tier
                    if new_total_points > 2000 and current_tier != "vip":
                        new_tier = "vip"
                    elif new_total_points > 500 and current_tier not in [
                        "vip",
                        "regular",
                    ]:
                        new_tier = "regular"
                    await session.execute(
                        text(
                            "UPDATE customers SET total_points = :points, customer_tier = :tier WHERE customer_id = :cid"
                        ),
                        {
                            "points": new_total_points,
                            "tier": new_tier,
                            "cid": customer_id,
                        },
                    )
                    await session.execute(
                        text("""INSERT INTO loyalty_points (customer_id, points_change, new_balance, transaction_type, order_id, description)
                             VALUES (:cid, :points, :balance, 'purchase', :oid, :desc)"""),
                        {
                            "cid": customer_id,
                            "points": points_earned,
                            "balance": new_total_points,
                            "oid": order_id,
                            "desc": f"Points earned from order #{order_id}",
                        },
                    )
                    if new_tier != current_tier:
                        yield rx.toast.info(
                            f"Customer promoted to {new_tier.capitalize()} tier!"
                        )
                    if customer_data["referred_by"]:
                        referral_check = await session.execute(
                            text("""SELECT referral_id, referrer_customer_id, reward_points 
                                     FROM customer_referrals 
                                     WHERE referred_customer_id = :referred_id AND referral_status = 'pending'"""),
                            {"referred_id": customer_id},
                        )
                        referral_info = referral_check.mappings().first()
                        order_count_check = await session.execute(
                            text(
                                "SELECT COUNT(*) FROM orders WHERE customer_id = :cid AND status = 'delivered'"
                            ),
                            {"cid": customer_id},
                        )
                        completed_orders_count = order_count_check.scalar_one()
                        if referral_info and completed_orders_count == 1:
                            referrer_id = referral_info["referrer_customer_id"]
                            reward_points = referral_info["reward_points"]
                            referrer_cust_res = await session.execute(
                                text(
                                    "SELECT name, total_points FROM customers WHERE customer_id = :rid"
                                ),
                                {"rid": referrer_id},
                            )
                            referrer_data = referrer_cust_res.mappings().first()
                            new_referrer_points = (
                                referrer_data["total_points"] + reward_points
                            )
                            await session.execute(
                                text(
                                    "UPDATE customers SET total_points = :points WHERE customer_id = :rid"
                                ),
                                {"points": new_referrer_points, "rid": referrer_id},
                            )
                            await session.execute(
                                text("""INSERT INTO loyalty_points (customer_id, points_change, new_balance, transaction_type, description)
                                     VALUES (:cid, :points, :balance, 'referral', :desc)"""),
                                {
                                    "cid": referrer_id,
                                    "points": reward_points,
                                    "balance": new_referrer_points,
                                    "desc": f"Referral bonus for {customer_data['name']}",
                                },
                            )
                            await session.execute(
                                text("""UPDATE customer_referrals 
                                     SET referral_status = 'completed', completed_date = :date, order_completed = TRUE
                                     WHERE referral_id = :ref_id"""),
                                {
                                    "date": datetime.date.today(),
                                    "ref_id": referral_info["referral_id"],
                                },
                            )
                            yield rx.toast.success(
                                f"Referrer {referrer_data['name']} awarded {reward_points} points!"
                            )
        async with self:
            yield OrderState.get_orders
        yield rx.toast.info(f"Order #{order_id} status updated to {new_status}.")
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT c.name, c.phone_number, c.opt_in_whatsapp, c.prefer_whatsapp 
                         FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
                         WHERE o.order_id = :order_id"""),
                {"order_id": order_id},
            )
            customer_info = result.mappings().first()
        if customer_info:
            notification_preference = customer_info.get("prefer_whatsapp", "sms")
            customer_phone = customer_info["phone_number"]
            customer_name = customer_info["name"]
            opt_in_whatsapp = customer_info.get("opt_in_whatsapp")
            if new_status.lower() == "ready":
                if notification_preference in ["sms", "both"]:
                    send_order_ready_notification(
                        customer_phone, customer_name, order_id
                    )
                if opt_in_whatsapp and notification_preference in ["whatsapp", "both"]:
                    send_whatsapp_order_ready(customer_phone, customer_name, order_id)
            else:
                if notification_preference in ["sms", "both"]:
                    send_status_update_notification(
                        customer_phone, customer_name, order_id, new_status
                    )
                if opt_in_whatsapp and notification_preference in ["whatsapp", "both"]:
                    send_whatsapp_status_update(
                        customer_phone, customer_name, order_id, new_status
                    )
        else:
            yield rx.toast.error(
                f"Could not find customer details for order #{order_id} to send notification."
            )

    @rx.event(background=True)
    async def duplicate_order(self, order_id: int):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM orders WHERE order_id = :order_id"),
                {"order_id": order_id},
            )
            original_order = result.mappings().first()
            if not original_order:
                async with self:
                    yield rx.toast.error("Original order not found.")
                return
            new_order_data = dict(original_order)
            new_order_data.pop("order_id", None)
            new_order_data["order_date"] = datetime.date.today()
            new_order_data["delivery_date"] = None
            new_order_data["status"] = "pending"
            new_order_data["is_duplicate"] = True
            new_order_data["original_order_id"] = order_id
            insert_query = text("""INSERT INTO orders (customer_id, order_date, delivery_date, status, cloth_type, quantity, total_amount, advance_payment, balance_payment, special_instructions, priority, is_duplicate, original_order_id)
                     VALUES (:customer_id, :order_date, :delivery_date, :status, :cloth_type, :quantity, :total_amount, :advance_payment, :balance_payment, :special_instructions, :priority, :is_duplicate, :original_order_id)
                     RETURNING order_id""")
            new_result = await session.execute(insert_query, new_order_data)
            new_order_id = new_result.scalar_one()
            await session.commit()
        async with self:
            yield rx.toast.success(
                f"Order #{order_id} duplicated as new order #{new_order_id}."
            )
            yield OrderState.get_orders

    @rx.event
    def generate_qr_code(self, order_id: int):
        return rx.toast.info(f"QR code for order #{order_id} is not yet implemented.")


class CustomerState(BaseState):
    customers: list[Customer] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_customer_id: int | None = None
    show_delete_dialog: bool = False
    customer_to_delete: Customer | None = None
    name: str = ""
    phone_number: str = ""
    email: str = ""
    address: str = ""
    notes: str = ""
    opt_in_whatsapp: bool = False
    prefer_whatsapp: bool = False
    customer_lifetime_value: float = 0.0
    suggested_discount_percent: float = 0.0
    show_pricing_suggestion: bool = False
    suggested_discount: float = 0.0
    suggested_price: float = 0.0

    @rx.event(background=True)
    async def get_pricing_suggestion(self, customer_id: int, order_amount: float):
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT customer_tier, SUM(o.total_amount) as total_spent FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE c.customer_id = :customer_id GROUP BY c.customer_id, c.customer_tier"
                ),
                {"customer_id": customer_id},
            )
            customer_data = result.mappings().first()
        async with self:
            if not customer_data:
                self.suggested_discount_percent = 0.0
                self.customer_lifetime_value = 0.0
                return
            self.customer_lifetime_value = float(customer_data["total_spent"] or 0.0)
            tier = customer_data["customer_tier"]
            if tier == "vip":
                self.suggested_discount_percent = 10.0
                reason = "VIP Customer Discount"
            elif tier == "regular":
                self.suggested_discount_percent = 5.0
                reason = "Loyal Customer Discount"
            else:
                self.suggested_discount_percent = 0.0
                reason = "Standard Pricing"
            discount_amount = order_amount * (self.suggested_discount_percent / 100)
            final_amount = order_amount - discount_amount
            order_state = await self.get_state(OrderState)
            order_state.suggested_discount = discount_amount
            order_state.suggested_price = final_amount
            self.show_pricing_suggestion = True
        yield rx.toast.info(
            f"Pricing Suggestion: {self.suggested_discount_percent}% off ({reason})"
        )

    @rx.event(background=True)
    async def get_customers(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT c.*, COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY c.name""")
            )
            rows = result.mappings().all()
            async with self:
                self.customers = [cast(Customer, dict(row)) for row in rows]

    @rx.var
    def filtered_customers(self) -> list[Customer]:
        if not self.search_query.strip():
            return self.customers
        lower_query = self.search_query.lower()
        return [
            c
            for c in self.customers
            if lower_query in c["name"].lower() or lower_query in c["phone_number"]
        ]

    @rx.event
    async def add_customer(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text(
                    "INSERT INTO customers (name, phone_number, email, address, notes, registration_date, opt_in_whatsapp, prefer_whatsapp) VALUES (:name, :phone_number, :email, :address, :notes, :registration_date, :opt_in_whatsapp, :prefer_whatsapp)"
                ),
                {
                    "name": form_data["name"],
                    "phone_number": form_data["phone_number"],
                    "email": form_data.get("email", ""),
                    "address": form_data.get("address", ""),
                    "notes": form_data.get("notes", ""),
                    "registration_date": datetime.date.today(),
                    "opt_in_whatsapp": form_data.get("opt_in_whatsapp") == "on",
                    "prefer_whatsapp": form_data.get("prefer_whatsapp") == "on",
                },
            )
            await session.commit()
        self.show_form = False
        yield rx.toast.success("Customer added successfully!")
        yield CustomerState.get_customers
        return

    @rx.event
    async def update_customer(self, form_data: dict):
        if self.editing_customer_id is None:
            yield rx.toast.error("No customer selected for editing.")
            return
        async with rx.asession() as session:
            await session.execute(
                text(
                    "UPDATE customers SET name = :name, phone_number = :phone_number, email = :email, address = :address, notes = :notes, opt_in_whatsapp = :opt_in_whatsapp, prefer_whatsapp = :prefer_whatsapp WHERE customer_id = :customer_id"
                ),
                {
                    "name": form_data["name"],
                    "phone_number": form_data["phone_number"],
                    "email": form_data.get("email", ""),
                    "address": form_data.get("address", ""),
                    "notes": form_data.get("notes", ""),
                    "opt_in_whatsapp": form_data.get("opt_in_whatsapp") == "on",
                    "prefer_whatsapp": form_data.get("prefer_whatsapp") == "on",
                    "customer_id": self.editing_customer_id,
                },
            )
            await session.commit()
        self.show_form = False
        yield rx.toast.success("Customer updated successfully!")
        yield CustomerState.get_customers
        return

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        if self.is_editing:
            yield CustomerState.update_customer(form_data)
        else:
            yield CustomerState.add_customer(form_data)

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self.is_editing = False
        self._reset_form_fields()

    @rx.event
    def start_editing(self, customer: Customer):
        self.is_editing = True
        self.editing_customer_id = customer["customer_id"]
        self.name = customer["name"]
        self.phone_number = customer["phone_number"]
        self.email = customer["email"] or ""
        self.address = customer["address"] or ""
        self.notes = customer.get("notes") or ""
        self.opt_in_whatsapp = customer.get("opt_in_whatsapp", False)
        self.prefer_whatsapp = bool(customer.get("prefer_whatsapp", False))
        self.show_form = True

    def _reset_form_fields(self):
        self.name = ""
        self.phone_number = ""
        self.email = ""
        self.address = ""
        self.notes = ""
        self.editing_customer_id = None
        self.opt_in_whatsapp = False
        self.prefer_whatsapp = False

    @rx.event
    def show_delete_confirmation(self, customer: Customer):
        self.show_delete_dialog = True
        self.customer_to_delete = customer

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.customer_to_delete = None

    @rx.event
    async def delete_customer(self):
        if self.customer_to_delete:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT COUNT(*) FROM orders WHERE customer_id = :customer_id"
                    ),
                    {"customer_id": self.customer_to_delete["customer_id"]},
                )
                order_count = result.scalar_one()
                if order_count > 0:
                    self.show_delete_dialog = False
                    yield rx.toast.error("Cannot delete customer with existing orders.")
                    return
                await session.execute(
                    text("DELETE FROM customers WHERE customer_id = :customer_id"),
                    {"customer_id": self.customer_to_delete["customer_id"]},
                )
                await session.commit()
            self.show_delete_dialog = False
            self.customer_to_delete = None
            yield rx.toast.success("Customer deleted successfully.")
            yield CustomerState.get_customers
            return
        self.show_delete_dialog = False
        yield rx.toast.error("No customer selected for deletion.")
        return


class BillingState(BaseState):
    orders_for_billing: list[OrderWithCustomerName] = []
    transactions: list[Transaction] = []
    invoices: list[Invoice] = []
    show_invoice_form: bool = False
    show_payment_form: bool = False
    selected_order_for_invoice: OrderWithCustomerName | None = None
    total_revenue: float = 0.0
    today_collection: float = 0.0
    pending_payments: float = 0.0
    month_revenue: float = 0.0

    @rx.event(background=True)
    async def get_orders_for_billing(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT o.*, c.name as customer_name 
FROM orders o JOIN customers c ON o.customer_id = c.customer_id 
ORDER BY o.order_date DESC""")
            )
            rows = result.mappings().all()
            async with self:
                self.orders_for_billing = [
                    cast(OrderWithCustomerName, dict(row)) for row in rows
                ]


class MaterialState(BaseState):
    materials: list[Material] = []
    search_query: str = ""
    stock_filter: str = "all"
    type_filter: str = "all"
    show_form: bool = False
    is_editing: bool = False
    editing_material_id: int | None = None
    show_delete_dialog: bool = False
    material_to_delete: Material | None = None
    material_name: str = ""
    material_type: str = "fabric"
    quantity_in_stock: float = 0.0
    unit: str = "meter"
    unit_price: float = 0.0
    reorder_level: float = 0.0
    supplier_name: str = ""
    supplier_contact: str = ""
    last_purchase_date: str = ""

    @rx.event(background=True)
    async def get_materials(self):
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT * FROM materials ORDER BY material_name")
            )
            rows = result.mappings().all()
            materials = []
            for row in rows:
                material_dict = dict(row)
                material_dict["quantity_in_stock"] = float(
                    material_dict.get("quantity_in_stock") or 0.0
                )
                material_dict["unit_price"] = float(
                    material_dict.get("unit_price") or 0.0
                )
                material_dict["reorder_level"] = float(
                    material_dict.get("reorder_level") or 0.0
                )
                materials.append(cast(Material, material_dict))
            async with self:
                self.materials = materials

    @rx.var
    def filtered_materials(self) -> list[Material]:
        materials = self.materials
        if self.stock_filter == "low":
            materials = [
                m
                for m in materials
                if m["quantity_in_stock"] <= m["reorder_level"]
                and m["quantity_in_stock"] > 0
            ]
        elif self.stock_filter == "out":
            materials = [m for m in materials if m["quantity_in_stock"] == 0]
        if self.type_filter != "all":
            materials = [m for m in materials if m["material_type"] == self.type_filter]
        if self.search_query.strip():
            lower_query = self.search_query.lower()
            materials = [
                m for m in materials if lower_query in m["material_name"].lower()
            ]
        return materials

    @rx.var
    def total_inventory_value(self) -> float:
        return sum(
            (
                float(m.get("quantity_in_stock", 0) or 0)
                * float(m.get("unit_price", 0) or 0)
                for m in self.materials
            )
        )

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        form_data["last_purchase_date"] = form_data["last_purchase_date"] or None
        form_data["supplier_name"] = form_data["supplier_name"] or None
        form_data["supplier_contact"] = form_data["supplier_contact"] or None
        if self.is_editing:
            return MaterialState.update_material(form_data)
        else:
            return MaterialState.add_material(form_data)

    @rx.event
    async def add_material(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO materials (material_name, material_type, quantity_in_stock, unit, unit_price, reorder_level, supplier_name, supplier_contact, last_purchase_date) 
                     VALUES (:material_name, :material_type, :quantity_in_stock, :unit, :unit_price, :reorder_level, :supplier_name, :supplier_contact, :last_purchase_date)"""),
                form_data,
            )
            await session.commit()
        self.show_form = False
        yield MaterialState.get_materials
        yield rx.toast.success("Material added successfully!")

    @rx.event
    async def update_material(self, form_data: dict):
        if self.editing_material_id is None:
            yield rx.toast.error("No material selected for editing.")
            return
        form_data["material_id"] = self.editing_material_id
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE materials SET material_name = :material_name, material_type = :material_type, 
                     quantity_in_stock = :quantity_in_stock, unit = :unit, unit_price = :unit_price, reorder_level = :reorder_level, 
                     supplier_name = :supplier_name, supplier_contact = :supplier_contact, last_purchase_date = :last_purchase_date
                     WHERE material_id = :material_id"""),
                form_data,
            )
            await session.commit()
        self.show_form = False
        yield MaterialState.get_materials
        yield rx.toast.success("Material updated successfully!")

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self.is_editing = False
        self._reset_form_fields()

    @rx.event
    def start_editing(self, material: Material):
        self.is_editing = True
        self.editing_material_id = material["material_id"]
        self.material_name = material["material_name"]
        self.material_type = material["material_type"]
        self.quantity_in_stock = float(material.get("quantity_in_stock") or 0.0)
        self.unit = material["unit"]
        self.unit_price = float(material.get("unit_price") or 0.0)
        self.reorder_level = float(material.get("reorder_level") or 0.0)
        self.supplier_name = material.get("supplier_name") or ""
        self.supplier_contact = material.get("supplier_contact") or ""
        purchase_date = material.get("last_purchase_date")
        self.last_purchase_date = str(purchase_date) if purchase_date else ""
        self.show_form = True

    def _reset_form_fields(self):
        self.is_editing = False
        self.editing_material_id = None
        self.material_name = ""
        self.material_type = "fabric"
        self.quantity_in_stock = 0.0
        self.unit = "meter"
        self.unit_price = 0.0
        self.reorder_level = 0.0
        self.supplier_name = ""
        self.supplier_contact = ""
        self.last_purchase_date = ""

    @rx.event
    def show_delete_confirmation(self, material: Material):
        self.show_delete_dialog = True
        self.material_to_delete = material

    @rx.event
    def cancel_delete(self):
        self.show_delete_dialog = False
        self.material_to_delete = None

    @rx.event
    async def delete_material(self):
        if self.material_to_delete:
            async with rx.asession() as session:
                await session.execute(
                    text("DELETE FROM materials WHERE material_id = :material_id"),
                    {"material_id": self.material_to_delete["material_id"]},
                )
                await session.commit()
            self.show_delete_dialog = False
            self.material_to_delete = None
            yield MaterialState.get_materials
            yield rx.toast.success("Material deleted successfully.")
        else:
            self.show_delete_dialog = False
            yield rx.toast.error("No material selected for deletion.")