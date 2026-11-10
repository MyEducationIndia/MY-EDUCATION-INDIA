# MY EDUCATION INDIA ERP V2 — NEON POSTGRESQL SETUP GUIDE

## 1. Project Initialization
1. Sign in to [Neon.tech](https://neon.tech).
2. Create Project:
   - **Name**: `my-education-india`
   - **Region**: `ap-southeast-1` (Singapore)
   - **PostgreSQL Version**: 15 or 16
   - **Database Name**: `my_education_india`

## 2. Connection URIs
- **Pooled Async URL (Backend Runtime)**:
  `postgresql+asyncpg://<username>:<password>@<neon-endpoint>-pooler.ap-southeast-1.neon.tech/my_education_india?ssl=require`
- **Direct Sync URL (Alembic Migrations)**:
  `postgresql://<username>:<password>@<neon-endpoint>.ap-southeast-1.neon.tech/my_education_india?sslmode=require`

## 3. Performance Best Practices
- Enable PgBouncer connection pooling for transaction pooling across web workers.
- Set connection pool timeout to 30 seconds.
