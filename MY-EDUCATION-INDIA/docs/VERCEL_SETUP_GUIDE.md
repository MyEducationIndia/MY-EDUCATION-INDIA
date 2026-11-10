# MY EDUCATION INDIA ERP V2 — VERCEL FRONTEND SETUP GUIDE

## 1. Project Import
1. In Vercel Dashboard, click **Add New** -> **Project**.
2. Import repository and set:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

## 2. Environment Variables
- `VITE_API_URL`: `https://api.myeducation.in/api/v1`
- `VITE_INSTITUTE_NAME`: `MY EDUCATION INDIA`

## 3. Custom Domain
Add `myeducation.in` and `admin.myeducation.in` in Project Settings -> Domains.
