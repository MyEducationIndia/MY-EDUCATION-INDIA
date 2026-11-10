# MY EDUCATION INDIA ERP V2 — DEVELOPER GUIDE

## 1. System Architecture Overview
MY EDUCATION INDIA ERP V2 is engineered as a high-performance **Enterprise Modular Monolith**. It provides comprehensive academic, administrative, financial, learning, and governance capabilities across 20 tightly integrated modules.

### Core Architectural Principles
- **Single-Institute Optimization**: Configured exclusively for **MY EDUCATION INDIA** (`MEI-HQ`).
- **Separation of Concerns**: Clean layers: `models` (SQLAlchemy 2.x declarative), `schemas` (Pydantic v2), `repositories` (async data access), `services` (business logic engines), and `router` (FastAPI controllers).
- **Strict Client-Side Storage Ban**: 100% compliant with enterprise security standards: zero usage of `localStorage`, `sessionStorage`, or `indexedDB`. Authentication tokens and sessions are managed exclusively through secure, HTTP-only cookies and in-memory caches.
- **Asynchronous I/O**: Full `async/await` execution for database operations (`asyncpg`), external API dispatches, and background queues.

## 2. Local Development Setup
### Prerequisites
- Python 3.11+
- Node.js 20+ & npm 10+
- PostgreSQL 15+ (or Neon Serverless Postgres)
- Redis 7+ (optional for background caching)

### Backend Initialization
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python3 -m scripts.seed_enterprise_foundation
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Initialization
```bash
cd frontend
npm install
npm run dev
```

## 3. Coding Standards & Conventions
- **Python**: PEP 8 style, strict type hints, Pydantic v2 request/response models.
- **TypeScript**: ESLint + Prettier, strict null checks, interface-first type contracts.
- **Git Commit Convention**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`).
