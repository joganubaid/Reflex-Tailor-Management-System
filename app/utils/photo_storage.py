import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import mimetypes
import reflex as rx

LOCAL_UPLOAD_DIR = Path("uploaded_photos")
LOCAL_UPLOAD_DIR.mkdir(exist_ok=True)
for subdir in ["orders", "customers", "materials", "measurements", "invoices"]:
    (LOCAL_UPLOAD_DIR / subdir).mkdir(exist_ok=True)


def get_photo_subdirectory(photo_type: str) -> str:
    """Map photo type to subdirectory name."""
    type_mapping = {
        "order_photo": "orders",
        "customer_reference": "customers",
        "material_photo": "materials",
        "measurement_photo": "measurements",
        "invoice_receipt": "invoices",
    }
    return type_mapping.get(photo_type, "misc")


def generate_unique_filename(
    original_filename: str, photo_type: str, reference_id: int
) -> str:
    """Generate a unique filename to prevent collisions."""
    ext = Path(original_filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{photo_type}_{reference_id}_{timestamp}_{unique_id}{ext}"


def save_photo_locally(
    file_data: bytes, original_filename: str, photo_type: str, reference_id: int
) -> tuple[str, str]:
    """
    Save photo to local file system.
    Returns: (file_path, file_name)
    """
    subdir = get_photo_subdirectory(photo_type)
    unique_filename = generate_unique_filename(
        original_filename, photo_type, reference_id
    )
    upload_dir = rx.get_upload_dir() / subdir
    upload_dir.mkdir(parents=True, exist_ok=True)
    full_path = upload_dir / unique_filename
    with open(full_path, "wb") as f:
        f.write(file_data)
    relative_path = f"{subdir}/{unique_filename}"
    return (relative_path, unique_filename)


def get_photo_url(file_path: str, storage_type: str = "local") -> str:
    """
    Get the URL/path to access a photo.
    For local storage, returns the file system path.
    For Supabase, returns the CDN URL.
    """
    return rx.cond(
        storage_type == "local",
        rx.get_upload_url(file_path),
        rx.cond(storage_type == "supabase", file_path, file_path),
    )


def delete_photo_file(file_path: str, storage_type: str = "local") -> bool:
    """Delete photo file from storage."""
    try:
        if storage_type == "local":
            full_path = rx.get_upload_dir() / file_path
            if full_path.exists():
                full_path.unlink()
                return True
        elif storage_type == "supabase":
            pass
        return False
    except Exception as e:
        logging.exception(f"Error deleting photo: {e}")
        return False


def upload_to_supabase(
    file_data: bytes, filename: str, bucket_name: str = "tailor-shop-photos"
) -> Optional[str]:
    """
    Upload photo to Supabase Storage.
    Returns the public URL if successful, None otherwise.
    """
    try:
        from supabase import create_client

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not supabase_url or not supabase_key:
            print("Supabase credentials not configured")
            return None
        supabase = create_client(supabase_url, supabase_key)
        response = supabase.storage.from_(bucket_name).upload(
            path=filename,
            file=file_data,
            file_options={
                "content-type": mimetypes.guess_type(filename)[0] or "image/jpeg"
            },
        )
        public_url = supabase.storage.from_(bucket_name).get_public_url(filename)
        return public_url
    except Exception as e:
        logging.exception(f"Supabase upload failed: {e}")
        return None