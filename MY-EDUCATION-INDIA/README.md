# MY EDUCATION INDIA – Enterprise Unified Autonomous Campus Platform

**Version:** `1.0.0-PRODUCTION`  
**Campus Node:** `MEI-HQ` (Autonomous Campus, Indore, Madhya Pradesh, India)  
**Architecture:** Multi-Tier Micro-Modular Monolith (FastAPI + React 18 + PostgreSQL + Redis)

---

## 1. Executive Summary

MY EDUCATION INDIA is a sovereign, enterprise-grade Higher Education Institution (HEI) Operating System uniting 5 mission-critical subsystems under unified governance:
* **Phase 1: Public Website & Enterprise CMS** – Dynamic headless institutional showcase, 21 public modules, admission leads, program discovery, and media CDN.
* **Phase 2: Enterprise ERP** – Student Information System (SIS), Faculty, Staff, Biometrics, Fee Ledgers, Double-Entry Accounts, Payroll, Library, Hostel, Transport, and Approval Workflows.
* **Phase 3: Enterprise Computer-Based Testing (CBT)** – Question Bank, Bloom's Taxonomy, blueprint builder, live anti-cheat exam delivery engine, psychometrics, and instant grading.
* **Phase 4: Enterprise Examination Management System (EMS)** – Timetable scheduling, seating plan generation, QR-verified hall tickets, marks moderation, SGPA/CGPA computation, transcripts, and degree certificates.
* **Phase 5: Enterprise Learning Experience Platform (LMS)** – Course studios, SCORM lessons, HLS video lectures, assignment grading rubrics, peer collaboration forums, live virtual classrooms, and AI learning tutor.
* **Enterprise Feature Control Center (Master Switch)** – Sovereign Root Owner cockpit controlling all 85 platform features, dependency safety graphs, strict User ID + Password authentication, session lifecycle, and immutable audit logging.

---

## 2. Enterprise Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │          Vercel Edge CDN / React 18          │
                    │   Zero Client-Side Storage / Tailwind CSS   │
                    └──────────────────────┬───────────────────────┘
                                           │ HTTPS (Strict TLS 1.3)
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │      FastAPI High-Concurrency REST API       │
                    │       786 Endpoints / Uvicorn Workers        │
                    ├──────────────────────────────────────────────┤
                    │ • Enterprise Feature Control Middleware       │
                    │ • Strict User ID + Password Auth Policy      │
                    │ • Multi-Tier Role-Based Access Control (RBAC)│
                    │ • Immutable Append-Only Audit Logging        │
                    └──────────────┬───────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Neon Serverless  │      │ Redis / Upstash  │      │ Cloudinary / S3  │
│ PostgreSQL 15    │      │ Cache & Queues   │      │ Media & Assets   │
│ 21 Migrations    │      │ Session Registry │      │ Storage Engine   │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## 3. Key Differentiators & Security Standard

1. **Strict User ID + Password Authentication**:
   - Zero tolerance for unverified auth vectors: All OTP, SMS, email login, social sign-in, Google, Microsoft, GitHub, and magic links are permanently removed.
   - Standardized deterministic identifiers: `STU240001` (Students), `FAC240001` (Faculty), `EMP240001` (Staff), `ADM000001` (Administrators), `ROOT000001` (Root Owner).
2. **Administrator-Only Password Reset Desk**:
   - Zero self-service password recovery: Public "Forgot Password" links are removed from login interfaces.
   - Temporary password assignment requires verified physical/biometric identity and enforces mandatory password change upon initial login.
3. **Zero Client-Side Storage (`Zero-Storage`)**:
   - Strictly 0 occurrences of `localStorage`, `sessionStorage`, or `indexedDB` in client code.
   - Authentication tokens rotate in memory with HttpOnly, Secure, SameSite=Strict cookies.
4. **Master Switch Feature Control**:
   - 85 platform features dynamically toggled across Enable, Disable, Hide, Maintenance, and Read-Only without code redeployment.
   - Dependency protection prevents disabling prerequisites that would break downstream workflows.
5. **Verified Scale**:
   - 786 production-tested REST endpoints across 20 functional domains.
   - Zero duplicate route definitions, zero unhandled exceptions, and complete database normalization.

---

## 4. Repository Structure

```
my-education-india/
├── backend/
│   ├── alembic/                # Database migrations (0001 to 0021)
│   ├── app/
│   │   ├── api/v1/             # Central router (786 endpoints)
│   │   ├── auth/               # Argon2id crypto & session security
│   │   ├── core/               # App configuration & exceptions
│   │   ├── db/                 # AsyncPG & SQLAlchemy engine
│   │   ├── models/             # Core database entity models
│   │   ├── modules/            # Domain sub-systems (ERP, CBT, EMS, LMS, Feature Control)
│   │   └── schemas/            # Pydantic v2 validation contracts
│   ├── pyproject.toml          # Poetry package definitions
│   └── Dockerfile              # Multi-stage production container
├── frontend/
│   ├── src/
│   │   ├── components/         # Shared UI components
│   │   ├── modules/            # Subsystem studios & portals
│   │   ├── pages/              # Routed pages (Login, Dashboard)
│   │   └── routes/             # AppRoutes single source of truth
│   ├── package.json            # React 18, Vite, Tailwind CSS
│   └── Dockerfile              # Nginx multi-stage container
├── docs/                       # Comprehensive documentation suite
├── deploy/                     # Docker & orchestration templates
├── scripts/                    # Validation & packaging utilities
├── vercel.json                 # Vercel deployment spec
├── render.yaml                 # Render backend spec
└── docker-compose.prod.yml     # Local/self-hosted orchestrator
```

---

## 5. Quick Verification Commands

```bash
# 1. Verify backend compilation
python3 -m compileall backend scripts

# 2. Check registered routes (786 endpoints)
python3 -c "import sys; sys.path.insert(0, 'backend'); from app.api.v1.router import api_v1_router; print('Routes:', len(api_v1_router.routes))"

# 3. Verify zero client storage in frontend
grep -rnE "(localStorage|sessionStorage|indexedDB)" frontend/src/
```

---

## 6. Deployment Targets

* **Frontend**: Vercel (`vercel.json`)
* **Backend API**: Render (`render.yaml`)
* **Database**: Neon Serverless PostgreSQL (`DATABASE_URL`)
* **Media Assets**: Cloudinary (`CLOUDINARY_*`)

---
*Autonomous Campus Engineering Team • MY EDUCATION INDIA • Indore, Madhya Pradesh*
