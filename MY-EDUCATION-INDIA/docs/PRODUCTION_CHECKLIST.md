# MY EDUCATION INDIA ERP V2 — PRODUCTION PRE-FLIGHT CHECKLIST

- [x] Python 3.11.9 pinned across `.python-version`, `runtime.txt`, `pyproject.toml`, and `render.yaml`.
- [x] Dependencies include `greenlet>=3.0.3` and `sqlalchemy[asyncio]>=2.0.27`.
- [x] Zero client-side storage (`localStorage`/`sessionStorage`/`indexedDB`) verified in frontend code.
- [x] All 20 Alembic migrations tested and verified against PostgreSQL 15/16.
- [x] Seed script initialized for single institute 'MY EDUCATION INDIA' (`MEI-HQ`).
- [x] Strictly 2 system accounts: Root Owner and Super Admin.
- [x] API health probes mounted at `/health`, `/ready`, `/live`, and `/api/v1/health`.
- [x] Vercel `vercel.json` SPA routing configured with security headers.
- [x] Multi-stage Dockerfiles verified for non-root execution.
