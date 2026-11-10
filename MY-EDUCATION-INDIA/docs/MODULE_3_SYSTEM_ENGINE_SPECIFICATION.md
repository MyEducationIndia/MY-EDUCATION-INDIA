# MY EDUCATION INDIA ERP V2
# MODULE 3: CORE SYSTEM ENGINE SPECIFICATION

## 1. Architectural Scope & Objectives

Module 3 delivers the **Core System Engine** for **MY EDUCATION INDIA ERP V2**, establishing the multi-tiered configuration, institutional hierarchy, and sequence numbering backbone for every downstream academic, financial, CBT, and operational module:
- **Multi-Institute & Multi-Branch Hierarchy**: A single ERP deployment supports multiple independent institutes (`Institute`) and regional campuses (`Branch`). Every future operational record links directly to this hierarchy.
- **Universal Number Generator Service**: Dynamic, token-based identifier formatting (`{PREFIX}-{BRANCH}-{COURSE}-{DEPT}-{YEAR}-{NUMBER}-{SUFFIX}`) with configurable reset rules (`YEARLY`, `ACADEMIC_YEAR`, `FINANCIAL_YEAR`, `MONTHLY`, `BRANCH`, `NEVER`), custom padding length, and atomic PostgreSQL sequence increments using row-level locking (`SELECT ... FOR UPDATE`).
- **Dynamic Configuration Engine**: 22 system categories (`general`, `institute`, `authentication`, `communication`, `website`, `appearance`, `security`, `backup`, `academic`, `financial`, `examination`, `certificates`, `attendance`, `fees`, `admissions`, `library`, `hostel`, `transport`, `inventory`, `lms`, `api`, `developer`) stored in PostgreSQL JSONB with zero hardcoded parameters.
- **Academic & Financial Sessions**: Session date boundaries, current active year switching, promotion flags, and GSTIN accounting mapping.
- **Localized Regional Governance**: Indian Rupee (INR ₹), Indian Standard Time (IST Asia/Kolkata +05:30), localized working hours, weekend scheduling, and holiday calendars.

---

## 2. Database Schema (PostgreSQL 16+ via Alembic Migration `0003_module3_core_system_engine.py`)

| Table Name | Entity Class | Architectural Role & Attributes |
| :--- | :--- | :--- |
| `institutes` | `Institute` | Master institutional identity, branding palettes (`primary_color_hex`, `secondary_color_hex`), domain mapping, and legal registration. |
| `branches` | `Branch` | Campus branches with unique `(code, institute_id)` constraints, physical address, working hours (`opening_time`, `closing_time`), and principal details. |
| `academic_years` | `AcademicYear` | Academic session cycles (e.g. `2026-2027`), `start_date`, `end_date`, `is_current`, and audit lock status. |
| `financial_years` | `FinancialYear` | Fiscal cycles (e.g. `FY2026-27`), GSTIN tax mapping, `is_current`, and fiscal books closure flag. |
| `number_generators`| `NumberGenerator` | Configurable templates per `entity_type` (e.g. `student_registration`, `invoice`, `certificate`) with padding, prefix, suffix, and reset policy. |
| `number_sequences` | `NumberSequence` | Running sequence counters locked atomically per `scope_key` (`GLOBAL`, `2027`, `BPL_2027`, etc.) to guarantee gapless progression without race conditions. |
| `currencies` | `Currency` | System currencies (INR ₹, USD $, EUR €) with decimal precision and default flag. |
| `languages` | `Language` | Multi-language localized support with RTL flags (English, Hindi हिन्दी, Tamil, Telugu). |
| `timezones` | `Timezone` | Canonical timezone definitions with minute offsets (Asia/Kolkata +330). |
| `themes` | `Theme` | Visual branding palettes and font definitions. |
| `holidays` | `Holiday` | National, institutional, and branch-level holiday calendars. |
| `working_days` | `WorkingDay` | Per-branch weekly schedule (Monday–Sunday) with active flags and standard shifts. |
| `organization_settings` | `OrganizationSetting` | Regional conventions: fiscal start month (April), academic start month (June), date format (`DD/MM/YYYY`), time format (`12_HOUR`), and sidebar styles. |
| `system_settings` | `SystemSetting` | Dynamic key-value store in PostgreSQL JSONB powering all 22 system categories. |

---

## 3. Backend Implementation (`backend/app/modules/system/`)

```
backend/app/modules/system/
├── __init__.py
├── models.py            # SQLAlchemy 2.x Mapped models for all 14 Core System entities
├── schemas.py           # Pydantic v2 validation models for branches, years, numbering, and settings
├── validators.py        # Token validation ({PREFIX}, {BRANCH}, {YEAR}, {NUMBER}) & date range checks
├── number_generator.py  # UniversalNumberGeneratorService with live preview and atomic sequence progression
├── settings.py          # DynamicSettingsEngine querying and caching PostgreSQL JSONB configurations
├── repository.py        # SystemRepository executing async SQLAlchemy 2.x queries
├── service.py           # CoreSystemService orchestrating multi-branch, fiscal, and numbering operations
└── router.py            # API router for /api/v1/system/ endpoints
```

---

## 4. Frontend Implementation (`frontend/src/modules/system/`)

```
frontend/src/modules/system/
├── types/
│   └── system.types.ts       # TypeScript interfaces for institutes, branches, years, numbering, and settings
├── api/
│   └── systemApi.ts          # Axios API client functions communicating with /api/v1/system/
├── services/
│   └── systemService.ts      # Reactive system service methods
└── pages/
    ├── SettingsDashboardPage.tsx      # Overview configuration hub connecting all system areas
    ├── InstituteManagementPage.tsx    # Multi-campus and franchise entity management
    ├── BranchManagementPage.tsx       # Campus branch provisioning and governance
    ├── AcademicYearPage.tsx           # Academic session creation and active switching
    ├── FinancialYearPage.tsx          # GSTIN-ready fiscal year management
    ├── NumberGeneratorPage.tsx        # Real-time token formatting with live calculation preview
    ├── AuthenticationSettingsPage.tsx # Multi-login criteria, session timeouts, and lockout rules
    ├── AppearanceSettingsPage.tsx     # Color palette selection, theme mode, and typography
    └── GeneralSettingsPage.tsx        # Regional localization (INR ₹, IST +05:30, DD/MM/YYYY)
```

---

## 5. Verification & Automated Test Results

The test suite in `tests/unit/test_module3_backend_system.py`, `tests/unit/test_module2_backend_auth.py`, and `tests/unit/test_module1_architecture_and_schemas.py` verifies:
- 100% clean AST compilation across all backend files.
- Universal Number Generator live preview rendering (`MEI-BPL-2027-000123`, `MEI/IND/CSE/2026/0045/REG`).
- Format template validation enforcing `{NUMBER}` presence and rejecting illegal tokens.
- Academic and financial year chronological date range validation.
- Complete coverage across all 22 system setting categories.
- Zero occurrences of browser `localStorage`, `sessionStorage`, or `indexedDB` in any frontend source file.
- All unit test cases passing (`OK`).
