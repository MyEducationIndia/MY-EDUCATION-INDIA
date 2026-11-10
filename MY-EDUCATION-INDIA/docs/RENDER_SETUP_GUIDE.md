# MY EDUCATION INDIA ERP V2 — RENDER.COM DEPLOYMENT GUIDE

## 1. Infrastructure-as-Code Deployment (`render.yaml`)
1. In Render Dashboard, click **New** -> **Blueprint**.
2. Connect your Git repository.
3. Render reads `render.yaml` and provisions:
   - `myeducation-backend` (Web Service, Python 3.11)
   - `myeducation-worker` (Background Worker)
   - `myeducation-postgres` (Managed PostgreSQL Database)

## 2. Manual Service Configuration
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
- **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT`
- **Health Check Path**: `/health`
- **Auto Deploy**: Enabled on push to `main`.
