"""Supabase database and storage operations."""
import logging
from pathlib import Path
from typing import Optional

from supabase import create_client, Client

logger = logging.getLogger(__name__)


def get_supabase_client(url: str, service_key: str) -> Client:
    """Create a Supabase client with service role key."""
    return create_client(url, service_key)


async def upload_image(
    supabase: Client, local_path: Path, folder: str
) -> Optional[str]:
    """
    Upload an image to Supabase Storage.

    Args:
        supabase: Supabase client
        local_path: Path to local image file
        folder: Storage folder path (e.g., "covers" or "chapters/uuid")

    Returns:
        Public URL of uploaded image, or None if upload fails
    """
    if not local_path.exists():
        logger.warning(f"Image file not found: {local_path}")
        return None

    storage_path = f"{folder}/{local_path.name}"

    try:
        with open(local_path, "rb") as f:
            file_bytes = f.read()

        # Upload with upsert (overwrite if exists)
        supabase.storage.from_("ebook-covers").upload(
            storage_path,
            file_bytes,
            {"upsert": "true", "content-type": "image/png"},
        )

        # Get public URL
        public_url = supabase.storage.from_("ebook-covers").get_public_url(storage_path)
        logger.info(f"Uploaded image: {storage_path}")
        return public_url

    except Exception as e:
        logger.error(f"Failed to upload image {local_path}: {e}")
        return None


async def insert_ebook(
    ebook_data: dict,
    supabase_url: str,
    service_key: str,
    images_dir: Path,
) -> str:
    """
    Insert ebook and chapters into Supabase database.

    Args:
        ebook_data: Dict with 'ebook' and 'chapters' keys
        supabase_url: Supabase project URL
        service_key: Supabase service role key
        images_dir: Directory containing generated images

    Returns:
        UUID of the created ebook
    """
    supabase = get_supabase_client(supabase_url, service_key)
    ebook = ebook_data["ebook"]
    chapters = ebook_data["chapters"]

    # Upload cover image if it exists locally
    cover_url = ebook.get("cover_image_url", "")
    if cover_url.startswith("images/"):
        local_path = images_dir / cover_url.replace("images/", "")
        uploaded_url = await upload_image(supabase, local_path, "covers")
        if uploaded_url:
            cover_url = uploaded_url

    # Calculate total read time
    total_read_time = sum(ch.get("estimated_read_time_minutes", 0) for ch in chapters)

    # Insert ebook record
    result = (
        supabase.table("ebooks")
        .insert(
            {
                "title_en": ebook["title_en"],
                "title_pt": ebook.get("title_pt"),
                "slug": ebook["slug"],
                "description_en": ebook.get("description_en"),
                "description_pt": ebook.get("description_pt"),
                "cover_image_url": cover_url,
                "price_usd": ebook.get("price_usd", 1997),
                "price_brl": ebook.get("price_brl", 9970),
                "estimated_read_time_minutes": total_read_time,
                "status": "draft",
            }
        )
        .execute()
    )

    ebook_id = result.data[0]["id"]
    logger.info(f"Created ebook: {ebook_id} - {ebook['title_en']}")

    # Insert chapters
    for ch in chapters:
        # Upload chapter image if exists
        ch_cover = ch.get("cover_image_url", "")
        if ch_cover.startswith("images/"):
            local_path = images_dir / ch_cover.replace("images/", "")
            uploaded_url = await upload_image(
                supabase, local_path, f"chapters/{ebook_id}"
            )
            if uploaded_url:
                ch_cover = uploaded_url

        supabase.table("chapters").insert(
            {
                "ebook_id": ebook_id,
                "chapter_number": ch["chapter_number"],
                "title_en": ch["title_en"],
                "title_pt": ch.get("title_pt"),
                "slug": ch["slug"],
                "cover_image_url": ch_cover,
                "content_en": ch.get("content_en"),
                "content_pt": ch.get("content_pt"),
                "summary_en": ch.get("summary_en"),
                "summary_pt": ch.get("summary_pt"),
                "estimated_read_time_minutes": ch.get("estimated_read_time_minutes", 0),
                "is_free_preview": ch.get("is_free_preview", False),
                "is_published": False,
            }
        ).execute()

        logger.info(f"  Created chapter {ch['chapter_number']}: {ch['title_en']}")

    return ebook_id
