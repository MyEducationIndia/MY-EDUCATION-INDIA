# MY EDUCATION INDIA ERP V2
### Enterprise Modular Monolith Educational ERP, LMS, CBT & Governance Platform

## Overview
**MY EDUCATION INDIA ERP V2** is a mission-critical, enterprise-grade institutional management system built specifically for the national flagship campus: **MY EDUCATION INDIA** (`MEI-HQ`, Indore, Madhya Pradesh).

The platform consolidates 20 complete institutional sub-systems into a unified, secure, high-performance architecture:
1. **Module 1**: Architecture, Security & Multitenancy Foundation
2. **Module 2**: Enterprise Authentication, JWT Lifecycle & RBAC
3. **Module 3**: Core System Engine, Atomic Numbering & Localization
4. **Module 4**: Enterprise Admin Dashboard & Operational Control Center
5. **Module 5**: Website CMS & Dynamic Landing Page Studio
6. **Module 6**: Enterprise Student Information Management System (SIMS)
7. **Module 7**: Admission Pipeline & CRM Management System
8. **Module 8**: Academic Backbone, Curriculum & Timetable
9. **Module 9**: Fee & Finance Management System
10. **Module 10**: Attendance & Leave Management (QR & Biometric Ready)
11. **Module 11**: Examination, Grading, Transcripts & SGPA/CGPA
12. **Module 12**: Computer Based Testing (CBT) Platform
13. **Module 13**: Certificate Generation & Digital Verification
14. **Module 14**: Library & Digital Knowledge Management System
15. **Module 15**: Learning Experience Platform (LXP)
16. **Module 16**: Universal API Integration Framework & Credential Vault
17. **Module 17**: Enterprise CRM, Sales Pipeline & Franchise Management
18. **Module 18**: Centralized Reports, Analytics & Business Intelligence
19. **Module 19**: Platform Administration, Security & DevOps Center
20. **Module 20**: Enterprise Experience Platform & Root Owner Control

## Standard Directory Structure
```text
MY-EDUCATION-INDIA/
├── backend/                  # FastAPI 0.109, SQLAlchemy 2.0 Async, Alembic
│   ├── app/                  # Application code, routers, models, engines
│   ├── alembic/              # 20 sequential database migrations (0001 - 0020)
│   ├── tests/                # Unit test suites across all 20 modules
│   ├── scripts/              # Production bootstrap & database maintenance
│   ├── requirements.txt      # Production dependencies (greenlet, sqlalchemy[asyncio])
│   ├── requirements-dev.txt  # Development & test tools
│   ├── pyproject.toml        # PEP 621 & Poetry dual packaging manifest
│   ├── poetry.lock           # Locked reproducible dependency graph
│   ├── .python-version       # Python 3.11.9
│   ├── runtime.txt           # python-3.11.9
│   ├── .env.example          # Backend configuration reference
│   └── README.md
├── frontend/                 # React 19, TypeScript, Vite, Tailwind CSS
│   ├── src/                  # Role portals, visual builders, component library
│   ├── public/               # Static assets, manifest, robots.txt
│   ├── package.json          # Node dependency manifest
│   ├── vite.config.ts        # Vite build configuration
│   ├── vercel.json           # Vercel SPA routing & security headers
│   ├── .env.example          # Frontend API URL configuration
│   └── README.md
├── docker/                   # Multi-stage container specifications
│   ├── Dockerfile.backend    # Non-root secure Python 3.11 container
│   ├── Dockerfile.frontend   # Nginx 1.25 Alpine edge container
│   ├── docker-compose.yml    # Multi-service stack orchestration
│   └── nginx.conf            # Reverse proxy & security headers
├── docs/                     # 10 Comprehensive Deployment & Setup Guides
├── scripts/                  # Enterprise bootstrap & backup scripts
├── .gitignore
├── LICENSE
├── README.md
└── render.yaml               # Render Infrastructure as Code specification
```

## Quick Start
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   python3 -m scripts.seed_enterprise_foundation
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
