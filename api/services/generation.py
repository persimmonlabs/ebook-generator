"""Background task generation services."""
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from ..job_store import update_job, JobStatus
from .supabase import insert_ebook

logger = logging.getLogger(__name__)


def _get_ebook_generator():
    """Lazy import of EbookGenerator to avoid import errors at startup."""
    # Add parent directory to path for importing generator
    parent_dir = str(Path(__file__).parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from generator import EbookGenerator
    return EbookGenerator


async def run_pdf_generation(
    job_id: str,
    pdf_en_bytes: bytes,
    pdf_pt_bytes: bytes,
    openrouter_key: str,
    supabase_url: str,
    supabase_service_key: str,
) -> None:
    """
    Background task for PDF-based ebook generation.

    Args:
        job_id: Job ID for progress tracking
        pdf_en_bytes: English PDF file contents
        pdf_pt_bytes: Portuguese PDF file contents
        openrouter_key: OpenRouter API key
        supabase_url: Supabase project URL
        supabase_service_key: Supabase service role key
    """
    try:
        update_job(
            job_id,
            status=JobStatus.PROCESSING,
            current_step="Initializing",
            progress=5,
        )
        logger.info(f"Job {job_id}: Starting PDF generation")

        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Write uploaded PDFs to temp files
            pdf_en_path = tmp_path / "ebook_en.pdf"
            pdf_pt_path = tmp_path / "ebook_pt.pdf"
            pdf_en_path.write_bytes(pdf_en_bytes)
            pdf_pt_path.write_bytes(pdf_pt_bytes)

            update_job(
                job_id, current_step="Extracting PDF content", progress=10
            )

            # Use existing EbookGenerator (lazy import)
            EbookGenerator = _get_ebook_generator()
            generator = EbookGenerator(openrouter_key, tmp_path)

            update_job(
                job_id, current_step="Processing with AI (this takes a few minutes)", progress=15
            )

            # This is the long-running operation (2-10 minutes)
            ebook_data = await generator.generate_from_pdfs(pdf_en_path, pdf_pt_path)

            update_job(
                job_id, current_step="Uploading images and saving to database", progress=85
            )

            # Insert into Supabase
            ebook_id = await insert_ebook(
                ebook_data,
                supabase_url,
                supabase_service_key,
                tmp_path / "images",
            )

            update_job(
                job_id,
                status=JobStatus.COMPLETED,
                ebook_id=ebook_id,
                current_step="Complete",
                progress=100,
            )
            logger.info(f"Job {job_id}: Completed. Ebook ID: {ebook_id}")

    except Exception as e:
        logger.exception(f"Job {job_id}: Failed")
        update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e),
            current_step="Failed",
        )


async def run_text_generation(
    job_id: str,
    topic: str,
    num_chapters: int,
    openrouter_key: str,
    supabase_url: str,
    supabase_service_key: str,
) -> None:
    """
    Background task for topic-based ebook generation.

    Args:
        job_id: Job ID for progress tracking
        topic: Topic/prompt for ebook generation
        num_chapters: Number of chapters to generate
        openrouter_key: OpenRouter API key
        supabase_url: Supabase project URL
        supabase_service_key: Supabase service role key
    """
    try:
        update_job(
            job_id,
            status=JobStatus.PROCESSING,
            current_step="Researching topic with Perplexity",
            progress=5,
        )
        logger.info(f"Job {job_id}: Starting text generation for '{topic}'")

        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            EbookGenerator = _get_ebook_generator()
            generator = EbookGenerator(openrouter_key, tmp_path)

            update_job(
                job_id,
                current_step="Generating content with AI (this takes several minutes)",
                progress=15,
            )

            # Full pipeline with Perplexity research
            ebook_data = await generator.generate(topic, num_chapters)

            update_job(
                job_id,
                current_step="Uploading images and saving to database",
                progress=85,
            )

            # Insert into Supabase
            ebook_id = await insert_ebook(
                ebook_data,
                supabase_url,
                supabase_service_key,
                tmp_path / "images",
            )

            update_job(
                job_id,
                status=JobStatus.COMPLETED,
                ebook_id=ebook_id,
                current_step="Complete",
                progress=100,
            )
            logger.info(f"Job {job_id}: Completed. Ebook ID: {ebook_id}")

    except Exception as e:
        logger.exception(f"Job {job_id}: Failed")
        update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e),
            current_step="Failed",
        )
