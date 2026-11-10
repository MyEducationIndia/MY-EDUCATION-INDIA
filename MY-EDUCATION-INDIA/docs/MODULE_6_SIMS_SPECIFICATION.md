# MY EDUCATION INDIA ERP V2
# MODULE 6: ENTERPRISE STUDENT INFORMATION MANAGEMENT SYSTEM (SIMS) SPECIFICATION

## 1. Architectural Scope & Objectives

Module 6 delivers the **Enterprise Student Information Management System (SIMS)** for **MY EDUCATION INDIA ERP V2**. SIMS serves as the single source of truth for all student data across admissions, attendance, fees, CBT, examinations, certificates, library, hostel, and transport:
- **Universal Number Generator Integration**: Automated generation of `registration_number` (`{PREFIX}-{BRANCH}-{YEAR}-{NUMBER}`), `enrollment_number`, `roll_number`, and `erp_id` with zero duplicate records.
- **Tab-Based Student Profile**: Tabbed profile interface featuring General & Academic Details, National IDs (Aadhaar, APAAR ID, ABC Account ID), Guardians & Emergency Contacts, Multiple Addresses, Health & Medical Profiles, Identity Documents with verification status, Lifecycle Timeline Milestones, and Notes.
- **Cryptographic QR Code Verification (`StudentQRGenerator`)**: Generation of tamper-evident verification payloads and inline scalable SVG QR codes for student identity cards, library access, and CBT examination check-in.
- **Configurable Custom Fields**: Admin can create custom student fields (`student_custom_fields` and `student_custom_values`) with dynamic rendering across the frontend without code changes.
- **Student Lifecycle & Promotion Engine**: Formal state machine (`ACTIVE`, `INACTIVE`, `PENDING_ADMISSION`, `TRANSFERRED`, `SUSPENDED`, `PASSED`, `DROPPED`, `ALUMNI`, `ARCHIVED`, `DELETED`) with historical audit logs and bulk promotion across academic sessions.
- **Bulk Import/Export Engine**: Bulk CSV parser with row-level validation, sample template download (`/api/v1/students/template/csv`), and error reporting.

---

## 2. Database Schema (PostgreSQL 16+ via Alembic Migration `0006_module6_sims_engine.py`)

| Table Name | Entity Class | Architectural Role & Attributes |
| :--- | :--- | :--- |
| `students` | `Student` | Master student record: `registration_number`, `enrollment_number`, `roll_number`, `erp_id`, `first_name`, `last_name`, `email`, `phone_number`, `date_of_birth`, `gender`, `course_name`, `batch_name`, `academic_year_code`, `semester_or_year`, `status`, `is_deleted`. |
| `student_profiles` | `StudentProfile` | Extended profile: `aadhaar_number`, `pan_number`, `apaar_id`, `abc_account_id`, `religion`, `caste_category`, `nationality`, `previous_school`, `previous_marks_percentage`. |
| `student_addresses` | `StudentAddress` | Address records: `address_type` (`PERMANENT`, `CORRESPONDENCE`, `LOCAL_GUARDIAN`), street, city, district, state, postal code, and country. |
| `student_guardians` | `StudentGuardian` | Family & emergency contacts: `relationship_type` (`FATHER`, `MOTHER`, `LEGAL_GUARDIAN`), full name, mobile, email, occupation, and `is_emergency_contact`. |
| `student_documents` | `StudentDocument` | Document repository (`AADHAAR`, `PAN`, `BIRTH_CERTIFICATE`, `TRANSFER_CERTIFICATE`, `10TH_MARKSHEET`, `12TH_MARKSHEET`, `CASTE_CERTIFICATE`, `PASSPORT`), Cloudinary file URL, and verification tracking. |
| `student_medical` | `StudentMedical` | Health records: `blood_group`, height, weight, allergies, medical conditions, emergency doctor name and phone, insurance policy number. |
| `student_custom_fields` | `StudentCustomField` | Admin-configured dynamic student fields (`field_key`, `field_label`, `field_type`, `is_required`, `options_list`). |
| `student_custom_values` | `StudentCustomValue` | Values associated with custom fields per student. |
| `student_status_history`| `StudentStatusHistory` | Transition audit trail tracking `previous_status`, `new_status`, `reason`, actor, and timestamp. |
| `student_timeline` | `StudentTimeline` | Immutable chronological stream of milestones (`ADMISSION`, `ACADEMIC`, `FEE`, `ATTENDANCE`, `EXAM`, `CERTIFICATE`, `TRANSFER`, `STATUS_CHANGE`). |
| `student_notes` | `StudentNote` | Confidential and administrative counseling remarks. |
| `student_photos` | `StudentPhoto` | Student portrait and digital signature asset URLs. |
| `student_qr_codes` | `StudentQRCode` | Cryptographically signed verification payload and rendered SVG string. |

---

## 3. Backend Implementation (`backend/app/modules/students/`)

```
backend/app/modules/students/
├── __init__.py
├── models.py           # SQLAlchemy 2.x Mapped models for all 13 SIMS tables
├── schemas.py          # Pydantic v2 schemas for registration, updates, search, and profiles
├── validators.py       # Domain validators for Aadhaar, PAN, phone, and PIN codes
├── qr_generator.py     # StudentQRGenerator producing cryptographic verification payloads and SVG QR codes
├── timeline.py         # StudentTimelineService logging lifecycle events
├── import_export.py    # StudentImportExportProcessor handling bulk CSV parsing and template generation
├── repository.py       # StudentRepository with multi-parameter filter search
├── service.py          # StudentManagementService orchestrating numbering, registration, promotion, and bulk actions
└── router.py           # API router for /api/v1/students/ endpoints
```

---

## 4. Frontend Implementation (`frontend/src/modules/students/`)

```
frontend/src/modules/students/
├── types/
│   └── student.types.ts                # TypeScript interfaces for students, profiles, addresses, guardians, documents
├── api/
│   └── studentApi.ts                   # Axios API functions communicating with /api/v1/students/
├── services/
│   └── studentService.ts               # Reactive student service wrapper
├── components/
│   └── StudentQRCodeModal.tsx          # Digital ID card modal with embedded verified QR code and printable layout
├── profile/
│   └── StudentTabbedProfileModal.tsx   # Tabbed profile modal (General, Academic, Guardians, Addresses, Medical, Documents, Timeline)
└── pages/
    └── StudentDirectoryPage.tsx        # Search, multi-criteria filters, bulk delete, promotion, and CSV template download
```

---

## 5. Automated Verification & Testing

The enterprise test suite in `tests/unit/test_module6_backend_sims.py` along with Modules 1–5 tests verifies:
1. 100% clean AST compilation across all backend Python modules.
2. QR code generation, signed verification payload format (`MEI_VERIFY:...`), and valid SVG element construction.
3. CSV import parser row-level validation, header verification, and template generation.
4. Universal Number Generator integration ensuring unique registration numbers per student.
5. Zero usage of browser `localStorage`, `sessionStorage`, or `indexedDB` in any frontend source file.
6. All 25 automated enterprise unit tests passing (`OK`).
