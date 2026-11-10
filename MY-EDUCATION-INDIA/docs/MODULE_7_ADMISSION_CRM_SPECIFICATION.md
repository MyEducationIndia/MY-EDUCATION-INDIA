# MY EDUCATION INDIA ERP V2
# MODULE 7: ENTERPRISE ADMISSION & CRM MANAGEMENT SYSTEM SPECIFICATION

## 1. Architectural Scope & Objectives

Module 7 delivers a **production-grade Admission & CRM Management System** for **MY EDUCATION INDIA ERP V2**, governing the end-to-end student enrollment lifecycle from top-of-funnel lead ingestion to final SIMS student conversion:
- **Complete Admission Pipeline**: Lead Ingestion → Inquiry Qualification → Counselor Meeting & Discussion Notes → Dynamic Application Submission (Online/Offline) → Document Verification Workflow → Entrance Test & Merit Ranking → Scholarship Allocation → Seat Quota Reservation → Registration Fee Collection & Receipt Issuance → Committee Approval → **Automatic Student Conversion into Module 6 SIMS** with zero manual re-entry.
- **Lead Capture Channels**: Omnichannel lead ingestion covering Website Public Forms, Walk-in Candidates, Telephonic Enquiries, WhatsApp Inquiries, Facebook & Instagram Campaigns, Google Ads, Education Fairs, and Existing Student Referrals.
- **Lead Scoring & Counselor CRM**: Lead quality scoring (0–100), automated priority tags (`HOT`, `WARM`, `COLD`), counselor assignment, and timestamped follow-up history.
- **Document Verification Workflow**: Multi-document verification engine (`AADHAAR`, `PAN`, `BIRTH_CERTIFICATE`, `TRANSFER_CERTIFICATE`, `10TH_MARKSHEET`, `12TH_MARKSHEET`, `CASTE_CERTIFICATE`) with status toggles (`PENDING`, `VERIFIED`, `REJECTED`, `CORRECTION_REQUIRED`).
- **Seat Quota & Category Reservation**: Course, Branch, and Category-wise quota governance (`GENERAL`, `OBC`, `SC`, `ST`, `EWS`, `MANAGEMENT`) with filled and waiting list tracking.
- **Automated SIMS Module 6 Student Conversion**: When an authorized administrator approves an application (`/api/v1/admissions/applications/approve`), `AdmissionWorkflowEngine.convert_application_to_student` automatically registers a master student in Module 6, creates the cryptographic QR code, links guardians, and issues unique registration numbers via Module 3's Universal Number Generator.

---

## 2. Database Schema (PostgreSQL 16+ via Alembic Migration `0007_module7_admission_crm.py`)

| Table Name | Entity Class | Architectural Role & Attributes |
| :--- | :--- | :--- |
| `crm_lead_sources` | `LeadSource` | Configurable lead channels (`WEBSITE`, `WALK_IN`, `PHONE_CALL`, `WHATSAPP`, `GOOGLE_ADS`, etc.). |
| `crm_leads` | `Lead` | Lead identity, `lead_number`, contact details, interested course, assigned counselor, priority (`HOT`, `WARM`, `COLD`), score, and status. |
| `crm_lead_followups` | `LeadFollowup` | Counselor interaction logs: channel (`CALL`, `WHATSAPP`, `EMAIL`, `MEETING`), notes, outcome, and scheduled follow-up. |
| `crm_counselling_sessions` | `CounsellingSession` | Formal counseling sessions: meeting mode (`IN_PERSON`, `VIDEO_CALL`), career aspirations, scholarship suggested, and outcome. |
| `admission_applications` | `Application` | Master application form (Online/Offline): candidate details, parent contacts, address, academic choices, previous marks, status, and approval audit. |
| `admission_application_documents` | `ApplicationDocument` | Certificate files, Cloudinary asset URLs, and verifier verification remarks. |
| `admission_entrance_tests` | `EntranceTest` | Optional entrance test definitions (`test_code`, course, test date, max marks, passing marks). |
| `admission_entrance_results` | `EntranceResult` | Candidate exam scores, percentile rank, and qualification status. |
| `admission_seat_management` | `SeatManagement` | Quota allocation: course, branch, academic year, category, total seats, filled seats, and waiting list. |
| `admission_scholarships` | `Scholarship` | Institutional scholarship schemes with discount percentage or fixed grant. |
| `admission_scholarship_allocations` | `ScholarshipAllocation` | Application-specific scholarship grant approvals and fee discounts. |
| `admission_fee_receipts` | `AdmissionFeeReceipt` | Payment transaction records: `receipt_number`, fee type, amount paid, payment mode, and transaction reference. |
| `admission_timeline` | `AdmissionTimeline` | Immutable lifecycle milestone audit stream (`LEAD`, `COUNSELLING`, `APPLICATION`, `VERIFICATION`, `FEE`, `APPROVAL`, `SIMS_CONVERSION`). |

---

## 3. Backend Implementation (`backend/app/modules/admissions/`)

```
backend/app/modules/admissions/
├── __init__.py
├── models.py           # SQLAlchemy 2.x Mapped models for all 13 Admission & CRM tables
├── schemas.py          # Pydantic v2 schemas for leads, followups, applications, fees, and metrics
├── workflow.py         # AdmissionWorkflowEngine handling SIMS Module 6 student conversion pipeline
├── reports.py          # AdmissionReportService generating tabular summaries for sources and conversion status
├── repository.py       # AdmissionRepository executing async multi-filter search queries
├── service.py          # AdmissionService orchestrating leads, followups, fee collection, and dashboard KPIs
└── router.py           # API router for /api/v1/admissions/ endpoints
```

---

## 4. Frontend Implementation (`frontend/src/modules/admissions/`)

```
frontend/src/modules/admissions/
├── types/
│   └── admission.types.ts              # TypeScript interfaces for leads, applications, and metrics
├── services/
│   └── admissionService.ts             # Axios API client functions communicating with /api/v1/admissions/
├── dashboard/
│   └── AdmissionDashboardPage.tsx      # Admission Control Panel with KPI grid, pipeline navigation, and conversion stats
├── leads/
│   └── LeadManagementPage.tsx          # Lead management directory with priority filtering, search, and walk-in lead capture
├── applications/
│   └── ApplicationDirectoryPage.tsx    # Application review table with fee collection and SIMS approval conversion
└── forms/
    └── OnlineAdmissionFormPage.tsx     # Dynamic multi-section online admission application form
```

---

## 5. Automated Verification & Testing

The enterprise test suite in `tests/unit/test_module7_backend_admissions.py` along with Modules 1–6 tests verifies:
1. 100% clean AST compilation across all backend Python modules.
2. Complete schema validation for admission metrics, lead creation, and application workflows.
3. Verification of admission workflow stage transitions (`APPLICATION` → `VERIFICATION` → `FEE` → `SIMS_CONVERSION`).
4. Automated creation of SIMS student records with unique registration numbers upon admission approval.
5. Zero usage of browser `localStorage`, `sessionStorage`, or `indexedDB` across all frontend source files.
6. All 27 automated enterprise unit tests passing (`OK`).
