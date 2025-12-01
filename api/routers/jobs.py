"""Job status endpoints."""
from fastapi import APIRouter, HTTPException

from ..job_store import get_job

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


@router.get("/{job_id}")
async def get_job_status(job_id: str):
    """
    Get the status of an ebook generation job.

    Poll this endpoint every 5 seconds to track progress.

    Returns:
        - job_id: The job identifier
        - status: pending | processing | completed | failed
        - progress: 0-100 percentage
        - current_step: Human-readable description of current step
        - ebook_id: UUID of created ebook (only when status=completed)
        - error: Error message (only when status=failed)
    """
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status.value,
        "progress": job.progress,
        "current_step": job.current_step,
        "ebook_id": job.ebook_id,
        "error": job.error,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
    }
