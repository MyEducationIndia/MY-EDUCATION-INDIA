# MY EDUCATION INDIA ERP V2 — RENDER.COM DEPLOYMENT GUIDE

## 1. Blueprint Configuration (`render.yaml`)
Deploy the entire ERP infrastructure to Render.com with a single click using the included `render.yaml` specification.

### Provisioned Resources
1. **Managed PostgreSQL**: High-availability Neon-backed PostgreSQL database.
2. **Web Service (Backend)**: FastAPI async web application with automatic TLS and health checks at `/api/v1/health`.
3. **Static Site (Frontend)**: React 19 Vite application with rewrite rules for client-side routing.
4. **Background Worker**: Celery / Asyncio worker processing automated scheduled backups, report generation, and SMS/WhatsApp queues.

## 2. Build Commands
- **Backend Build**: `pip install -r requirements.txt && alembic upgrade head`
- **Frontend Build**: `npm install && npm run build`
