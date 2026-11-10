# MY EDUCATION INDIA ERP V2 — ENVIRONMENT VARIABLES REFERENCE

| Variable | Required | Default / Value | Description |
| :--- | :---: | :--- | :--- |
| `APP_ENV` | Yes | `production` | Application operational mode |
| `APP_NAME` | Yes | `MY EDUCATION INDIA ERP` | Institutional brand name |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Asynchronous Neon database connection string |
| `SYNC_DATABASE_URL`| Yes | `postgresql://...` | Synchronous psycopg string for Alembic |
| `SECRET_KEY` | Yes | 256-bit Hex String | Secret key for CSRF and signing |
| `JWT_SECRET_KEY` | Yes | 256-bit Hex String | JWT signature token key |
| `REFRESH_SECRET_KEY`| Yes | 256-bit Hex String | Refresh token secret key |
| `VAULT_MASTER_KEY`| Yes | 256-bit Hex String | AES-256 key for Credential Vault |
| `INITIAL_SUPERADMIN_EMAIL` | Yes | `superadmin@myeducation.in` | Root Super Admin bootstrap email |
| `INITIAL_SUPERADMIN_PASSWORD` | Yes | String | Root Super Admin bootstrap password |
| `CORS_ORIGINS` | No | `https://myeducation.in,...` | Permitted browser origins |
