# MY EDUCATION INDIA ERP V2 — MODULE 19 SPECIFICATION
## ENTERPRISE PLATFORM ADMINISTRATION, SECURITY, BACKUP & DEVOPS CENTER

### 1. Executive Summary & Architectural Overview
Module 19 establishes the **Centralized Platform Operations, Security, Disaster Recovery, and DevOps Control Center** for MY EDUCATION INDIA ERP V2. It governs system-wide configurations, multitenant security policies, automated backups, restore drills, feature toggles, object storage quotas, API keys, and cluster health monitoring across all 18 upstream ERP modules.

#### Key Architectural Highlights
- **Centralized Platform Governance**: Eliminates decentralized administration logic by aggregating global branding, localization, currency formats, academic calendar boundaries, and session policies into a single configurable vault.
- **Enterprise Security & Policy Enforcement (`security_engine.py`)**:
  - Enforces password complexity rules (minimum 10 characters, uppercase, digits, symbols).
  - Failed login attempt tracking with automated account lockout thresholds (5 failed attempts = 30-minute lockout).
  - Multi-subnet IP CIDR whitelisting and session timeout governance.
- **Disaster Recovery & Automated Backup Engine (`backup_engine.py`, `restore_engine.py`)**:
  - Full, incremental, database-only, and files-only scheduled backup snapshots with SHA-256 integrity checksum verification.
  - Multi-destination storage support: Local volume, AWS S3, and Cloudflare R2.
  - Non-mutating dry-run restore simulator executing schema verification and foreign key consistency checks before rollback.
- **Deterministic Feature Flag Engine (`feature_flag_engine.py`)**:
  - Hash-based canary rollouts (0–100%) using MD5 hashing over `flag_key:user_id` for deterministic bucket allocation.
  - Granular role-based and branch-based target filtering for beta feature testing without redeployments.
- **Cluster Telemetry & Health Monitoring (`health_engine.py`)**:
  - Real-time latency tracking for API gateways, PostgreSQL connection pools, background queue workers, and Redis cache hit rates.
- **Enterprise License & Subscription Management**:
  - Enforces student enrollment quotas, branch allocations, and storage tier limits with automated expiry warnings.
- **Zero Client-Side Storage**: 100% compliant with zero usage of `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (17 Enterprise Relational Tables)
Provisioned via Alembic revision `0019_platform_devops`:
1. `platform_settings`: Key-value configuration for branding, localization, timezones, and currencies.
2. `security_policies`: Password complexity, lockout durations, session timeouts, and IP CIDR ranges.
3. `backup_jobs`: Scheduled cron jobs, compression formats (GZIP/ZSTD), destinations, and retention periods.
4. `backup_history`: Historical backup archives, SHA-256 checksums, execution durations, and file sizes.
5. `restore_history`: Disaster recovery logs, restore scopes, dry-run flags, and operator user IDs.
6. `audit_events`: Chronological audit trail of user logins, financial modifications, and permission shifts.
7. `system_logs`: Multitenant application logs with log levels (DEBUG, INFO, WARN, ERROR, CRITICAL) and stack traces.
8. `api_keys`: Hashed API secrets, key prefixes, scope lists, rate limits, and expiration dates.
9. `api_usage_logs`: Outbound and inbound API telemetry with HTTP status codes and latency in milliseconds.
10. `integration_configs`: Connected third-party cloud service credentials and health statuses.
11. `feature_flags`: Dynamic feature switches with percentage rollouts, role targets, and branch filters.
12. `storage_configs`: S3/R2 bucket pointers, storage quotas, and automated cleanup retention rules.
13. `cache_logs`: Cache warming, key eviction logs, and affected key counts.
14. `health_checks`: Microservice latency telemetry, uptime checks, and diagnostic payloads.
15. `license_settings`: Institutional license keys, student/branch limits, and feature entitlements.
16. `maintenance_windows`: Scheduled downtime windows, IP whitelists, and custom broadcast notices.
17. `platform_reports`: Pre-built DevOps compliance audits, backup verification reports, and SLA summaries.

---

### 3. Business Logic & Calculation Engines
- **Enterprise Backup Engine (`backup_engine.py`)**:
  - SHA-256 checksum computation for cryptographic verification.
  - Standardized archive naming: `backup_{institute_id}_{backup_type}_{timestamp}.tar.gz`.
  - Retention evaluator checking age against retention limits.
- **Disaster Recovery Engine (`restore_engine.py`)**:
  - Validates completed backup status and checksum integrity.
  - Generates multi-phase dry-run restore plans.
- **Platform Security Engine (`security_engine.py`)**:
  - Evaluates password complexity violations across length, uppercase, numbers, and special characters.
  - Enforces account lockout rules upon reaching maximum failed login attempts.
- **Feature Flag Evaluation Engine (`feature_flag_engine.py`)**:
  - Evaluates deterministic MD5 hash buckets (0–99) for canary rollouts.
  - Enforces role-based override rules.
- **Cluster Health Engine (`health_engine.py`)**:
  - Synthesizes health telemetry across database, API gateway, cache, and background queues.

---

### 4. Frontend & Navigation Architecture
- **Path**: `frontend/src/modules/platform/`
- **14 Submodules Delivered**:
  - `dashboard/PlatformDashboardPage.tsx`: Executive DevOps operations command center (System Health, DB Status, Storage 42.8/500 GB, Backup Status).
  - `settings/SystemSettingsPage.tsx`: Global branding, localization, currency, and academic calendar bounds.
  - `security/SecurityCenterPage.tsx`: Enterprise password complexity, failed login lockout, and IP CIDR restrictions.
  - `backups/BackupManagerPage.tsx`: Automated backup scheduling with AES encryption and SHA-256 validation.
  - `restores/RestoreManagerPage.tsx`: Disaster recovery runner with non-mutating dry-run verification.
  - `feature-flags/FeatureFlagsPage.tsx`: Feature toggle studio with percentage rollout sliders and role targeting.
  - `storage/StorageManagerPage.tsx`: Object storage pool quotas, retention policies, and media buckets.
  - `health/ClusterHealthPage.tsx`: Real-time infrastructure health and cluster telemetry.
  - `audit/AuditCenterPage.tsx`: Enterprise audit center and immutable activity logs.
  - `licenses/LicenseManagerPage.tsx`: Institutional license keys and enrollment quota governance.
  - `maintenance/MaintenanceModePage.tsx`: Scheduled maintenance windows and custom notice banners.
  - `reports/PlatformReportsPage.tsx`: DevOps compliance audits, SLA uptime records, and backup logs.
  - `types/platform.types.ts` & `services/platformService.ts`: TypeScript contracts and HTTP API client.
- **Routing**: Mounted under `/admin/platform/*` in `AppRoutes.tsx` with navigation item `DevOps & Platform` (`Terminal` icon).

---

### 5. Verification & Testing
- Unit test suite `tests/unit/test_module19_backend_platform.py` executed with 100% pass rate:
  - Clean AST syntax across all 14 Python files in `backend/app/modules/platform/`.
  - Pydantic schema validation for platform settings, security policies, backup jobs, and feature flags.
  - Cron syntax, IP CIDR, rollout percentage, and password policy validators.
  - Backup SHA-256 checksum computation, standardized archive naming, and retention age logic.
  - Disaster recovery prerequisite checks and dry-run restore plan simulation.
  - Password complexity verification and failed login attempt lockout states.
  - Deterministic hash-bucket percentage feature flag rollouts and role targeting.
  - Zero browser storage audit: 0 instances of `localStorage`, `sessionStorage`, or `indexedDB`.
