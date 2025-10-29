import reflex as rx
from app.states.photo_state import PhotoState
from app.utils.photo_storage import get_photo_url


def photo_gallery_card(photo: rx.Var[dict]) -> rx.Component:
    """Individual photo card for gallery view."""
    return rx.el.div(
        rx.el.image(
            src=get_photo_url(photo["file_path"], photo["storage_type"]),
            alt=photo["caption"].to_string(),
            class_name="w-full h-48 object-cover rounded-t-lg",
        ),
        rx.el.div(
            rx.el.p(
                rx.cond(photo["caption"], photo["caption"], "No caption"),
                class_name="text-sm text-gray-600 mb-2 truncate",
            ),
            rx.el.p(
                photo["upload_date"].to_string().split("T")[0],
                class_name="text-xs text-gray-400",
            ),
            rx.el.div(
                rx.cond(
                    photo["is_approved"],
                    rx.el.div(
                        rx.icon("square_check", class_name="h-4 w-4 mr-1"),
                        "Approved",
                        class_name="flex items-center text-xs text-green-600 font-semibold",
                    ),
                    rx.el.button(
                        "Approve",
                        on_click=lambda: PhotoState.approve_photo(photo["photo_id"]),
                        class_name="text-xs px-2 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200",
                    ),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: PhotoState.delete_photo(photo["photo_id"]),
                    class_name="p-1 text-red-500 hover:bg-red-100 rounded-full",
                ),
                class_name="flex justify-between items-center mt-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("send", class_name="h-4 w-4"),
                    on_click=lambda: PhotoState.send_photo_for_approval(
                        photo["photo_id"]
                    ),
                    class_name="p-1 text-blue-500 hover:bg-blue-100 rounded-full",
                ),
                class_name="flex justify-end items-center mt-2",
            ),
            class_name="p-3",
        ),
        class_name="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow bg-white",
    )


def photo_gallery() -> rx.Component:
    """Photo gallery grid component."""
    return rx.el.div(
        rx.cond(
            PhotoState.photos.length() > 0,
            rx.el.div(
                rx.foreach(PhotoState.photos, photo_gallery_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4",
            ),
            rx.el.div(
                rx.icon("image-off", class_name="h-12 w-12 text-gray-400 mb-4"),
                rx.el.p("No photos uploaded yet", class_name="text-gray-600"),
                class_name="flex flex-col items-center justify-center text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed",
            ),
        ),
        class_name="mt-6",
    )


def photo_upload_dialog() -> rx.Component:
    """Photo upload dialog component."""
    upload_id = "photo_upload_area"
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Manage Photos", class_name="text-2xl font-bold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.upload.root(
                        rx.el.div(
                            rx.icon("cloud_upload", class_name="h-8 w-8 text-gray-500"),
                            rx.el.p(
                                "Click or drag to upload",
                                class_name="mt-2 text-sm text-gray-600",
                            ),
                            class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50",
                        ),
                        id=upload_id,
                        accept={
                            "image/png": [".png"],
                            "image/jpeg": [".jpg", ".jpeg"],
                            "image/webp": [".webp"],
                        },
                        multiple=True,
                        max_files=5,
                        class_name="w-full mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            rx.selected_files(upload_id),
                            lambda file: rx.el.div(
                                rx.el.p(file, class_name="text-xs truncate"),
                                class_name="p-2 bg-purple-50 rounded border border-purple-100 text-sm",
                            ),
                        ),
                        class_name="mt-2 space-y-2 max-h-24 overflow-y-auto",
                    ),
                    rx.el.input(
                        placeholder="Caption for all photos (optional)",
                        on_change=PhotoState.set_upload_caption,
                        class_name="w-full p-2 border rounded-lg mt-4",
                        default_value=PhotoState.upload_caption,
                    ),
                    rx.el.button(
                        "Upload",
                        on_click=PhotoState.handle_photo_upload(
                            rx.upload_files(upload_id=upload_id)
                        ),
                        class_name="w-full mt-4 py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold",
                        disabled=PhotoState.upload_in_progress,
                    ),
                    class_name="p-4 border rounded-lg bg-gray-50 mb-6",
                ),
                photo_gallery(),
                class_name="max-h-[60vh] overflow-y-auto pr-2",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        on_click=PhotoState.close_photo_uploader,
                        class_name="py-2 px-4 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 font-semibold",
                    )
                ),
                class_name="flex justify-end gap-4 mt-6 pt-4 border-t",
            ),
            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 w-[56rem] max-w-[95vw]",
        ),
        open=PhotoState.show_photo_uploader,
        on_open_change=PhotoState.set_show_photo_uploader,
    )