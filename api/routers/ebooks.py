"""Ebook generation endpoints."""
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form, Depends, HTTPException

from ..auth import verify_admin
from ..config import settings
from ..job_store import create_job
from ..services.generation import run_pdf_generation, run_text_generation

router = APIRouter(prefix="/api/v1/ebooks", tags=["ebooks"])


@router.post("/from-pdfs")
async def create_ebook_from_pdfs(
    background_tasks: BackgroundTasks,
    pdf_en: UploadFile = File(..., description="English PDF file"),
    pdf_pt: UploadFile = File(..., description="Portuguese PDF file"),
    _: str = Depends(verify_admin),
):
    """
    Create a new ebook from English and Portuguese PDF files.

    Returns a job_id that can be used to poll for status.
    The ebook will be created as a draft.
    """
    # Validate file types
    if not pdf_en.filename or not pdf_en.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="English file must be a PDF")
    if not pdf_pt.filename or not pdf_pt.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Portuguese file must be a PDF")

    # Read files into memory
    pdf_en_bytes = await pdf_en.read()
    pdf_pt_bytes = await pdf_pt.read()

    # Validate file sizes (max 50MB each)
    max_size = 50 * 1024 * 1024
    if len(pdf_en_bytes) > max_size:
        raise HTTPException(status_code=400, detail="English PDF exceeds 50MB limit")
    if len(pdf_pt_bytes) > max_size:
        raise HTTPException(status_code=400, detail="Portuguese PDF exceeds 50MB limit")

    # Create job for tracking
    job = create_job()

    # Schedule background task
    background_tasks.add_task(
        run_pdf_generation,
        job.id,
        pdf_en_bytes,
        pdf_pt_bytes,
        settings.OPENROUTER_API_KEY,
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_ROLE_KEY,
    )

    return {
        "job_id": job.id,
        "message": "Ebook generation started. Poll /api/v1/jobs/{job_id} for status.",
    }


@router.post("/from-text")
async def create_ebook_from_text(
    background_tasks: BackgroundTasks,
    topic: str = Form(..., description="Topic or prompt for ebook generation"),
    num_chapters: int = Form(5, ge=1, le=20, description="Number of chapters (1-20)"),
    _: str = Depends(verify_admin),
):
    """
    Create a new ebook from a text topic using AI generation.

    This uses Perplexity for research and Claude for content generation.
    Returns a job_id that can be used to poll for status.
    The ebook will be created as a draft.
    """
    # Validate topic length
    if len(topic) < 10:
        raise HTTPException(
            status_code=400, detail="Topic must be at least 10 characters"
        )
    if len(topic) > 1000:
        raise HTTPException(
            status_code=400, detail="Topic must be less than 1000 characters"
        )

    # Create job for tracking
    job = create_job()

    # Schedule background task
    background_tasks.add_task(
        run_text_generation,
        job.id,
        topic,
        num_chapters,
        settings.OPENROUTER_API_KEY,
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_ROLE_KEY,
    )

    return {
        "job_id": job.id,
        "message": "Ebook generation started. Poll /api/v1/jobs/{job_id} for status.",
    }
