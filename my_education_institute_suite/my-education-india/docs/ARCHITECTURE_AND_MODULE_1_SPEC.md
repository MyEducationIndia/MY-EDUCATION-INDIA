# MY EDUCATION INDIA — Enterprise Architecture & Module 1 Specification

## 1. Executive Architecture Overview

**MY EDUCATION INDIA** is engineered as a **Modular Monolith** backed exclusively by **Neon PostgreSQL (PostgreSQL 16+)** using **SQLAlchemy 2.x Async ORM (`asyncpg`)** and **Alembic** migrations, with a **React 19 + TypeScript + Vite + Tailwind CSS** frontend. Every boundary is strictly separated into models, Pydantic v2 schemas, repositories, services, permissions, and versioned `/api/v1` routers so individual domains can be extracted into independent microservices across dedicated subdomains without schema rewrites.

| Architectural Layer | Technology & Standards | Key Implementation Files |
| :--- | :--- | :--- |
| **Frontend Application** | React 19, TypeScript 5.6, Vite 5, Tailwind CSS, TanStack Query v5, React Hook Form + Zod, Framer Motion | `frontend/src/App.tsx`, `frontend/src/routes/AppRoutes.tsx`, `frontend/src/layouts/SuperAdminLayout.tsx` |
| **Zero-Storage Auth State** | Volatile JS closure memory (`EnterpriseVolatileAuthStore`) + `HttpOnly; Secure; SameSite=Strict` refresh cookie | `frontend/src/store/authMemoryStore.ts`, `frontend/src/api/httpClient.ts`, `frontend/src/hooks/useAuthSession.ts` |
| **Backend API Gateway** | FastAPI, Python 3.12, Pydantic v2, OpenAPI `/api/v1`, Sliding-Window Rate Limiter, Subdomain Context Resolver | `backend/app/main.py`, `backend/app/middleware/enterprise_middleware.py`, `backend/app/core/config.py` |
| **Security & Cryptography** | Argon2id + Bcrypt (`pwdlib`), PyJWT Access & Refresh tokens, Token Family Reuse Detection, HMAC-SHA256 CSRF | `backend/app/auth/security.py`, `backend/app/permissions/rbac_dependencies.py`, `backend/app/services/auth_service.py` |
| **Database & Persistence** | Neon PostgreSQL (`postgresql+asyncpg://`), SQLAlchemy 2.x `Mapped` models, Alembic migrations, Native `pg_dump`/`pg_restore` | `backend/app/db/base.py`, `backend/app/db/session.py`, `backend/alembic/versions/0001_initial_module1_schema.py`, `scripts/pg_backup_restore.py` |
| **External Provider Layer** | Configurable SMTP Email, DLT SMS Gateway, Meta Cloud WhatsApp API, Cloudinary & S3 Storage | `backend/app/utils/providers.py`, `.env.example` |
| **DevOps & Deployment** | Multi-stage Dockerfiles (non-root user + `postgresql-client`), Nginx security proxy, Docker Compose, Render Blueprint | `docker/Dockerfile.backend`, `docker/Dockerfile.frontend`, `docker-compose.yml`, `render.yaml` |

## 2. Subdomain Routing Matrix (Modular Monolith to Microservice Ready)

Both `backend/app/middleware/enterprise_middleware.py` and `frontend/src/utils/subdomainResolver.ts` inspect incoming `Host` headers and resolve the active portal context across all 14 enterprise subdomains sharing the unified Neon PostgreSQL database:

| Subdomain Prefix | Target Portal / Subsystem | Primary Module Keys |
| :--- | :--- | :--- |
| `admin.` | Super Admin & Institute Governance Portal | `institute_management`, `role_management`, `settings`, `audit_logs`, `backup`, `restore`, `hr`, `payroll`, `inventory`, `hostel`, `transport`, `reports`, `analytics` |
| `website.` | Public Dynamic SEO Website CMS | `website_cms`, `gallery`, `news`, `notice_board` |
| `student.` | Student Academic & Lifecycle Portal | `student_management`, `admission` |
| `teacher.` | Faculty & Academic Delivery Portal | `faculty_management` |
| `parent.` | Parent & Guardian Monitoring Portal | `student_management`, `attendance`, `fees`, `results` |
| `exam.` | Examination & Grading Controller Portal | `exam_management`, `results` |
| `cbt.` | Online & Offline Computer-Based Testing Engine | `question_bank`, `offline_cbt`, `online_cbt` |
| `fees.` | Fee Ledger, Installments & Receipts Portal | `fees` |
| `attendance.` | Biometric / QR / Daily Attendance Portal | `attendance` |
| `certificate.` | QR-Verifiable Certificate Issuance & Verification | `certificates` |
| `library.` | Barcode Circulation & Catalog Portal | `library` |
| `lms.` | Course Curriculum & Learning Management Portal | `course_management`, `batch_management` |
| `communication.` | Omnichannel Broadcast Hub (SMTP, SMS, WhatsApp) | `communication`, `sms`, `whatsapp`, `email` |
| `api.` | Versioned REST API Gateway (`/api/v1`) | `authentication`, `api_management` |

## 3. Module 1 Complete Implementation Breakdown

 Following the strict **one-module-at-a-time** enterprise development methodology, **Module 1 (Foundation, Identity & Authentication, RBAC Role Management, Institute & 37-Module Governance Registry, and Compliance Audit Logs)** is 100% complete across all seven layers:

