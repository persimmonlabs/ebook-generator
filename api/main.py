"""AlphaGrit Ebook Generator API - Minimal CORS-enabled version."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Delay router imports to prevent any import-time crashes
# from .routers import ebooks_router, jobs_router

from .config import settings

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# CORS origins
CORS_ORIGINS = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
print(f"CORS ORIGINS: {CORS_ORIGINS}", flush=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== API STARTING ===", flush=True)
    # Lazy import routers AFTER app starts
    try:
        from .routers import ebooks_router, jobs_router
        app.include_router(ebooks_router)
        app.include_router(jobs_router)
        print("=== ROUTERS LOADED ===", flush=True)
    except Exception as e:
        print(f"=== ROUTER IMPORT ERROR: {e} ===", flush=True)
    yield
    print("=== API SHUTTING DOWN ===", flush=True)


app = FastAPI(title="AlphaGrit Ebook Generator", lifespan=lifespan)

# Standard FastAPI CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"api": "ebook-generator", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/v1/test")
def test():
    print("TEST ENDPOINT HIT", flush=True)
    return {"test": "ok"}


# Manual OPTIONS handlers as fallback
@app.options("/api/v1/ebooks/from-pdfs")
def options_pdfs(request: Request):
    origin = request.headers.get("origin", "")
    print(f"OPTIONS from-pdfs, origin={origin}", flush=True)
    headers = {}
    if origin in CORS_ORIGINS:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    return JSONResponse({"ok": True}, headers=headers)


@app.options("/api/v1/ebooks/from-text")
def options_text(request: Request):
    origin = request.headers.get("origin", "")
    print(f"OPTIONS from-text, origin={origin}", flush=True)
    headers = {}
    if origin in CORS_ORIGINS:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    return JSONResponse({"ok": True}, headers=headers)
