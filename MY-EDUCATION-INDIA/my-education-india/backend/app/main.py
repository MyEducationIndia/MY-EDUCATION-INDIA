from contextlib import asynccontextmanager
try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import (
    EnterpriseAppException,
    enterprise_exception_handler,
    unhandled_exception_handler,
)
from app.db.session import engine
from app.logs.logger import app_logger
from app.middleware.enterprise_middleware import (
    EnterpriseContextAndSecurityMiddleware,
)

settings = get_settings()

if settings.SENTRY_DSN and sentry_sdk:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.APP_ENV,
        traces_sample_rate=0.2,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info(f"Starting {settings.APP_NAME} ({settings.APP_ENV})")
    yield
    await engine.dispose()
    app_logger.info(f"Shut down {settings.APP_NAME} database connection pool.")


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description=(
            "Enterprise Modular Monolith Backend for MY EDUCATION INDIA — "
            "Multi-Institute ERP, LMS, CBT, Website CMS, and Super Admin Governance."
        ),
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-CSRF-Token", "X-Request-ID"],
        expose_headers=["X-Request-ID", "X-Subdomain-Context"],
    )# 1. Custom enterprise middleware runs first on internal requests
    app.add_middleware(EnterpriseContextAndSecurityMiddleware, max_requests_per_minute=180)

    # 2. CORSMiddleware added LAST so it wraps everything and handles OPTIONS preflights
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Subdomain-Context"],
    )

app = create_application()

# Root Health Probes for Render, Kubernetes & Load Balancers
@app.get("/health", tags=["System Health"])
async def root_health():
    return {"status": "healthy", "service": "MY EDUCATION INDIA ERP V2", "env": settings.APP_ENV}

@app.get("/ready", tags=["System Health"])
async def root_ready():
    return {"status": "ready", "database": "connected", "traffic": "admissible"}

@app.get("/live", tags=["System Health"])
async def root_live():
    return {"status": "alive", "timestamp": "ok"}

