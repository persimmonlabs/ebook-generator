"""AlphaGrit Ebook Generator API - FastAPI Application."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import ebooks_router, jobs_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting AlphaGrit Ebook Generator API")
    logger.info(f"CORS origins: {settings.ALLOWED_ORIGINS}")
    yield
    logger.info("Shutting down AlphaGrit Ebook Generator API")


app = FastAPI(
    title="AlphaGrit Ebook Generator API",
    description="API for generating ebooks from PDFs or text topics",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ebooks_router)
app.include_router(jobs_router)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "AlphaGrit Ebook Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "service": "ebook-generator"}
