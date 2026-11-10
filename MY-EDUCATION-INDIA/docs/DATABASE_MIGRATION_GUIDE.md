# MY EDUCATION INDIA ERP V2 — DATABASE MIGRATION GUIDE

## 1. Migration Architecture
- Tool: Alembic
- Sequential Revisions: 20 migrations (`0001` to `0020`).
- Driver: `psycopg2-binary` via `SYNC_DATABASE_URL`.

## 2. Execution Commands
```bash
# Upgrade to latest revision
alembic upgrade head

# Check current revision status
alembic current

# Rollback single revision
alembic downgrade -1
```

## 3. Seed Production Baseline
```bash
python3 -m scripts.seed_enterprise_foundation
```
