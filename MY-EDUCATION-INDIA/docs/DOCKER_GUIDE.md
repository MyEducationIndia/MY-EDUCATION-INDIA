# MY EDUCATION INDIA ERP V2 — DOCKER DEPLOYMENT GUIDE

## 1. Multi-Stage Dockerfile
The ERP provides production Dockerfiles for both Backend and Frontend:
- **Backend**: Python 3.11 slim image with non-root security user (`spark`).
- **Frontend**: Node 20 builder compiled into lightweight Nginx Alpine container.

## 2. Docker Compose Orchestration
Run the complete production stack using `docker-compose.yml`:
```bash
docker compose up -d --build
```

### Services Included
1. `backend`: FastAPI async application container mounted on port 8000.
2. `frontend`: React 19 production bundle served via Nginx on port 80.
3. `postgres`: PostgreSQL 15 database engine with persistent volume mapping.
4. `redis`: In-memory cache and background task queue worker broker.

## 3. Container Health Checks
```bash
docker compose ps
docker compose logs -f backend
```
