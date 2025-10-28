import reflex as rx
from app.states.purchase_order_state import PurchaseOrderState, PurchaseOrderItem
from app.components.sidebar import sidebar, mobile_header

STATUS_COLORS = {
    "pending": "bg-yellow-100 text-yellow-800",
    "ordered": "bg-blue-100 text-blue-800",
    "received": "bg-green-100 text-green-800",
    "cancelled": "bg-red-100 text-red-800",
}


def status_badge(status: rx.Var[str]) -> rx.Component:
    base_classes = " px-2.5 py-0.5 text-xs font-medium rounded-full w-fit capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status.lower(),
            ("pending", STATUS_COLORS["pending"] + base_classes),
            ("ordered", STATUS_COLORS["ordered"] + base_classes),
            ("received", STATUS_COLORS["received"] + base_classes),
            ("cancelled", STATUS_COLORS["cancelled"] + base_classes),
            "bg-gray-100 text-gray-800" + base_classes,
        ),
    )


def suggested_po_card(suggested_po: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                suggested_po["supplier_name"], class_name="font-bold text-gray-800"
            ),
            rx.el.span(
                f"{suggested_po['item_count']} items",
                class_name="text-sm text-gray-500",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Est. Total", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"₹{suggested_po['total_amount'].to_string()}",
                    class_name="font-bold text-purple-600",
                ),
            ),
            rx.el.button(
                "Create PO",
                on_click=lambda: PurchaseOrderState.create_suggested_po(suggested_po),
                class_name="flex items-center bg-purple-600 text-white px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-purple-700",
            ),
            class_name="flex justify-between items-center mt-3 pt-3 border-t",
        ),
        class_name="bg-purple-50 p-4 rounded-xl border border-purple-200 shadow-sm",
    )


def po_card(po: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(f"PO #{po['po_id']}", class_name="font-bold text-gray-800"),
            status_badge(po["status"]),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.p(po["supplier_name"], class_name="text-sm text-gray-600"),
        rx.el.div(
            rx.el.div(
                rx.el.p("Order Date", class_name="text-xs text-gray-500"),
                rx.el.p(
                    po["po_date"].to_string().split("T")[0], class_name="font-medium"
                ),
            ),
            rx.el.div(
                rx.el.p("Total", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"⁷{po['total_amount']}", class_name="font-bold text-purple-600"
                ),
            ),
            class_name="grid grid-cols-2 gap-4 mt-3 pt-3 border-t",
        ),
        rx.el.div(
            rx.el.div(),
            rx.el.div(
                rx.cond(
                    po["status"] == "pending",
                    rx.el.button(
                        "Mark Ordered",
                        on_click=lambda: PurchaseOrderState.update_po_status(
                            po["po_id"], "ordered"
                        ),
                        class_name="px-3 py-1.5 text-xs bg-blue-100 text-blue-700 rounded-md font-semibold",
                    ),
                    None,
                ),
                rx.cond(
                    po["status"] == "ordered",
                    rx.el.button(
                        "Mark Received",
                        on_click=lambda: PurchaseOrderState.update_po_status(
                            po["po_id"], "received"
                        ),
                        class_name="px-3 py-1.5 text-xs bg-green-100 text-green-700 rounded-md font-semibold",
                    ),
                    None,
                ),
                class_name="flex gap-2 justify-end",
            ),
            class_name="flex justify-between items-center mt-3 pt-3 border-t",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def po_row(po: rx.Var[dict]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(f"#{po['po_id']}", class_name="px-6 py-4 font-medium text-gray-900"),
        rx.el.td(po["supplier_name"], class_name="px-6 py-4"),
        rx.el.td(po["po_date"].to_string().split("T")[0], class_name="px-6 py-4"),
        rx.el.td(status_badge(po["status"]), class_name="px-6 py-4"),
        rx.el.td(
            f"₹{po['total_amount'].to_string()}", class_name="px-6 py-4 font-semibold"
        ),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    po["status"] == "pending",
                    rx.el.button(
                        "Mark Ordered",
                        on_click=lambda: PurchaseOrderState.update_po_status(
                            po["po_id"], "ordered"
                        ),
                        class_name="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded",
                    ),
                    None,
                ),
                rx.cond(
                    po["status"] == "ordered",
                    rx.el.button(
                        "Mark Received",
                        on_click=lambda: PurchaseOrderState.update_po_status(
                            po["po_id"], "received"
                        ),
                        class_name="px-2 py-1 text-xs bg-green-100 text-green-700 rounded",
                    ),
                    None,
                ),
                class_name="flex gap-2",
            ),
            class_name="px-6 py-4 text-center",
        ),
        class_name="border-b bg-white hover:bg-gray-50/50",
    )


