# MY EDUCATION INDIA ERP V2
# MODULE 2: ENTERPRISE AUTHENTICATION & AUTHORIZATION SPECIFICATION

## 1. Architectural Scope & Foundation

Module 2 delivers a **production-grade enterprise authentication and authorization system** that forms the security backbone of **MY EDUCATION INDIA ERP V2**. All authentication state is managed through **PostgreSQL-backed sessions**, **HttpOnly, Secure, SameSite=Strict cookies**, and **volatile in-memory client state**. In compliance with enterprise security requirements:
- **Zero LocalStorage, SessionStorage, or IndexedDB** usage anywhere in the frontend.
- **Argon2id password hashing** with PBKDF2-HMAC-SHA256 (600,000 iterations) fallback.
- **Token Family Reuse Detection**: revoking all active sessions in a family immediately upon detected replay.
- **Fine-Grained Permission Engine**: supporting exact codes (e.g. `student.view`) and wildcard scopes (e.g. `student.*`, `*`).
- **Configurable Multi-Identifier Login**: dynamically resolving users by Email, Username, Mobile Number, Roll Number, Registration Number, Enrollment Number, ERP ID, Student ID, or custom field based on institutional settings stored in PostgreSQL.

---

## 2. Database Schema (PostgreSQL 16+ via Alembic Migration `0002_module2_enterprise_auth.py`)

| Table Name | Entity Class | Purpose & Security Attributes |
| :--- | :--- | :--- |
| `users` | `User` | Core user identity with Argon2id password hash, lockout tracking (`failed_login_attempts`, `locked_until`), configurable identifier columns (`registration_number`, `enrollment_number`, `roll_number`, `erp_id`, `student_id`), and password history ring buffer (`password_history`). |
| `roles` | `Role` | Subdomain-scoped RBAC roles (`SUPER_ADMIN`, `INSTITUTE_ADMIN`, `FACULTY`, `STUDENT`, etc.) and unlimited custom roles created by administrators. |
| `permissions` | `Permission` | Atomic institutional permissions (`student.view`, `fees.manage`, `attendance.manage`, `exam.manage`, `cms.manage`, `settings.manage`, `backup.manage`, `restore.manage`, `communication.manage`, `reports.export`, etc.). |
| `role_permissions` | Association | Many-to-many relationship linking permissions to roles. |
| `user_roles` | Association | Many-to-many relationship assigning roles to users. |
| `login_history` | `LoginHistory` | Immutable record of all login events: timestamp, identifier used, criterion, status (`SUCCESS`, `FAILED`, `LOCKED`), failure reason, IP address, user agent, device type, browser, OS, and session ID. |
| `refresh_tokens` | `RefreshToken` | PostgreSQL-stored refresh token sessions with SHA-256 token hash, `token_family` lineage, device info, client IP, expiration, and revocation status/timestamp. |
| `password_reset_tokens` | `PasswordResetToken` | Secure cryptographic tokens with 1-hour expiration and single-use enforcement for account recovery. |
| `email_verification_tokens`| `EmailVerificationToken` | Single-use email verification tokens. |
| `system_settings` | `SystemSetting` | Dynamic JSONB configuration table for authentication parameters (`auth_config`), password complexity policies, session timeouts, and login criteria. |
| `audit_logs` | `AuditLog` | Comprehensive security and administrative audit trail with actor ID, action, HTTP method, path, status, IP, device, browser, and JSONB delta payload. |

---

## 3. Backend Module Structure (`backend/app/modules/auth/`)

```
backend/app/modules/auth/
├── __init__.py
├── constants.py          # Default system roles (13 types), permissions (19 granular codes), and default auth policies
├── exceptions.py         # Domain-specific enterprise exceptions (InvalidCredentials, AccountLocked, TokenRevoked, etc.)
├── models.py             # SQLAlchemy 2.x Mapped models for all 11 tables/entities
├── schemas.py            # Pydantic v2 validation models for requests and responses
├── security.py           # Argon2id/PBKDF2 hashing, password policy validation, history check, and token generation
├── jwt.py                # JWT access and refresh token signing, decoding, and expiration validation
├── native_jwt.py         # RFC 7519 HMAC-SHA256 JWT fallback implementation
├── permissions.py        # PermissionEngine evaluating user permissions, wildcards, and role memberships
├── repository.py         # Async data access layer with parameterized ORM queries preventing SQL injection
├── service.py            # Enterprise auth business logic, brute-force mitigation, and session rotation
├── dependencies.py       # FastAPI dependencies: get_current_user, require_permissions, require_roles, enforce_csrf
└── router.py             # API routers for /api/v1/auth and /api/v1/auth/admin endpoints
```

