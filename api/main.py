"""AlphaGrit Ebook Generator API - FastAPI Application."""
import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .routers import ebooks_router, jobs_router

# Configure logging - make sure it outputs
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,  # Override any existing config
)
logger = logging.getLogger(__name__)

# Also log to stdout explicitly
import sys
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Parse CORS origins
cors_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]
logger.info(f"Parsed CORS origins: {cors_origins}")


class CORSAndLoggingMiddleware(BaseHTTPMiddleware):
    """Custom middleware to handle CORS and log all requests."""

    async def dispatch(self, request: Request, call_next):
        # Log every request
        logger.info(f"=== INCOMING REQUEST ===")
        logger.info(f"Method: {request.method}")
        logger.info(f"Path: {request.url.path}")
        logger.info(f"Origin: {request.headers.get('origin', 'NONE')}")

        origin = request.headers.get("origin", "")

        # Handle OPTIONS preflight
        if request.method == "OPTIONS":
            logger.info(f"Handling OPTIONS preflight for origin: {origin}")

            if origin in cors_origins or not origin:
                response = JSONResponse(
                    content={"status": "preflight_ok"},
                    status_code=200,
                )
                response.headers["Access-Control-Allow-Origin"] = origin or "*"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
                response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, Origin, X-Requested-With"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Max-Age"] = "600"
                logger.info(f"Returning preflight response with headers")
                return response
            else:
                logger.warning(f"Origin {origin} not in allowed origins: {cors_origins}")

        # Process actual request
        try:
            response = await call_next(request)

            # Add CORS headers to all responses
            if origin in cors_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"

            logger.info(f"=== RESPONSE: {response.status_code} ===")
            return response

        except Exception as e:
            logger.error(f"=== EXCEPTION ===")
            logger.error(f"Error: {str(e)}")
            logger.error(traceback.format_exc())

            response = JSONResponse(
                content={"detail": str(e)},
                status_code=500,
            )
            if origin in cors_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
            return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("=" * 60)
    logger.info("Starting AlphaGrit Ebook Generator API")
    logger.info(f"CORS origins: {cors_origins}")
    logger.info("=" * 60)
    print("=" * 60, flush=True)
    print("API STARTED - CORS origins:", cors_origins, flush=True)
    print("=" * 60, flush=True)
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="AlphaGrit Ebook Generator API",
    description="API for generating ebooks from PDFs or text topics",
    version="1.0.0",
    lifespan=lifespan,
)

# Add our custom CORS/logging middleware
app.add_middleware(CORSAndLoggingMiddleware)

# Include routers
app.include_router(ebooks_router)
app.include_router(jobs_router)


@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {
        "name": "AlphaGrit Ebook Generator API",
        "version": "1.0.0",
        "cors_origins": cors_origins,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/v1/test")
async def test_endpoint():
    """Simple test endpoint."""
    logger.info("Test endpoint called")
    return {"status": "ok", "message": "API is working"}
