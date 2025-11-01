import reflex as rx
from app.states.purchase_order_state import PurchaseOrderState
from app.components.sidebar import sidebar, mobile_header


def purchase_order_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.dialog.title(
                    "Create Purchase Order", class_name="text-2xl font-bold mb-4"
                ),
                rx.el.div(
                    rx.el.label("Supplier", class_name="font-semibold"),
                    rx.el.select(
                        rx.foreach(
                            PurchaseOrderState.available_suppliers,
                            lambda s: rx.el.option(
                                s["name"], value=s["supplier_id"].to_string()
                            ),
                        ),
                        value=PurchaseOrderState.selected_supplier_id,
                        on_change=PurchaseOrderState.set_selected_supplier_id,
                        class_name="w-full p-2 border rounded",
                        name="supplier_id",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.h3("Add Item", class_name="text-lg font-semibold mb-2"),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Select material...", value=""),
                            rx.foreach(
                                PurchaseOrderState.available_materials,
                                lambda m: rx.el.option(
                                    m["material_name"],
                                    value=m["material_id"].to_string(),
                                ),
                            ),
                            on_change=PurchaseOrderState.on_material_select,
                            class_name="p-2 border rounded w-full",
                            name="material_id",
                        ),
                        rx.el.input(
                            name="item_quantity",
                            placeholder="Qty",
                            type="number",
                            class_name="p-2 border rounded w-24",
                            default_value=PurchaseOrderState.item_quantity.to_string(),
                        ),
                        rx.el.input(
                            name="item_unit_price",
                            placeholder="Unit Price",
                            type="number",
                            class_name="p-2 border rounded w-28",
                            default_value=PurchaseOrderState.item_unit_price.to_string(),
                        ),
                        rx.el.button(
                            "Add",
                            type="button",
                            on_click=PurchaseOrderState.add_po_item,
                            class_name="bg-blue-500 text-white px-3 py-2 rounded",
                        ),
                        class_name="flex items-center gap-2 mb-4",
                    ),
                ),
                rx.el.div(
                    rx.el.h4("Order Items", class_name="font-semibold mb-2"),
                    rx.foreach(
                        PurchaseOrderState.po_items,
                        lambda item, index: rx.el.div(
                            rx.el.p(item.material_name),
                            rx.el.p(
                                f"{item.quantity} x ₹{item.unit_price} = ₹{item.quantity * item.unit_price}"
                            ),
                            rx.el.button(
                                rx.icon("x"),
                                on_click=lambda: PurchaseOrderState.remove_po_item(
                                    index
                                ),
                            ),
                            class_name="flex justify-between items-center p-2 bg-gray-100 rounded",
                        ),
                    ),
                    rx.el.p(
                        f"Total: ₹{PurchaseOrderState.po_total.to_string()}",
                        class_name="font-bold text-right mt-2",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=PurchaseOrderState.toggle_po_form,
                        class_name="bg-gray-300 px-4 py-2 rounded",
                    ),
                    rx.el.button(
                        "Create PO",
                        type="submit",
                        class_name="bg-green-500 text-white px-4 py-2 rounded",
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                on_submit=PurchaseOrderState.create_purchase_order,
            ),
            class_name="p-6 bg-white rounded-lg",
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
                    rx.el.button(
                        "Create PO",
                        on_click=PurchaseOrderState.toggle_po_form,
                        class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Suggested Purchase Orders (Low Stock)",
                        class_name="text-xl font-semibold mb-4",
                    ),
                    rx.cond(
                        PurchaseOrderState.suggested_pos.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                PurchaseOrderState.suggested_pos,
                                lambda po: rx.el.div(
                                    rx.el.p(po.supplier_name, class_name="font-bold"),
                                    rx.el.p(
                                        f"{po.item_count} items, Total: ₹{po.total_amount}"
                                    ),
                                    rx.el.button(
                                        "Create PO",
                                        on_click=lambda: PurchaseOrderState.create_suggested_po(
                                            po
                                        ),
                                        class_name="text-sm bg-blue-500 text-white px-2 py-1 rounded",
                                    ),
                                    class_name="p-4 bg-yellow-100 rounded-lg",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",
                        ),
                        rx.el.p(
                            "All materials are well-stocked.",
                            class_name="text-gray-500",
                        ),
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Purchase Order History",
                        class_name="text-xl font-semibold mb-4",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th("PO ID"),
                                    rx.el.th("Supplier"),
                                    rx.el.th("Date"),
                                    rx.el.th("Total"),
                                    rx.el.th("Status"),
                                    rx.el.th("Actions"),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    PurchaseOrderState.purchase_orders,
                                    lambda po: rx.el.tr(
                                        rx.el.td(po.po_id.to_string()),
                                        rx.el.td(po.supplier_name),
                                        rx.el.td(po.po_date.to_string().split("T")[0]),
                                        rx.el.td(f"₹{po.total_amount}"),
                                        rx.el.td(po.status.capitalize()),
                                        rx.el.td(
                                            rx.el.button(
                                                "Receive",
                                                on_click=lambda: PurchaseOrderState.receive_purchase_order(
                                                    po.po_id
                                                ),
                                                disabled=po.status == "received",
                                            )
                                        ),
                                    ),
                                )
                            ),
                        ),
                        class_name="overflow-x-auto bg-white p-4 rounded-xl shadow-sm",
                    ),
                ),
                purchase_order_form(),
                class_name="p-4 md:p-8",
            ),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )