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

# Parse CORS origins - strip whitespace from each origin
cors_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]
logger.info(f"Parsed CORS origins: {cors_origins}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting AlphaGrit Ebook Generator API")
    logger.info(f"CORS origins configured: {cors_origins}")
    yield
    logger.info("Shutting down AlphaGrit Ebook Generator API")


app = FastAPI(
    title="AlphaGrit Ebook Generator API",
    description="API for generating ebooks from PDFs or text topics",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Next.js frontend
# Must be added BEFORE routers for preflight OPTIONS to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight for 10 minutes
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
