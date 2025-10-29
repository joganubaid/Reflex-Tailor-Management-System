import reflex as rx
from typing import Optional, cast
from sqlalchemy import text
import datetime
import logging


class PhotoState(rx.State):
    """State for managing photo uploads and display."""

    photos: list[dict] = []
    selected_photo_type: str = "order_photo"
    selected_reference_id: int = 0
    show_photo_uploader: bool = False
    show_photo_gallery: bool = False
    upload_caption: str = ""
    storage_preference: str = "local"
    upload_in_progress: bool = False
    upload_status_message: str = ""
    photo_to_send_url: str = ""

    @rx.event(background=True)
    async def get_photos_by_reference(self, photo_type: str, reference_id: int):
        """Fetch all photos for a specific entity (order, customer, etc.)."""
        async with rx.asession() as session:
            result = await session.execute(
                text("""SELECT * FROM photos 
                    WHERE photo_type = :photo_type AND reference_id = :reference_id 
                    ORDER BY upload_date DESC"""),
                {"photo_type": photo_type, "reference_id": reference_id},
            )
            rows = result.mappings().all()
            async with self:
                self.photos = [dict(row) for row in rows]

    @rx.event(background=True)
    async def get_all_photos_by_type(self, photo_type: str):
        """Get all photos of a specific type (e.g., all order photos)."""
        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT * FROM photos WHERE photo_type = :photo_type ORDER BY upload_date DESC"
                ),
                {"photo_type": photo_type},
            )
            rows = result.mappings().all()
            async with self:
                self.photos = [dict(row) for row in rows]

    @rx.event
    def open_photo_uploader(self, photo_type: str, reference_id: int):
        """Open photo upload dialog."""
        self.selected_photo_type = photo_type
        self.selected_reference_id = reference_id
        self.show_photo_uploader = True
        self.upload_caption = ""
        self.photos = []
        return PhotoState.get_photos_by_reference(photo_type, reference_id)

    @rx.event
    def close_photo_uploader(self):
        """Close photo upload dialog."""
        self.show_photo_uploader = False
        self.upload_in_progress = False
        self.upload_status_message = ""
        self.photos = []

    @rx.event
    async def handle_photo_upload(self, files: list[rx.UploadFile]):
        """Handle photo file uploads."""
        from app.utils.photo_storage import save_photo_locally, upload_to_supabase

        if not files:
            yield rx.toast.error("No file selected")
            return
        self.upload_in_progress = True
        yield rx.toast.info("Uploading photo(s)...")
        for upload_file in files:
            try:
                file_data = await upload_file.read()
                file_size = len(file_data)
                if self.storage_preference == "supabase":
                    file_path = upload_to_supabase(
                        file_data, upload_file.name, bucket_name="tailor-shop-photos"
                    )
                    storage_type = "supabase" if file_path else "local"
                    if not file_path:
                        file_path, _ = save_photo_locally(
                            file_data,
                            upload_file.name,
                            self.selected_photo_type,
                            self.selected_reference_id,
                        )
                        storage_type = "local"
                else:
                    file_path, _ = save_photo_locally(
                        file_data,
                        upload_file.name,
                        self.selected_photo_type,
                        self.selected_reference_id,
                    )
                    storage_type = "local"
                async with rx.asession() as session:
                    await session.execute(
                        text("""INSERT INTO photos (photo_type, reference_id, file_name, file_path, 
                                              storage_type, file_size, mime_type, caption, uploaded_by)
                            VALUES (:photo_type, :reference_id, :file_name, :file_path, 
                                   :storage_type, :file_size, :mime_type, :caption, :uploaded_by)"""),
                        {
                            "photo_type": self.selected_photo_type,
                            "reference_id": self.selected_reference_id,
                            "file_name": upload_file.name,
                            "file_path": file_path,
                            "storage_type": storage_type,
                            "file_size": file_size,
                            "mime_type": upload_file.content_type or "image/jpeg",
                            "caption": self.upload_caption or None,
                            "uploaded_by": "admin",
                        },
                    )
                    await session.commit()
                yield rx.toast.success(
                    f"Photo '{upload_file.name}' uploaded successfully!"
                )
            except Exception as e:
                logging.exception(f"Error: {e}")
                yield rx.toast.error(f"Upload failed: {str(e)}")
        self.upload_in_progress = False
        yield PhotoState.get_photos_by_reference(
            self.selected_photo_type, self.selected_reference_id
        )

    @rx.event(background=True)
    async def delete_photo(self, photo_id: int):
        """Delete a photo from storage and database."""
        from app.utils.photo_storage import delete_photo_file

        async with rx.asession() as session:
            result = await session.execute(
                text(
                    "SELECT file_path, storage_type FROM photos WHERE photo_id = :photo_id"
                ),
                {"photo_id": photo_id},
            )
            photo_data = result.mappings().first()
            if photo_data:
                delete_photo_file(photo_data["file_path"], photo_data["storage_type"])
                await session.execute(
                    text("DELETE FROM photos WHERE photo_id = :photo_id"),
                    {"photo_id": photo_id},
                )
                await session.commit()
        async with self:
            yield rx.toast.success("Photo deleted successfully!")
            yield PhotoState.get_photos_by_reference(
                self.selected_photo_type, self.selected_reference_id
            )

    @rx.event(background=True)
    async def approve_photo(self, photo_id: int):
        """Mark a photo as approved (for customer approval workflow)."""
        async with rx.asession() as session:
            await session.execute(
                text("""UPDATE photos 
                    SET is_approved = TRUE, approval_date = :approval_date 
                    WHERE photo_id = :photo_id"""),
                {"photo_id": photo_id, "approval_date": datetime.datetime.now()},
            )
            await session.commit()
        async with self:
            yield rx.toast.success("Photo approved!")
            yield PhotoState.get_photos_by_reference(
                self.selected_photo_type, self.selected_reference_id
            )

    @rx.event(background=True)
    async def send_photo_for_approval(self, photo_id: int):
        from app.utils.whatsapp import send_whatsapp_order_photo_for_approval
        from app.utils.photo_storage import get_photo_url

        async with rx.asession() as session:
            photo_result = await session.execute(
                text("SELECT * FROM photos WHERE photo_id = :id"), {"id": photo_id}
            )
            photo = photo_result.mappings().first()
            if not photo or photo.get("photo_type") != "order_photo":
                yield rx.toast.error("Invalid photo for approval")
                return
            order_result = await session.execute(
                text(
                    "SELECT c.name, c.phone_number FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id = :order_id"
                ),
                {"order_id": photo.get("reference_id")},
            )
            customer = order_result.mappings().first()
        if not customer:
            yield rx.toast.error("Customer not found for this order")
            return
        async with self:
            photo_url = get_photo_url(photo["file_path"], photo["storage_type"])
            self.photo_to_send_url = str(photo_url)
        sent = send_whatsapp_order_photo_for_approval(
            customer_phone=customer["phone_number"],
            customer_name=customer["name"],
            order_id=photo.get("reference_id"),
            photo_url=self.photo_to_send_url,
        )
        if sent:
            yield rx.toast.success("Photo sent for approval via WhatsApp!")
        else:
            yield rx.toast.error("Failed to send photo via WhatsApp.")