### 3.1 Database Schema (`backend/app/models/` & `backend/alembic/versions/0001_initial_module1_schema.py`)
1. `institutes` (`Institute`): Multi-campus identity, affiliation metadata, Cloudinary logo/favicon URLs, hex color palettes, JSONB SEO metadata, and communication gateway settings.
2. `permissions` (`Permission`): Granular action codes (`institutes:read`, `institutes:write`, `modules:toggle`, `roles:read`, `roles:write`, `users:read`, `users:write`, `audit:read`) scoped by `module_key`.
3. `roles` (`Role`) & `role_permissions`: Subdomain-scoped RBAC roles with many-to-many permission bindings.
4. `users` (`User`) & `user_roles`: Argon2id password hashes, brute-force lockout counters (`failed_login_attempts`, `locked_until`), verification flags, and institute/role associations.
5. `refresh_token_sessions` (`RefreshTokenSession`): SHA-256 hashed refresh tokens with `token_family` lineage tracking to detect token replay and automatically revoke compromised session families.
6. `system_module_configs` (`SystemModuleConfig`): Per-institute registry of all 37 platform modules with real-time `is_enabled` flags, `is_core_locked` protection for security-critical modules, and JSONB module configuration.
7. `audit_logs` (`AuditLog`): Immutable append-only compliance records capturing `actor_user_id`, `institute_id`, `module_key`, `action`, `resource_type`, `resource_id`, HTTP method/path/status, client IP, User-Agent, `request_id`, and JSONB delta payloads.

### 3.2 REST API v1 Endpoints (`backend/app/api/v1/endpoints/`)
- `GET /api/v1/health`: Verifies live async connectivity and PostgreSQL server version.
- `POST /api/v1/auth/login`: Authenticates user, enforces lockout policy, issues short-lived JWT access token + HMAC CSRF token in JSON, sets `HttpOnly; Secure; SameSite=Strict` refresh cookie, and writes an audit log.
- `POST /api/v1/auth/refresh`: Validates and rotates the refresh token session in PostgreSQL with token-family reuse detection.
- `POST /api/v1/auth/logout`: Enforces CSRF validation, revokes the entire token family in PostgreSQL, clears the HttpOnly cookie, and records an audit event.
- `GET /api/v1/auth/me`: Returns the authenticated user profile, assigned roles, and effective permission codes.
- `POST /api/v1/auth/change-password`: Verifies current password, enforces strong password complexity, updates Argon2id hash, and logs the security event.
- `GET /api/v1/roles`, `GET /api/v1/roles/permissions`, `POST /api/v1/roles`, `PUT /api/v1/roles/{role_id}/permissions`: Full RBAC role and permission matrix CRUD.
- `GET /api/v1/users`, `POST /api/v1/users`, `PATCH /api/v1/users/{user_id}`: Paginated, searchable user directory, user provisioning, and account suspension/activation.
- `GET /api/v1/institutes`, `GET /api/v1/institutes/{institute_id}`, `POST /api/v1/institutes`, `PATCH /api/v1/institutes/{institute_id}/branding`, `PATCH /api/v1/institutes/{institute_id}/modules/{module_key}`: Multi-institute governance, branding updates, and real-time enable/disable toggles for all 37 modules.
- `GET /api/v1/audit-logs`: Paginated, filterable security and compliance audit trail.

### 3.3 Deployment & Verification Instructions
1. **Configure Environment**: Copy `.env.example` to `.env` and set your Neon PostgreSQL connection strings (`DATABASE_URL` with `postgresql+asyncpg://` and `SYNC_DATABASE_URL` with `postgresql+psycopg://`) along with 64-byte cryptographic secrets (`openssl rand -hex 64`).
2. **Run Database Migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```
3. **Seed Initial Super Admin & 37 Module Configurations**:
   ```bash
   INITIAL_SUPERADMIN_EMAIL="admin@myeducationindia.edu.in" \
   INITIAL_SUPERADMIN_PASSWORD="StrongEnterprisePassword#2026" \
   python3 scripts/seed_enterprise_foundation.py
   ```
4. **Start Backend & Frontend**:
   - Docker Compose: `docker compose up --build -d`
   - Local Backend: `cd backend && uvicorn app.main:app --reload --port 8000`
   - Local Frontend: `cd frontend && npm install && npm run dev`
5. **Transaction-Safe PostgreSQL Backup & Restore**:
   - Create binary custom-format dump: `python3 scripts/pg_backup_restore.py backup --out-dir ./backups`
   - Atomic single-transaction restore (auto-rollback on error): `python3 scripts/pg_backup_restore.py restore --file ./backups/<archive>.dump`

## 4. Roadmap for Subsequent Modules (Module-by-Module Progression)

With Module 1 complete and verified, choose which module to build next in full end-to-end detail:
1. **Module 2 — Dynamic Website CMS, Gallery, News & Notice Board**: Dynamic SEO pages, navigation builders, Cloudinary media albums, and public notice boards with zero hardcoded content.
2. **Module 3 — Academic Core (Course Management, Batch Management, Faculty & Student Management, Admission)**: Program structures, cohort timetables, student/faculty onboarding, and admission workflows.
3. **Module 4 — Fees & Financial Ledger**: Fee heads, installment schedules, fine rules, payment gateway webhooks, and printable PDF receipts.
4. **Module 5 — Attendance, Exam Management, Question Bank, Offline/Online CBT, Results & Certificates**: High-concurrency computer-based test delivery, LAN sync for offline labs, automated rank calculation, and QR-verifiable certificates.
5. **Module 6 — Campus Operations & HR (Library, Inventory, Hostel, Transport, HR, Payroll, Communication, Reports & Analytics)**.
