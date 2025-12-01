"""AlphaGrit Ebook Generator API - FastAPI Application."""
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routers import ebooks_router, jobs_router

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Parse CORS origins - strip whitespace from each origin
cors_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]
logger.info(f"Parsed CORS origins: {cors_origins}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("=" * 60)
    logger.info("Starting AlphaGrit Ebook Generator API")
    logger.info(f"CORS origins configured: {cors_origins}")
    logger.info("=" * 60)
    yield
    logger.info("Shutting down AlphaGrit Ebook Generator API")


app = FastAPI(
    title="AlphaGrit Ebook Generator API",
    description="API for generating ebooks from PDFs or text topics",
    version="1.0.0",
    lifespan=lifespan,
)


# Request logging middleware (added FIRST, runs LAST)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with details."""
    start_time = time.time()

    # Log request details
    logger.info(f">>> {request.method} {request.url.path}")
    logger.info(f"    Origin: {request.headers.get('origin', 'none')}")
    logger.info(f"    Headers: {dict(request.headers)}")

    # Process request
    try:
        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(f"<<< {request.method} {request.url.path} -> {response.status_code} ({process_time:.3f}s)")
        logger.info(f"    Response headers: {dict(response.headers)}")

        return response
    except Exception as e:
        logger.error(f"!!! {request.method} {request.url.path} -> Exception: {e}")
        raise


# CORS middleware - added AFTER logging, runs BEFORE
# This ensures CORS headers are added to all responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow ALL methods including OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)


# Global exception handler to ensure CORS on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all exceptions and ensure CORS headers are present."""
    logger.error(f"Unhandled exception: {exc}")
    origin = request.headers.get("origin")

    response = JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

    # Manually add CORS headers if origin matches
    if origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response


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


# Explicit OPTIONS handlers for debugging
@app.options("/api/v1/ebooks/from-pdfs")
async def options_from_pdfs(request: Request):
    """Explicit OPTIONS handler for from-pdfs endpoint."""
    logger.info(f"OPTIONS /api/v1/ebooks/from-pdfs - Origin: {request.headers.get('origin')}")
    origin = request.headers.get("origin", "")

    response = JSONResponse(content={"status": "ok"})

    if origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "600"

    return response


@app.options("/api/v1/ebooks/from-text")
async def options_from_text(request: Request):
    """Explicit OPTIONS handler for from-text endpoint."""
    logger.info(f"OPTIONS /api/v1/ebooks/from-text - Origin: {request.headers.get('origin')}")
    origin = request.headers.get("origin", "")

    response = JSONResponse(content={"status": "ok"})

    if origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "600"

    return response


# Debug endpoint to test CORS
@app.get("/api/v1/cors-test")
async def cors_test(request: Request):
    """Test endpoint to verify CORS is working."""
    return {
        "status": "ok",
        "origin_received": request.headers.get("origin"),
        "allowed_origins": cors_origins,
        "cors_should_work": request.headers.get("origin") in cors_origins,
    }
