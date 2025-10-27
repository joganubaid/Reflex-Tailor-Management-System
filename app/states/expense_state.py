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
        return []

    @rx.var
    def total_expenses(self) -> float:
        return 0.0

    @rx.event
    async def get_expenses(self):
        self.expenses = []

    @rx.event
    async def load_form_data(self):
        self.categories = []

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

    @rx.event
    def start_editing(self, expense: Expense):
        pass

    @rx.event
    async def handle_form_submit(self, form_data: dict):
        pass

    @rx.event
    async def add_expense(self, form_data: dict):
        pass

    @rx.event
    async def update_expense(self, form_data: dict):
        pass