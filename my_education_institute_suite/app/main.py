import os
import time
from collections import defaultdict, deque
from typing import Deque, Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging
from app.db.init_db import init_database
from app.db.seed_data import seed
from app.api.v1.admissions import router as admissions_router
from app.api.v1.assignments import router as assignments_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.auth import router as auth_router
from app.api.v1.batches import router as batches_router
from app.api.v1.cms import router as cms_router
from app.api.v1.courses import router as courses_router
from app.api.v1.exams import router as exams_router
from app.api.v1.fees import router as fees_router
from app.api.v1.materials import router as materials_router
from app.api.v1.notices import router as notices_router
from app.api.v1.reports import router as reports_router
from app.api.v1.settings import router as settings_router
from app.api.v1.staff import router as staff_router
from app.api.v1.storage import router as storage_router
from app.api.v1.students import router as students_router
from app.api.v1.sync import router as sync_router
from app.api.v1.users import router as users_router

setup_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="MY EDUCATION INSTITUTE - Production Enterprise ERP + CMS + CBT Platform with Render PostgreSQL Persistence",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# GZip Compression for Static Assets and Large JSON Payloads
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS Configuration from BaseSettings
cors_origins = settings.cors_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Window Store (Per-IP sliding window)
_RATE_BUCKETS: Dict[str, Deque[float]] = defaultdict(deque)


@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    bucket = _RATE_BUCKETS[client_ip]
    while bucket and bucket[0] < now - 60.0:
        bucket.popleft()
    if len(bucket) >= settings.RATE_LIMIT_PER_MINUTE:
        logger.warning("Rate limit exceeded for IP %s", client_ip)
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "message": "Rate limit exceeded. Please wait before sending more requests.",
                "detail": "Rate limit exceeded.",
            },
        )
    bucket.append(now)

    response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


# Centralized Structured Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    msg = str(exc.detail) if exc.detail else "Request failed."
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": msg,
            "detail": exc.detail,
        },
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_msg = errors[0].get("msg", "Invalid input parameters.") if errors else "Validation error."
    logger.warning("Validation error on %s: %s", request.url.path, errors)
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": f"Validation error: {first_msg}",
            "detail": errors,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected internal server error occurred.",
            "detail": "Internal server error.",
        },
    )


# Initialize Schema & Seed Baseline Data Safely
try:
    init_database(fresh=False)
    seed()
except Exception as startup_exc:
    logger.warning("Deferred database initialization check: %s", startup_exc)

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
    settings_router,
    sync_router,
    exams_router,
    storage_router,
]

for r in api_v1_routers:
    app.include_router(r, prefix=settings.API_V1_STR)


@app.api_route("/health", methods=["GET", "HEAD"], tags=["System Health"])
def health_check():
    return {
        "success": True,
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "database": "PostgreSQL (Render)",
        "environment": settings.ENVIRONMENT,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "2.0.0",
    }


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
def serve_spa():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {
        "success": True,
        "project": settings.PROJECT_NAME,
        "status": "online",
        "database": "PostgreSQL (Render)",
        "version": "2.0.0",
        "docs_url": "/docs",
    }
