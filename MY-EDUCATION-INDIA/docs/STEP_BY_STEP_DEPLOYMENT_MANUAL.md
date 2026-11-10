# MY EDUCATION INDIA ERP V2 — MASTER DEPLOYMENT RUNBOOK
## EXECUTABLE 8-STEP PRODUCTION CLOUD DEPLOYMENT MANUAL

### Step 1: Provision Neon PostgreSQL Database
1. Sign in to [Neon Console](https://console.neon.tech).
2. Create project `my-education-india` in region `ap-southeast-1` (Singapore).
3. Copy the **Pooled connection string** (Async: `postgresql+asyncpg://...`) and **Direct connection string** (Sync: `postgresql://...`).

### Step 2: Configure Environment Variables
Generate high-entropy 256-bit keys using OpenSSL:
```bash
openssl rand -hex 32
```
Prepare your environment variables for Render and Vercel following `.env.example`.

### Step 3: Deploy Backend on Render.com
1. Create a new Web Service pointing to `backend` root directory.
2. Build Command: `pip install -r requirements.txt && alembic upgrade head`.
3. Start Command: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`.
4. Health Check Path: `/health`.
5. Enter required environment variables (`DATABASE_URL`, `SYNC_DATABASE_URL`, `JWT_SECRET_KEY`, `INITIAL_SUPERADMIN_EMAIL`, `INITIAL_SUPERADMIN_PASSWORD`).

### Step 4: Verify Backend Health Probes
```bash
curl https://api.myeducation.in/health
# Expected: {"status": "healthy", "service": "MY EDUCATION INDIA ERP V2", "env": "production"}
```

### Step 5: Execute Initial Bootstrap Seeding
On Render shell or SSH console:
```bash
python3 -m scripts.seed_enterprise_foundation
```
This initializes **MY EDUCATION INDIA** (`MEI-HQ`), the 9 system roles, and seeds the Root Owner and Super Admin accounts.

### Step 6: Deploy Frontend on Vercel
1. In Vercel, import the repository and select `frontend` directory.
2. Build Command: `npm run build`, Output Directory: `dist`.
3. Add Environment Variables:
   - `VITE_API_URL`: `https://api.myeducation.in/api/v1`
   - `VITE_INSTITUTE_NAME`: `MY EDUCATION INDIA`
4. Click **Deploy**.

### Step 7: Configure GoDaddy DNS Records
Point your domain records:
- `A` record `@` -> `76.76.21.21` (Vercel)
- `CNAME` `admin` -> `cname.vercel-dns.com.` (Vercel)
- `CNAME` `api` -> `myeducation-backend.onrender.com.` (Render)

### Step 8: Production Verification Test
1. Access `https://admin.myeducation.in` and log in with your Super Admin credentials.
2. Navigate through the 20 institutional modules.
3. Access `/library/opac` to verify public search.
4. Verify system health at `/admin/platform/health`.
