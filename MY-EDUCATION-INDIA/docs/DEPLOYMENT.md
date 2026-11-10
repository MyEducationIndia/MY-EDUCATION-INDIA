# MY EDUCATION INDIA – Production Deployment Guide

Target Infrastructure:
* **Frontend:** Vercel Edge Hosting
* **Backend API:** Render Web Service (FastAPI + Uvicorn)
* **Database:** Neon Serverless PostgreSQL
* **Media Assets:** Cloudinary Asset Optimization
* **Caching & Queues:** Upstash Redis

---

## 1. Database Provisioning (Neon PostgreSQL)

1. Create a project at [Neon](https://neon.tech) named `my-education-india-prod`.
2. Select PostgreSQL version `15` and choose AWS Region `ap-south-1` (Mumbai) for minimum latency to Indore campus (`MEI-HQ`).
3. Under **Dashboard > Connection Details**, copy the connection string:
   * **Pooled AsyncPG URL (for FastAPI runtime):**
     `postgresql+asyncpg://<username>:<password>@<neon-host>-pooler.ap-south-1.aws.neon.tech/<dbname>?ssl=require`
   * **Direct Sync URL (for Alembic migrations):**
     `postgresql://<username>:<password>@<neon-host>.ap-south-1.aws.neon.tech/<dbname>?ssl=require`

---

## 2. Backend Deployment (Render)

1. Push your repository to GitHub.
2. In the [Render Dashboard](https://dashboard.render.com), select **New > Blueprint**.
3. Point to the repository. Render reads `render.yaml` automatically and configures:
   * Service `my-education-india-api`
   * Worker `my-education-india-worker`
4. In the Environment settings, populate the required secret keys:
   * `DATABASE_URL`: Your Neon AsyncPG connection string
   * `SYNC_DATABASE_URL`: Your Neon sync connection string
   * `SECRET_KEY`: 64-character hexadecimal crypto key
   * `JWT_SECRET_KEY`: 64-character hexadecimal signing key
   * `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
5. Trigger manual deploy. The build command runs `poetry install --no-root`, then executes `alembic upgrade head` before booting 4 Uvicorn workers.

---

## 3. Frontend Deployment (Vercel)

1. Log in to [Vercel](https://vercel.com) and click **Add New Project**.
2. Select your GitHub repository.
3. Configure the Project:
   * **Framework Preset:** Vite
   * **Root Directory:** `frontend`
   * **Build Command:** `npm run build`
   * **Output Directory:** `dist`
4. Environment Variables:
   * `VITE_API_BASE_URL`: `https://my-education-india-api.onrender.com/api/v1`
   * `VITE_CAMPUS_CODE`: `MEI-HQ`
5. Click **Deploy**. Vercel will build the React 18 production bundle, apply security headers defined in `vercel.json`, and route all client-side navigation via Single Page Application fallback.

---

## 4. Post-Deployment Verification Checklist

* [ ] Visit `https://your-domain.vercel.app` – Public website loads with zero console errors.
* [ ] Verify SSL certificates (HTTPS forced, HSTS enabled).
* [ ] Check `/api/v1/health` on Render backend – Returns HTTP 200 `healthy`.
* [ ] Attempt login at `/login` with invalid User ID – Verifies strict User ID + Password rejection.
* [ ] Visit `/root/feature-control` with Root Owner credentials – Verify all 85 feature flags load from PostgreSQL.
