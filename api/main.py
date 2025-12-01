"""AlphaGrit Ebook Generator API - FastAPI Application."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    logger.info(f"CORS origins: {cors_origins}")
    yield
    logger.info("Shutting down AlphaGrit Ebook Generator API")


app = FastAPI(
    title="AlphaGrit Ebook Generator API",
    description="API for generating ebooks from PDFs or text topics",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
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
        "cors_origins": cors_origins,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "service": "ebook-generator"}


@app.get("/api/v1/cors-test")
async def cors_test(request: Request):
    """Test endpoint to verify CORS is working."""
    origin = request.headers.get("origin", "none")
    logger.info(f"CORS test - Origin: {origin}")
    return {
        "status": "ok",
        "origin_received": origin,
        "allowed_origins": cors_origins,
        "cors_should_work": origin in cors_origins,
    }


# Explicit OPTIONS handlers with manual CORS headers
@app.options("/api/v1/ebooks/from-pdfs")
async def options_from_pdfs(request: Request):
    """Explicit OPTIONS handler for from-pdfs endpoint."""
    origin = request.headers.get("origin", "")
    logger.info(f"OPTIONS /api/v1/ebooks/from-pdfs - Origin: {origin}")

    headers = {
        "Access-Control-Allow-Origin": origin if origin in cors_origins else "",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Origin, X-Requested-With",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "600",
    }

    return JSONResponse(content={"status": "ok"}, headers=headers)


@app.options("/api/v1/ebooks/from-text")
async def options_from_text(request: Request):
    """Explicit OPTIONS handler for from-text endpoint."""
    origin = request.headers.get("origin", "")
    logger.info(f"OPTIONS /api/v1/ebooks/from-text - Origin: {origin}")

    headers = {
        "Access-Control-Allow-Origin": origin if origin in cors_origins else "",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Origin, X-Requested-With",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "600",
    }

    return JSONResponse(content={"status": "ok"}, headers=headers)


@app.options("/api/v1/jobs/{job_id}")
async def options_jobs(request: Request, job_id: str):
    """Explicit OPTIONS handler for jobs endpoint."""
    origin = request.headers.get("origin", "")
    logger.info(f"OPTIONS /api/v1/jobs/{job_id} - Origin: {origin}")

    headers = {
        "Access-Control-Allow-Origin": origin if origin in cors_origins else "",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Origin, X-Requested-With",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "600",
    }

    return JSONResponse(content={"status": "ok"}, headers=headers)
