# MY EDUCATION INDIA ERP V2 — BACKEND APPLICATION

## Overview
The backend application is an enterprise modular monolith built with **FastAPI**, **SQLAlchemy 2.x**, and **PostgreSQL (Neon)**. It provides unified data models, business logic engines, and REST API controllers for all 20 institutional modules.

## Directory Structure
- `app/`: Application core, database session, middleware, API v1 endpoints, and domain modules.
- `alembic/`: Database migrations across 20 sequential versioned revisions.
- `tests/`: Automated unit and integration test suites.
- `scripts/`: Production bootstrap and backup utility scripts.
- `requirements.txt`: Pinned production dependencies including `greenlet` and `sqlalchemy[asyncio]`.
- `pyproject.toml`: PEP 621 and Poetry dual-compatible packaging manifest.
- `poetry.lock`: Locked dependency graph.
- `.python-version` & `runtime.txt`: Standardized Python 3.11.9 runtime pin.
- `.env.example`: Production environment variables specification.

## Local Execution
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python3 -m scripts.seed_enterprise_foundation
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
