# MY EDUCATION INDIA ERP V2 — INSTALLATION GUIDE

## 1. Prerequisites Check
Ensure the following software packages are installed on your host system:
- Git
- Python 3.11 or later (`python3 --version`)
- Node.js 20.x or later (`node --version`)
- PostgreSQL 15 or cloud database connection string

## 2. Environment Configuration
Clone the repository and copy the environment configuration:
```bash
cp .env.example .env
```
Edit `.env` to configure your database URL, JWT secret keys, and institute parameters:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/my_education_india
JWT_SECRET_KEY=your-super-secure-256-bit-secret-key-here
INITIAL_SUPERADMIN_EMAIL=superadmin@myeducation.in
INITIAL_SUPERADMIN_PASSWORD=EduIndia#Production2026!
```

## 3. Database Migration & Baseline Seeding
Run Alembic migrations to construct all 20 modules' relational tables:
```bash
cd backend
alembic upgrade head
python3 -m scripts.seed_enterprise_foundation
```

## 4. Verification
Launch the backend and verify the health check endpoint:
```bash
curl http://localhost:8000/api/v1/health
# Response: {"status": "healthy", "institute": "MY EDUCATION INDIA"}
```