def po_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    "Create Purchase Order",
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.label("Supplier", class_name="block text-sm font-semibold"),
                    rx.el.select(
                        rx.el.option("Select Supplier", value="", disabled=True),
                        rx.foreach(
                            PurchaseOrderState.available_suppliers,
                            lambda s: rx.el.option(
                                s["name"], value=s["supplier_id"].to_string()
                            ),
                        ),
                        value=PurchaseOrderState.selected_supplier_id,
                        on_change=PurchaseOrderState.set_selected_supplier_id,
                        class_name="w-full p-2 border rounded-md mt-1",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Expected Delivery Date",
                        class_name="block text-sm font-semibold",
                    ),
                    rx.el.input(
                        type="date",
                        name="expected_delivery_date",
                        default_value=PurchaseOrderState.expected_delivery_date,
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.h3(
                    "Order Items",
                    class_name="text-lg font-bold mt-6 mb-2 border-t pt-4",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Select Material", value="", disabled=True),
                        rx.foreach(
                            PurchaseOrderState.available_materials,
                            lambda m: rx.el.option(
                                f"{m['material_name']} ({m['unit']})",
                                value=m["material_id"].to_string(),
                            ),
                        ),
                        value=PurchaseOrderState.selected_material_id,
                        on_change=PurchaseOrderState.on_material_select,
                        class_name="flex-1 p-2 border rounded-md",
                    ),
                    rx.el.input(
                        type="number",
                        placeholder="Qty",
                        name="item_quantity",
                        default_value=PurchaseOrderState.item_quantity.to_string(),
                        class_name="w-24 p-2 border rounded-md",
                    ),
                    rx.el.input(
                        type="number",
                        placeholder="Unit Price",
                        name="item_unit_price",
                        class_name="w-28 p-2 border rounded-md",
                        default_value=PurchaseOrderState.item_unit_price.to_string(),
                    ),
                    rx.el.button(
                        rx.icon("plus"),
                        on_click=PurchaseOrderState.add_po_item,
                        class_name="p-2 bg-purple-600 text-white rounded-md",
                    ),
                    class_name="flex items-center gap-2 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        PurchaseOrderState.po_items,
                        lambda item, index: rx.el.div(
                            rx.el.p(
                                item.material_name, class_name="flex-1 font-medium"
                            ),
                            rx.el.p(f"{item.quantity} x ₹{item.unit_price}"),
                            rx.el.p(
                                f"₹{item.quantity * item.unit_price}",
                                class_name="font-semibold w-24 text-right",
                            ),
                            rx.el.button(
                                rx.icon("x", class_name="h-4 w-4"),
                                on_click=lambda: PurchaseOrderState.remove_po_item(
                                    index
                                ),
                                class_name="p-1 text-red-500 hover:bg-red-100 rounded-full",
                            ),
                            class_name="flex items-center gap-4 p-2 border-b",
                        ),
                    ),
                    class_name="max-h-64 overflow-y-auto mb-4",
                ),
                rx.cond(
                    PurchaseOrderState.po_items.length() > 0,
                    rx.el.div(
                        rx.el.p("Total:", class_name="font-bold text-xl"),
                        rx.el.p(
                            f"₹{PurchaseOrderState.po_total.to_string()}",
                            class_name="font-bold text-xl text-purple-700",
                        ),
                        class_name="flex justify-end items-center gap-4 mt-4 p-4 bg-gray-50 rounded-lg",
                    ),
                    None,
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            on_click=PurchaseOrderState.toggle_po_form,
                            class_name="py-2 px-4 rounded-lg bg-gray-200 font-semibold",
                        )
                    ),
                    rx.el.button(
                        "Create PO",
                        type="submit",
                        class_name="py-2 px-4 rounded-lg bg-purple-600 text-white font-semibold",
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                on_submit=PurchaseOrderState.create_purchase_order,
                reset_on_submit=True,
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg w-[48rem]",
        ),
        open=PurchaseOrderState.show_po_form,
        on_open_change=PurchaseOrderState.set_show_po_form,
    )


def purchase_orders_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Purchase Orders", class_name="text-3xl font-bold text-gray-800"
                    ),
                    rx.el.p(
                        "Manage procurement of materials from suppliers.",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.cond(
                    PurchaseOrderState.suggested_pos.length() > 0,
                    rx.el.div(
                        rx.el.h2(
                            "Suggested Purchase Orders",
                            class_name="text-xl font-semibold text-gray-700 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                PurchaseOrderState.suggested_pos, suggested_po_card
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                        ),
                        class_name="mb-8",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.div(class_name="flex-1"),
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2 h-5 w-5"),
                        "Create PO",
                        on_click=PurchaseOrderState.toggle_po_form,
                        class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(PurchaseOrderState.purchase_orders, po_card),
                        class_name="grid grid-cols-1 gap-4 md:hidden",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "PO ID",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Supplier",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Order Date",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Status",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Total",
                                            class_name="px-6 py-3 text-left text-xs font-bold uppercase",
                                        ),
                                        rx.el.th(
                                            "Actions",
                                            class_name="px-6 py-3 text-center text-xs font-bold uppercase",
                                        ),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        PurchaseOrderState.purchase_orders, po_row
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.cond(
                            PurchaseOrderState.purchase_orders.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "file-stack",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "No Purchase Orders Found",
                                    class_name="text-lg font-semibold",
                                ),
                                rx.el.p(
                                    "Create your first purchase order to start restocking.",
                                    class_name="text-gray-500 mt-1",
                                ),
                                class_name="text-center py-16",
                            ),
                            None,
                        ),
                        class_name="hidden md:block overflow-hidden border border-gray-200 rounded-xl",
                    ),
                    class_name="md:bg-white md:p-6 rounded-xl shadow-sm",
                ),
                po_form(),
                class_name="flex-1 p-4 md:p-8 overflow-auto",
            ),
            class_name="flex flex-col w-full",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )