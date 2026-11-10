# MY EDUCATION INDIA ERP V2 — PRE-PRODUCTION DEPLOYMENT GUIDE
## ZERO-ERROR DEPLOYMENT RUNBOOK: NEON POSTGRESQL • RENDER BACKEND • VERCEL FRONTEND

### 1. Architectural Topology Overview
This production runbook guides the complete zero-downtime, zero-error deployment of **MY EDUCATION INDIA ERP V2** across three decoupled enterprise cloud services:
1. **Database Layer**: Neon Serverless Managed PostgreSQL (High-availability connection pooling with SSL).
2. **Backend API & Queue Layer**: Render Web Service (FastAPI async modular monolith) + Background Task Worker.
3. **Frontend Presentation Layer**: Vercel Edge Network (React 19, Vite, Tailwind SPA with edge rewrites).
4. **Custom Domain Routing**: GoDaddy DNS pointing apex and subdomains (`myeducation.in`, `api.myeducation.in`, `admin.myeducation.in`).

---

### 2. Neon PostgreSQL Database Provisioning
1. **Create Project**:
   - Region: `ap-southeast-1` (Singapore) or closest Indian gateway.
   - Postgres Version: 15 or 16.
   - Database Name: `my_education_india`.
2. **Connection Strings**:
   - **Async URL (Backend Runtime)**:
     `postgresql+asyncpg://<user>:<password>@<neon-host>/my_education_india?ssl=require`
   - **Sync URL (Alembic Migrations)**:
     `postgresql://<user>:<password>@<neon-host>/my_education_india?sslmode=require`
3. **Connection Pooling**:
   - Utilize Neon's PgBouncer pooled endpoint (`-pooler`) for transaction pooling across web workers.

---

### 3. Render Backend & Worker Deployment
Deploy using the root `render.yaml` blueprint or manual service creation:

#### Web Service Specification
- **Environment**: Python 3.11
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
- **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`
- **Health Check Path**: `/health` (also supports `/ready`, `/live`, and `/api/v1/health`)
- **Required Environment Variables**:
  - `PYTHON_VERSION`: `3.11.9`
  - `APP_ENV`: `production`
  - `APP_NAME`: `MY EDUCATION INDIA ERP`
  - `DATABASE_URL`: Your Neon asyncpg connection string.
  - `SYNC_DATABASE_URL`: Your Neon psycopg connection string.
  - `SECRET_KEY`: High-entropy 256-bit secret generated via `openssl rand -hex 32`.
  - `JWT_SECRET_KEY`: High-entropy 256-bit secret.
  - `REFRESH_SECRET_KEY`: High-entropy 256-bit secret.
  - `CSRF_SECRET_KEY`: High-entropy 256-bit secret.
  - `VAULT_MASTER_KEY`: 256-bit secret for AES Credential Vault.
  - `INITIAL_SUPERADMIN_EMAIL`: `superadmin@myeducation.in`
  - `INITIAL_SUPERADMIN_PASSWORD`: Strong initial administrative passphrase.
  - `CORS_ORIGINS`: `https://myeducation.in,https://admin.myeducation.in,https://vercel.app`

#### Background Worker Specification
- **Type**: Background Worker
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m app.workers.background_scheduler`
- **Environment Variables**: Mirror database and system keys from web service.

---

### 4. Vercel Frontend Deployment
1. **Import Git Repository**: Select root directory or set Root Directory to `frontend`.
2. **Framework Preset**: `Vite`.
3. **Build Command**: `npm run build`.
4. **Output Directory**: `dist`.
5. **Environment Variables**:
   - `VITE_API_URL`: `https://api.myeducation.in/api/v1`
   - `VITE_INSTITUTE_NAME`: `MY EDUCATION INDIA`
6. **Vercel Rewrites (`vercel.json`)**:
   Automatically rewrites all client-side paths `/(.*)` to `/index.html` with security headers (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`).

---

### 5. GoDaddy Custom Domain DNS Records
In your GoDaddy DNS Manager for `myeducation.in`, configure:
- **Apex Record**: `A` record `@` -> Vercel IP `76.76.21.21`
- **Frontend CNAME**: `CNAME` `www` -> `cname.vercel-dns.com.`
- **Admin Subdomain**: `CNAME` `admin` -> `cname.vercel-dns.com.`
- **API Subdomain**: `CNAME` `api` -> `myeducation-backend.onrender.com.`

---

### 6. Database Migration & Rollback Runbook
- **Upgrade Migrations**:
  ```bash
  alembic upgrade head
  ```
- **Verify Current Revision**:
  ```bash
  alembic current
  ```
- **Step-by-Step Rollback (if necessary)**:
  ```bash
  alembic downgrade -1
  ```
- **Automated Nightly Backup**:
  Backup engine snapshots database schema and tables to AES-256 encrypted archives verified with SHA-256 checksums.
