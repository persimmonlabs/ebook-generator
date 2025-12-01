"""AlphaGrit Ebook Generator API."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from .routers import ebooks_router, jobs_router

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
try:
    app.include_router(ebooks_router)
    print("[STARTUP] Ebooks router registered", flush=True)
except Exception as e:
    print(f"[ERROR] Failed to register ebooks router: {e}", flush=True)

try:
    app.include_router(jobs_router)
    print("[STARTUP] Jobs router registered", flush=True)
except Exception as e:
    print(f"[ERROR] Failed to register jobs router: {e}", flush=True)


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


@app.get("/routes")
def list_routes():
    """List all registered routes for debugging."""
    routes = []
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods) if route.methods else [],
            })
    return {"routes": routes}


@app.on_event("startup")
async def startup_event():
    """Log registered routes at startup."""
    print("[STARTUP] Registered routes:", flush=True)
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            print(f"  {list(route.methods) if route.methods else []} {route.path}", flush=True)


print("[STARTUP] Agent Morpheus ready", flush=True)
