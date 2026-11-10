# MY EDUCATION INDIA – Local & Server Installation Guide

**Campus Standard:** Node `MEI-HQ` (Indore Autonomous Campus)  
**Release:** `v1.0.0-PRODUCTION`

---

## 1. Prerequisites

Ensure your host machine satisfies the following hardware and software specifications:
* **Operating System:** Linux (Ubuntu 22.04 LTS recommended), macOS (13+), or Windows with WSL2
* **Python Runtime:** Python 3.11.x (with `pip` and `poetry` 1.8+)
* **Node.js Runtime:** Node.js 20.x LTS (with `npm` 10+)
* **Database Engine:** PostgreSQL 15+ (Local or Neon Serverless instance)
* **In-Memory Cache:** Redis 7+ (Local or Upstash instance)

---

## 2. Repository Setup

```bash
# Clone the repository
git clone https://github.com/my-education-india/enterprise-platform.git
cd enterprise-platform
```

---

## 3. Backend Setup & Startup

```bash
cd backend

# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies (excluding dev tools in production)
poetry install --no-root

# Configure environment variables
cp ../.env.production.example .env
# Edit .env with your PostgreSQL and secret key parameters

# Run database schema migrations
poetry run alembic upgrade head

# Start local development server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify backend health:
```bash
curl http://localhost:8000/api/v1/health
# Response: {"status":"healthy","version":"1.0.0","campus":"MEI-HQ"}
```

---

## 4. Frontend Setup & Startup

```bash
cd ../frontend

# Install node dependencies
npm ci

# Start development server
npm run dev
```

Visit `http://localhost:5173` in your browser.

---

## 5. Dockerized Orchestration (Single Command)

To run the entire platform with local PostgreSQL and Redis:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

Services initialized:
* **Frontend:** `http://localhost`
* **API Service:** `http://localhost:8000`
* **PostgreSQL:** `localhost:5432` (`my_education_india`)
* **Redis:** `localhost:6379`
