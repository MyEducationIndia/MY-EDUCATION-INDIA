# MY EDUCATION INDIA ERP V2 — ENVIRONMENT VARIABLES GUIDE

| Variable Name | Required | Default / Format | Description |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | Yes | `production` / `development` | Deployment environment state |
| `APP_NAME` | Yes | `MY EDUCATION INDIA ERP` | Institutional application title |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Connection URI for async PostgreSQL database |
| `JWT_SECRET_KEY` | Yes | 256-bit Hex String | Secret key used for signing HS256 auth tokens |
| `JWT_ALGORITHM` | No | `HS256` | Token signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | Validity duration of access JWTs |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Sliding expiration duration for refresh tokens |
| `INITIAL_SUPERADMIN_EMAIL` | Yes | `superadmin@myeducation.in` | Bootstrap email address for root super admin |
| `INITIAL_SUPERADMIN_PASSWORD` | Yes | String | Secure password for initial super administrator |
| `CORS_ORIGINS` | No | `https://myeducation.in` | Comma-delimited list of allowed browser origins |
| `VAULT_MASTER_KEY` | Yes | 256-bit String | AES-256 master key for Credential Vault |
