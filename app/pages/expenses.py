import reflex as rx
from app.states.expense_state import ExpenseState
from app.components.sidebar import sidebar


def expense_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    rx.cond(ExpenseState.is_editing, "Edit Expense", "Add New Expense"),
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Category", class_name="block text-sm font-semibold mb-2"
                        ),
                        rx.el.select(
                            rx.el.option("Select Category", value="", disabled=True),
                            rx.foreach(
                                ExpenseState.categories,
                                lambda c: rx.el.option(
                                    c["category_name"],
                                    value=c["category_id"].to_string(),
                                ),
                            ),
                            name="category_id",
                            value=ExpenseState.category_id,
                            on_change=ExpenseState.set_category_id,
                            class_name="w-full p-3 bg-white border rounded-lg",
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Amount", class_name="block text-sm font-semibold mb-2"
                        ),
                        rx.el.input(
                            name="amount",
                            type="number",
                            default_value=ExpenseState.amount.to_string(),
                            class_name="w-full p-3 bg-white border rounded-lg",
                            required=True,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Expense Date", class_name="block text-sm font-semibold mb-2"
                    ),
                    rx.el.input(
                        name="expense_date",
                        type="date",
                        default_value=ExpenseState.expense_date,
                        class_name="w-full p-3 bg-white border rounded-lg",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description", class_name="block text-sm font-semibold mb-2"
                    ),
                    rx.el.textarea(
                        name="description",
                        default_value=ExpenseState.description,
                        class_name="w-full p-3 bg-white border rounded-lg",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Vendor (Optional)",
                        class_name="block text-sm font-semibold mb-2",
                    ),
                    rx.el.input(
                        name="vendor_name",
                        default_value=ExpenseState.vendor_name,
                        class_name="w-full p-3 bg-white border rounded-lg",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=ExpenseState.toggle_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 font-semibold",
                        )
                    ),
                    rx.el.button(
                        rx.cond(ExpenseState.is_editing, "Save Changes", "Add Expense"),
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white font-semibold",
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                on_submit=ExpenseState.handle_form_submit,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg w-[36rem]",
        ),
        open=ExpenseState.show_form,
        on_open_change=ExpenseState.set_show_form,
    )


def expense_row(expense: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            expense["expense_date"].to_string().split("T")[0], class_name="px-6 py-4"
        ),
        rx.el.td(
            expense["category_name"].capitalize(),
            class_name="px-6 py-4 font-medium text-gray-900",
        ),
        rx.el.td(expense["description"], class_name="px-6 py-4 text-sm text-gray-600"),
        rx.el.td(
            f"₹{expense['amount'].to_string()}",
            class_name="px-6 py-4 font-semibold text-red-600",
        ),
        rx.el.td(expense["vendor_name"], class_name="px-6 py-4"),
        rx.el.td(
            rx.el.button(
                rx.icon("copy", class_name="h-4 w-4"),
                on_click=lambda: ExpenseState.start_editing(expense),
                class_name="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-md",
            ),
            class_name="px-6 py-4 text-center",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def expenses_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Expense Tracking", class_name="text-3xl font-bold text-gray-800"
                ),
                rx.el.p(
                    "Record and manage all your business expenses.",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search expenses...",
                        on_change=ExpenseState.set_search_query,
                        class_name="w-full md:w-80 pl-10 pr-4 py-2 border rounded-lg",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    rx.el.span("Total Expenses:", class_name="font-semibold"),
                    rx.el.span(
                        f"₹{ExpenseState.total_expenses.to_string()}",
                        class_name="font-bold text-red-600 text-lg",
                    ),
                    class_name="flex items-center gap-2 bg-red-50 p-2 rounded-lg",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-5 w-5"),
                    "Add Expense",
                    on_click=ExpenseState.toggle_form,
                    class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Date",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Category",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Description",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Amount",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Vendor",
                                    class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                ),
                                rx.el.th(
                                    "Action",
                                    class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(ExpenseState.filtered_expenses, expense_row)
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    rx.cond(
                        ExpenseState.filtered_expenses.length() == 0,
                        rx.el.div(
                            rx.el.p(
                                "No expenses recorded yet.",
                                class_name="text-center text-gray-500 py-8",
                            )
                        ),
                        None,
                    ),
                    class_name="overflow-hidden border border-gray-200 rounded-xl",
                ),
                class_name="bg-white p-6 rounded-xl shadow-sm",
            ),
            expense_form(),
            class_name="flex-1 p-6 md:p-8 overflow-auto",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )