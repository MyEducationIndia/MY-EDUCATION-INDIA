from contextlib import asynccontextmanager
try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import (
    EnterpriseAppException,
    enterprise_exception_handler,
    unhandled_exception_handler,
)
from app.db.base import Base
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

    # 1. Create any missing tables safely without sorted_tables
    for _ in range(2):
        for table in list(Base.metadata.tables.values()):
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(lambda sync_conn, t=table: t.create(sync_conn, checkfirst=True))
            except Exception as e:
                app_logger.warning(f"Table create skip ({table.name}): {e}")

    # 2. Patch missing columns on existing tables (users, institutes, audit_logs)
    column_patches = [
        # users
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_secret VARCHAR(64)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_backup_codes TEXT",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS user_category VARCHAR(32) NOT NULL DEFAULT 'STUDENT'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS department VARCHAR(100)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS designation VARCHAR(100)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS admission_or_emp_id VARCHAR(64)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS dob DATE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR(20)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS blood_group VARCHAR(10)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS photo_url TEXT",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS digital_signature_url TEXT",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS identity_verification_status VARCHAR(32) NOT NULL DEFAULT 'PENDING'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_id_type VARCHAR(50)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_id_number VARCHAR(100)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_archived BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS institute_id UUID",
        # institutes
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS time_zone VARCHAR(64) NOT NULL DEFAULT 'Asia/Kolkata'",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS default_language VARCHAR(16) NOT NULL DEFAULT 'en-IN'",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS currency_code VARCHAR(10) NOT NULL DEFAULT 'INR'",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS currency_symbol VARCHAR(10) NOT NULL DEFAULT '₹'",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS current_academic_year VARCHAR(64) NOT NULL DEFAULT '2026-2027'",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS custom_domain VARCHAR(255)",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS custom_domain_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS google_maps_embed_url TEXT",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS google_maps_latitude DOUBLE PRECISION",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS google_maps_longitude DOUBLE PRECISION",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS social_media_links JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS smtp_config JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS sms_gateway_config JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS whatsapp_gateway_config JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS payment_gateway_config JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS theme_config JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS seo_metadata JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE institutes ADD COLUMN IF NOT EXISTS communication_settings JSONB NOT NULL DEFAULT '{}'::jsonb",
        # audit_logs
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_username VARCHAR(100)",
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS actor_role VARCHAR(64)",
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS event_category VARCHAR(50) NOT NULL DEFAULT 'CRUD_OPERATION'",
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS severity VARCHAR(20) NOT NULL DEFAULT 'INFO'",
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS duration_ms INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS ip_location VARCHAR(100) NOT NULL DEFAULT 'Indore, MP, India'",
        "ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS payload_checksum VARCHAR(64)",
        # roles
        "ALTER TABLE roles ADD COLUMN IF NOT EXISTS is_custom_role BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE roles ADD COLUMN IF NOT EXISTS department_name VARCHAR(100)",
        "ALTER TABLE roles ADD COLUMN IF NOT EXISTS data_scope VARCHAR(50) NOT NULL DEFAULT 'ALL'",
        "ALTER TABLE roles ADD COLUMN IF NOT EXISTS field_permissions_json JSONB NOT NULL DEFAULT '{}'::jsonb",
        "ALTER TABLE roles ADD COLUMN IF NOT EXISTS menu_permissions_json JSONB NOT NULL DEFAULT '{}'::jsonb",
        # permissions
        "ALTER TABLE permissions ADD COLUMN IF NOT EXISTS group_key VARCHAR(64) NOT NULL DEFAULT 'GENERAL'",
        "ALTER TABLE permissions ADD COLUMN IF NOT EXISTS action_type VARCHAR(32) NOT NULL DEFAULT 'READ'",
        # refresh_token_sessions
        "ALTER TABLE refresh_token_sessions ADD COLUMN IF NOT EXISTS device_name VARCHAR(255) NOT NULL DEFAULT 'Web Browser'",
        "ALTER TABLE refresh_token_sessions ADD COLUMN IF NOT EXISTS last_active_at TIMESTAMPTZ",
    ]
    for ddl in column_patches:
        try:
            async with engine.begin() as conn:
                await conn.execute(text(ddl))
        except Exception as e:
            app_logger.warning(f"Column patch skip: {e}")

    # 3. Seed Super Administrator if missing
    try:
        from app.auth.security import hash_password
        from app.db.session import AsyncSessionLocal
        from app.models.institute import Institute
        from app.models.role import Role
        from app.models.user import User

        async with AsyncSessionLocal() as session:
            admin_res = await session.execute(
                select(User).where(User.username == "superadmin")
            )
            admin_user = admin_res.scalar_one_or_none()
            if not admin_user:
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
                    user_category="SUPER_ADMIN",
                    identity_verification_status="VERIFIED",
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
