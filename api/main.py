"""AlphaGrit Ebook Generator API - Ultra minimal version for debugging."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

# Get CORS origins from env
ALLOWED = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
CORS_ORIGINS = [o.strip() for o in ALLOWED.split(",") if o.strip()]

print(f"[STARTUP] CORS: {CORS_ORIGINS}", flush=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    print("[REQUEST] GET /", flush=True)
    return {"api": "ebook-generator", "cors": CORS_ORIGINS}

@app.get("/health")
def health():
    print("[REQUEST] GET /health", flush=True)
    return {"status": "healthy"}

@app.get("/api/v1/test")
def test():
    print("[REQUEST] GET /api/v1/test", flush=True)
    return {"test": "ok"}

@app.options("/api/v1/ebooks/from-pdfs")
def options_pdfs(request: Request):
    origin = request.headers.get("origin", "")
    print(f"[REQUEST] OPTIONS /api/v1/ebooks/from-pdfs origin={origin}", flush=True)
    return JSONResponse(
        {"ok": True},
        headers={
            "Access-Control-Allow-Origin": origin if origin in CORS_ORIGINS else "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.post("/api/v1/ebooks/from-pdfs")
def post_pdfs(request: Request):
    origin = request.headers.get("origin", "")
    print(f"[REQUEST] POST /api/v1/ebooks/from-pdfs origin={origin}", flush=True)
    return JSONResponse(
        {"message": "Endpoint works but generation not implemented in minimal mode"},
        headers={
            "Access-Control-Allow-Origin": origin if origin in CORS_ORIGINS else "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.options("/api/v1/ebooks/from-text")
def options_text(request: Request):
    origin = request.headers.get("origin", "")
    print(f"[REQUEST] OPTIONS /api/v1/ebooks/from-text origin={origin}", flush=True)
    return JSONResponse(
        {"ok": True},
        headers={
            "Access-Control-Allow-Origin": origin if origin in CORS_ORIGINS else "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.post("/api/v1/ebooks/from-text")
def post_text(request: Request):
    origin = request.headers.get("origin", "")
    print(f"[REQUEST] POST /api/v1/ebooks/from-text origin={origin}", flush=True)
    return JSONResponse(
        {"message": "Endpoint works but generation not implemented in minimal mode"},
        headers={
            "Access-Control-Allow-Origin": origin if origin in CORS_ORIGINS else "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

print("[STARTUP] App ready", flush=True)
