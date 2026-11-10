# MY EDUCATION INDIA ERP V2 — BACKEND DEPLOYMENT GUIDE

## 1. Architecture Overview
- **Framework**: FastAPI (Asynchronous ASGI)
- **Runtime**: Python 3.11.9
- **Database Engine**: SQLAlchemy 2.0 Async (`asyncpg`) with connection pooling (20 pool size + 10 max overflow)
- **Hosting Targets**: Render Web Service, Linux VPS (Gunicorn + Uvicorn), or Docker container.

## 2. Production Startup Command
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT --timeout 60
```

## 3. Health Monitoring Endpoints
- `/health`: Liveness probe for load balancers.
- `/ready`: Readiness probe verifying database connectivity.
- `/live`: Basic process heartbeat.
- `/api/v1/health`: API v1 service catalog health probe.
