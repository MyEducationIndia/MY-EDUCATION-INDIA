# MY EDUCATION INDIA ERP V2 — GODADDY DNS CONFIGURATION GUIDE

## DNS Zone File Configuration (`myeducation.in`)

| Type | Name | Value | TTL | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **A** | `@` | `76.76.21.21` | 600 | Vercel Apex Frontend |
| **CNAME** | `www` | `cname.vercel-dns.com.` | 600 | Vercel WWW Redirect |
| **CNAME** | `admin` | `cname.vercel-dns.com.` | 600 | Vercel Admin Portal |
| **CNAME** | `api` | `myeducation-backend.onrender.com.` | 600 | Render API Endpoint |
