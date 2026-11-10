# MY EDUCATION INDIA – Environment Variables Reference Guide

All environment variables used across the platform are documented below with their default values, scope, and production recommendations.

---

## 1. Application & Server Settings

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | String | `development` | Runtime environment (`development`, `staging`, `production`) |
| `DEBUG` | Boolean | `false` | Enable verbose error traces and query echo (MUST be false in production) |
| `APP_NAME` | String | `MY EDUCATION INDIA` | Platform brand name for email notices, page headers, and API meta |
| `APP_VERSION` | String | `1.0.0` | Active semantic release version |
| `CAMPUS_CODE` | String | `MEI-HQ` | Primary autonomous institution branch code |
| `CAMPUS_CITY` | String | `Indore` | Campus physical node city |
| `CAMPUS_STATE` | String | `Madhya Pradesh` | Campus geographic state |
| `SERVER_HOST` | String | `0.0.0.0` | IP binding for Uvicorn HTTP server |
| `SERVER_PORT` | Integer | `8000` | Port binding for HTTP server |

---

## 2. Database & Connection Pooling (PostgreSQL / Neon)

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | String | Required | Async connection string: `postgresql+asyncpg://user:pass@host/db?ssl=require` |
| `SYNC_DATABASE_URL` | String | Required | Sync connection string for Alembic: `postgresql://user:pass@host/db?ssl=require` |
| `DB_POOL_SIZE` | Integer | `20` | Core connection pool size for FastAPI workers |
| `DB_MAX_OVERFLOW` | Integer | `10` | Temporary connection spike allowance |
| `DB_POOL_TIMEOUT` | Integer | `30` | Seconds to wait before timing out connection acquisition |

---

## 3. Cryptography & Authentication Policies

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `SECRET_KEY` | String (Hex) | Required | Master encryption secret for AES-256 GCM tokenization |
| `JWT_SECRET_KEY` | String (Hex) | Required | HMAC key for signing RS256 / HS256 authentication tokens |
| `JWT_ALGORITHM` | String | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Integer | `60` | In-memory access token TTL |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Integer | `7` | HttpOnly cookie refresh token TTL |
| `ALLOWED_AUTH_METHODS` | JSON | `["USER_ID_PASSWORD"]` | Strict allowed login methods |
| `ALLOW_FORGOT_PASSWORD` | Boolean | `false` | Public self-service password reset toggle (Disabled by default) |

---

## 4. Session & Lockdown Policies

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `SESSION_TIMEOUT_MINUTES` | Integer | `60` | Maximum absolute duration of an authenticated session |
| `IDLE_TIMEOUT_MINUTES` | Integer | `15` | Inactivity threshold before automatic session termination |
| `MAX_CONCURRENT_SESSIONS` | Integer | `1` | Max concurrent device sessions allowed per User ID |
| `SINGLE_DEVICE_LOGIN_ENFORCED`| Boolean | `true` | Terminate earlier session on new device login |
| `AUTO_LOGOUT_ON_IDLE` | Boolean | `true` | Enforce client-side ping idle auto-logout |

---

## 5. Media & Cloud Storage

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `MEDIA_PROVIDER` | String | `cloudinary` | Storage engine (`cloudinary`, `s3`, `local`) |
| `CLOUDINARY_CLOUD_NAME` | String | Required | Cloudinary organization identifier |
| `CLOUDINARY_API_KEY` | String | Required | Cloudinary API access key |
| `CLOUDINARY_API_SECRET` | String | Required | Cloudinary API secret |

---

## 6. CORS & Cookie Policies

| Variable Name | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `ALLOWED_ORIGINS` | JSON Array | `["https://my-education-india.vercel.app"]` | Whitelisted cross-origin origins |
| `COOKIE_DOMAIN` | String | `.myeducationindia.com` | Top-level cookie domain |
| `COOKIE_SECURE` | Boolean | `true` | Enforce HTTPS-only transmission of auth cookies |
| `COOKIE_SAMESITE` | String | `strict` | Cross-site request forgery prevention |
