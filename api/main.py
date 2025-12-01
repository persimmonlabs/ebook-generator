"""AlphaGrit Ebook Generator API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .routers import ebooks, jobs

# Get CORS origins from env
ALLOWED = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
CORS_ORIGINS = [o.strip() for o in ALLOWED.split(",") if o.strip()]

print(f"[STARTUP] CORS origins: {CORS_ORIGINS}", flush=True)

app = FastAPI(
    title="AlphaGrit Ebook Generator",
    description="API for generating ebooks with Agent Morpheus",
    version="1.0.0",
)

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ebooks.router)
app.include_router(jobs.router)


@app.get("/")
def root():
    """Health check and API info."""
    return {
        "api": "ebook-generator",
        "version": "1.0.0",
        "agent": "Morpheus",
        "cors_origins": CORS_ORIGINS,
    }


@app.get("/health")
def health():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "agent": "Morpheus is awake"}


print("[STARTUP] Agent Morpheus ready", flush=True)
