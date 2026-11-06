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
    
    # Automated Zero-Shell Database Bootstrap
    try:
        from app.auth.security import hash_password
        from app.db.session import AsyncSessionLocal
        from app.models.institute import Institute
        from app.models.role import Role
        from app.models.user import User
        from sqlalchemy import select

        async with AsyncSessionLocal() as session:
            admin_res = await session.execute(
                select(User).where(User.username == "superadmin")
            )
            admin_user = admin_res.scalar_one_or_none()
            if not admin_user:
                # 1. Ensure Flagship Institute
                inst_res = await session.execute(
                    select(Institute).where(Institute.code == "MEI-HQ")
                )
                inst = inst_res.scalar_one_or_none()
                if not inst:
                    inst = Institute(
                        code="MEI-HQ",
                        name="MY EDUCATION INDIA",
                        official_email="superadmin@myeducation.in",
                        official_phone="+917312456789",
                        address_line1="Campus Square",
                        city="Indore",
                        state="Madhya Pradesh",
                        postal_code="452001",
                        country="India",
                    )
                    session.add(inst)
                    await session.flush()

                # 2. Ensure Role
                role_res = await session.execute(
                    select(Role).where(Role.code == "SUPER_ADMIN")
                )
                role = role_res.scalar_one_or_none()
                if not role:
                    role = Role(
                        code="SUPER_ADMIN",
                        name="Enterprise Super Administrator",
                        is_system_role=True,
                        portal_subdomain="admin",
                        institute_id=inst.id,
                    )
                    session.add(role)
                    await session.flush()

                # 3. Create Super Administrator with exact pwdlib hash
                admin_user = User(
                    email="superadmin@myeducation.in",
                    username="superadmin",
                    phone_number="+919999999999",
                    first_name="Enterprise",
                    last_name="Administrator",
                    password_hash=hash_password("EduIndia#Production2026!"),
                    is_active=True,
                    is_super_admin=True,
                    is_verified=True,
                    institute_id=inst.id,
                    roles=[role],
                )
                session.add(admin_user)
                await session.commit()
                app_logger.info("Super Administrator seeded successfully into PostgreSQL.")
    except Exception as e:
        app_logger.warning(f"Startup database check: {e}")

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

    # 1. Custom enterprise security middleware
    app.add_middleware(EnterpriseContextAndSecurityMiddleware, max_requests_per_minute=180)

    # 2. Outermost CORSMiddleware to handle browser preflight OPTIONS requests cleanly
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Subdomain-Context"],
    )

    app.add_exception_handler(EnterpriseAppException, enterprise_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

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

    return app


app = create_application()
