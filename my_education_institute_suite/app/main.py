from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os, time

from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.students import router as students_router
from app.api.v1.staff import router as staff_router
from app.api.v1.courses import router as courses_router
from app.api.v1.batches import router as batches_router
from app.api.v1.admissions import router as admissions_router
from app.api.v1.fees import router as fees_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.materials import router as materials_router
from app.api.v1.notices import router as notices_router
from app.api.v1.cms import router as cms_router
from app.api.v1.assignments import router as assignments_router
from app.api.v1.reports import router as reports_router
from app.api.v1.settings import router as settings_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="MY EDUCATION INSTITUTE - Production Premier Institute of Computer & IT Studies REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enterprise Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Mount API Routers under /api/v1
api_v1_routers = [
    auth_router,
    users_router,
    students_router,
    staff_router,
    courses_router,
    batches_router,
    admissions_router,
    fees_router,
    attendance_router,
    materials_router,
    notices_router,
    cms_router,
    assignments_router,
    reports_router,
    settings_router
]

for r in api_v1_routers:
    app.include_router(r, prefix=settings.API_V1_STR)

# Healthcheck Endpoint
@app.get("/health", tags=["System Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0.0"
    }

# Static Files & SPA Delivery
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def serve_spa():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {
        "project": settings.PROJECT_NAME,
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