---

## 4. Frontend Module Structure (`frontend/src/modules/auth/`)

```
frontend/src/modules/auth/
├── types/
│   └── auth.types.ts     # TypeScript interfaces for user profiles, sessions, history, and policies
├── api/
│   └── authApi.ts        # Axios API client functions with HttpOnly cookie credentials
├── services/
│   └── authService.ts    # Session management and volatile in-memory token synchronization
├── context/
│   └── AuthContext.tsx   # React Context provider supplying user state, dark mode toggle, and permission checks
├── hooks/
│   ├── useAuth.ts        # Primary authentication hook
│   └── usePermissions.ts # Fine-grained permission and role evaluation hook
├── components/
│   ├── ProtectedRoute.tsx # Route guard checking session validity before rendering protected child routes
│   ├── RoleGuard.tsx      # Guard checking user roles with redirect to 403 Forbidden
│   └── PermissionGuard.tsx# Guard checking granular permissions with wildcard support
├── pages/
│   ├── LoginPage.tsx      # Adaptable login page with criteria switcher, show/hide password, remember me, forgot modal, dark mode
│   ├── UnauthorizedPage.tsx# Custom 401 Unauthorized page
│   ├── ForbiddenPage.tsx   # Custom 403 Access Forbidden page
│   ├── ActiveSessionsPage.tsx # Active PostgreSQL session monitoring and force logout
│   └── LoginHistoryPage.tsx   # Immutable institutional login history table
└── routes/
    └── AuthRoutes.tsx     # Route mapping for public authentication flows
```

---

## 5. Security Architecture & Threat Protection

1. **Zero-LocalStorage Rule**: Tokens are never placed in browser `localStorage`, `sessionStorage`, or `indexedDB`. The short-lived JWT access token lives strictly in JavaScript closure memory (`authMemoryStore.ts`). The refresh token is delivered exclusively as an `HttpOnly`, `Secure`, `SameSite=Strict` cookie bound to `/api/v1/auth`.
2. **Brute Force & Lockout Mitigation**: Failed login attempts are recorded in PostgreSQL. After 5 consecutive failed attempts, the account is temporarily locked for 15 minutes (`AccountLockedException`), and the security event is written to both `login_history` and `audit_logs`.
3. **Token Reuse & Replay Detection**: Every refresh token belongs to a `token_family`. When a refresh token is used, it is rotated. If an already-rotated token is re-submitted (indicating token theft), the entire `token_family` is revoked immediately (`TokenRevokedException`).
4. **CSRF Protection**: All state-modifying requests (`POST`, `PUT`, `PATCH`, `DELETE`) require an `X-CSRF-Token` header containing an HMAC-SHA256 signature linked to the user's active session ID.
5. **Password History & Complexity**: Passwords must satisfy length, uppercase, lowercase, numeric, and special character criteria. Reusing any of the user's last 5 passwords raises `PasswordHistoryException`.

---

## 6. Verification & Automated Test Results

The automated test suite in `tests/unit/test_module2_backend_auth.py` and `tests/unit/test_module1_architecture_and_schemas.py` confirms:
- 100% clean AST compilation across all backend files.
- Full verification of password policy rules and password history ring buffer prevention.
- JWT access and refresh token encoding, decoding, claims validation, and remember-me duration handling.
- Permission engine evaluation across exact permissions, wildcards, and super admin privileges.
- Zero occurrences of `localStorage`, `sessionStorage`, or `indexedDB` across all TypeScript source files.
- All 10 unit test cases passing (`OK`).
