"""In-memory job store for tracking ebook generation progress."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict
import uuid


class JobStatus(str, Enum):
    """Status of an ebook generation job."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    """Represents an ebook generation job."""

    id: str
    status: JobStatus
    progress: int = 0  # 0-100
    current_step: str = ""
    ebook_id: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


# In-memory store (note: jobs lost on restart)
_jobs: Dict[str, Job] = {}


def create_job() -> Job:
    """Create a new job and add it to the store."""
    job = Job(id=str(uuid.uuid4()), status=JobStatus.PENDING)
    _jobs[job.id] = job
    return job


def update_job(job_id: str, **updates) -> None:
    """Update job fields."""
    if job_id in _jobs:
        for key, value in updates.items():
            if hasattr(_jobs[job_id], key):
                setattr(_jobs[job_id], key, value)
        _jobs[job_id].updated_at = datetime.utcnow()


def get_job(job_id: str) -> Optional[Job]:
    """Get a job by ID."""
    return _jobs.get(job_id)


def delete_job(job_id: str) -> bool:
    """Delete a job from the store."""
    if job_id in _jobs:
        del _jobs[job_id]
        return True
    return False
