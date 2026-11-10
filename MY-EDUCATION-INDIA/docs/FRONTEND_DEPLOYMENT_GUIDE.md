# MY EDUCATION INDIA ERP V2 — FRONTEND DEPLOYMENT GUIDE

## 1. Architecture Overview
- **Framework**: React 19 + TypeScript + Vite + Tailwind CSS
- **Routing**: React Router with Single Page Application (SPA) client-side routing.
- **Hosting Targets**: Vercel Edge Network, Cloudflare Pages, or Nginx Docker container.

## 2. Build Pipeline
```bash
npm install
npm run build
```
- **Output Directory**: `dist`
- **Build Output**: Optimized ES modules, CSS bundles, and static assets.

## 3. SPA Routing Configuration (`vercel.json`)
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [{ "source": "/(.*)", "destination": "/" }]
}
```
