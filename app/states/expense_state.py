import reflex as rx
from typing import cast, TypedDict
from sqlalchemy import text
import datetime


class ExpenseCategory(TypedDict):
    category_id: int
    category_name: str
    description: str | None


class Expense(TypedDict):
    expense_id: int
    category_id: int
    category_name: str
    amount: float
    expense_date: str
    description: str | None
    vendor_name: str | None


class ExpenseState(rx.State):
    is_loading: bool = False
    expenses: list[Expense] = []
    categories: list[ExpenseCategory] = []
    search_query: str = ""
    show_form: bool = False
    is_editing: bool = False
    editing_expense_id: int | None = None
    category_id: str = ""
    amount: float = 0.0
    expense_date: str = datetime.date.today().isoformat()
    description: str = ""
    vendor_name: str = ""

    @rx.var
    def filtered_expenses(self) -> list[Expense]:
        if not self.search_query.strip():
            return self.expenses
        lower_query = self.search_query.lower()
        return [
            e
            for e in self.expenses
            if lower_query in (e.get("description") or "").lower()
            or lower_query in (e.get("vendor_name") or "").lower()
            or lower_query in e["category_name"].lower()
        ]

    @rx.var
    def total_expenses(self) -> float:
        return sum((e["amount"] for e in self.expenses))

    @rx.event(background=True)
    async def get_expenses(self):
        async with self:
            self.is_loading = True
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT e.*, ec.category_name
                     FROM expenses e
                     JOIN expense_categories ec ON e.category_id = ec.category_id
                     ORDER BY e.expense_date DESC""")
            )
            async with self:
                self.expenses = [
                    cast(Expense, dict(row)) for row in result.mappings().all()
                ]
                self.is_loading = False

    @rx.event(background=True)
    async def load_form_data(self):
        async with rx.asession() as session:
            cat_result = await session.execute(
                text(
                    "SELECT * FROM expense_categories WHERE is_active = TRUE ORDER BY category_name"
                )
            )
            async with self:
                self.categories = [
                    cast(ExpenseCategory, dict(row))
                    for row in cat_result.mappings().all()
                ]

    def _reset_form(self):
        self.is_editing = False
        self.editing_expense_id = None
        self.category_id = ""
        self.amount = 0.0
        self.expense_date = datetime.date.today().isoformat()
        self.description = ""
        self.vendor_name = ""

    @rx.event
    def toggle_form(self):
        self.show_form = not self.show_form
        self._reset_form()
        if self.show_form:
            return ExpenseState.load_form_data

    @rx.event
    def start_editing(self, expense: Expense):
        self.is_editing = True
        self.editing_expense_id = expense["expense_id"]
        self.category_id = str(expense["category_id"])
        self.amount = float(expense["amount"])
        self.expense_date = str(expense["expense_date"]).split(" ")[0]
        self.description = expense.get("description") or ""
        self.vendor_name = expense.get("vendor_name") or ""
        self.show_form = True

    @rx.event(background=True)
    async def handle_form_submit(self, form_data: dict):
        async with self:
            is_editing = self.is_editing
        if is_editing:
            yield ExpenseState.update_expense(form_data)
        else:
            yield ExpenseState.add_expense(form_data)

    @rx.event(background=True)
    async def add_expense(self, form_data: dict):
        async with rx.asession() as session:
            await session.execute(
                text("""INSERT INTO expenses (category_id, amount, expense_date, description, vendor_name)
                     VALUES (:category_id, :amount, :expense_date, :description, :vendor_name)"""),
                form_data,
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield ExpenseState.get_expenses
        yield rx.toast.success("Expense added successfully!")

    @rx.event(background=True)
    async def update_expense(self, form_data: dict):
        async with self:
            editing_id = self.editing_expense_id
        if not editing_id:
            return
        form_data["expense_id"] = editing_id
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE expenses SET
                        category_id = :category_id,
                        amount = :amount,
                        expense_date = :expense_date,
                        description = :description,
                        vendor_name = :vendor_name
                     WHERE expense_id = :expense_id"""),
                form_data,
            )
            await session.commit()
        async with self:
            self.show_form = False
        yield ExpenseState.get_expenses
        yield rx.toast.success("Expense updated successfully!")