# MY EDUCATION INDIA ERP V2
## Module 8: Enterprise Academic Management System Architecture & Technical Specification

---

### 1. Executive Summary & System Architecture

The **Enterprise Academic Management System (Module 8)** provides the core educational and academic backbone of the **MY EDUCATION INDIA ERP V2** platform. It establishes the organizational and pedagogical structure upon which all dependent enterprise subsystems—such as **Student Information Management (SIMS, Module 6)**, **Admission & CRM Pipeline (Module 7)**, Fees & Billing, Examination & Evaluation, Attendance, and Learning Management Systems (LMS)—are grounded.

```
                              ┌───────────────────────────────────────┐
                              │     MY EDUCATION INDIA ERP V2         │
                              │ Module 8: Academic Management Engine  │
                              └──────────────────┬────────────────────┘
                                                 │
            ┌────────────────────────────────────┼────────────────────────────────────┐
            ▼                                    ▼                                    ▼
┌───────────────────────┐            ┌───────────────────────┐            ┌───────────────────────┐
│ Academic Architecture │            │ Operational Structure │            │ Pedagogical Engine    │
├───────────────────────┤            ├───────────────────────┤            ├───────────────────────┤
│ • Departments         │            │ • Batches             │            │ • CBCS / NEP Builder  │
│ • Programs (UG/PG/Dip)│            │ • Sections            │            │ • Credit Rules        │
│ • Courses & Specs     │            │ • Classrooms          │            │ • Grading Scale (10pt)│
│ • Semesters & Years   │            │ • Faculty Allocations │            │ • Calendar Events     │
│ • Master Subjects     │            │ • Timetable Engine    │            │ • Prerequisite Rules  │
└───────────────────────┘            └───────────────────────┘            └───────────────────────┘
```

#### Core Design Principles
1. **Multi-Tenancy & Institutional Hierarchy**: Complete multi-institute and multi-branch isolation. Every department, course, batch, and timetable slot is explicitly tied to an `institute_id` and optional `branch_id`.
2. **CBCS & NEP Compliance**: Native support for the Choice Based Credit System (CBCS) and the National Education Policy (NEP) curriculum structures, including Major, Minor, Open Elective, Skill Enhancement, and Ability Enhancement credit baskets.
3. **Automated Conflict Detection**: The `TimetableConflictEngine` performs mathematical window overlap validation to prevent double-booking of physical classroom resources and academic faculty across all lecture, lab, and tutorial slots.
4. **Zero-Trust Security & Storage Compliance**: Strictly zero browser `localStorage`, `sessionStorage`, or `indexedDB` data storage. All state is maintained through React Context, memory cache, and secure HTTP-only cookie sessions.

---

### 2. Database Schema (Alembic Migration `0008_module8_academic_engine.py`)

Module 8 provisions 16 relational database tables configured with enterprise foreign keys, cascade safety rules, and composite search indexes:

| # | Table Name | Description | Key Attributes |
|---|---|---|---|
| 1 | `acad_departments` | Academic faculties and departments | `id`, `code`, `name`, `hod_user_id`, `institute_id`, `branch_id`, `is_active` |
| 2 | `acad_programs` | Degree levels (UG, PG, PhD, Diploma) | `id`, `code`, `name`, `level`, `duration_years`, `institute_id` |
| 3 | `acad_courses` | Degree courses (e.g. B.Tech, MBA, MBBS) | `id`, `code`, `name`, `academic_pattern`, `total_semesters_or_years`, `department_id`, `program_id` |
| 4 | `acad_specializations` | Course branches and honors disciplines | `id`, `course_id`, `code`, `name`, `is_active` |
| 5 | `acad_semesters` | Academic terms and semesters | `id`, `course_id`, `semester_number`, `name`, `term_type` |
| 6 | `acad_subjects` | Master repository of academic subjects | `id`, `code`, `name`, `subject_type`, `credits`, `lecture_hours`, `lab_hours`, `tutorial_hours` |
| 7 | `acad_curriculums` | Curriculum frameworks per course/year | `id`, `course_id`, `academic_year_id`, `code`, `title`, `total_credits_required`, `status` |
| 8 | `acad_curriculum_subjects` | Subjects mapped into curriculums | `id`, `curriculum_id`, `semester_id`, `subject_id`, `course_type`, `is_elective` |
| 9 | `acad_batches` | Student cohorts (e.g., 2026-2030) | `id`, `course_id`, `academic_year_code`, `code`, `name`, `start_date`, `end_date`, `intake_capacity` |
| 10 | `acad_sections` | Divisible sections per batch (A, B, C) | `id`, `batch_id`, `name`, `capacity`, `classroom_number`, `class_teacher_name` |
| 11 | `acad_classrooms` | Physical/virtual infrastructure | `id`, `room_number`, `building`, `floor`, `capacity`, `room_type`, `is_smart_room` |
| 12 | `acad_faculty_assignments`| Teaching allocations | `id`, `faculty_user_id`, `subject_id`, `section_id`, `academic_year_code`, `is_primary` |
| 13 | `acad_timetables` | Master timetable schedules | `id`, `academic_year_code`, `course_id`, `batch_id`, `section_id`, `effective_from`, `is_active` |
| 14 | `acad_timetable_slots` | Individual periods/time allocations | `id`, `timetable_id`, `subject_id`, `faculty_user_id`, `classroom_id`, `day_of_week`, `start_time`, `end_time` |
| 15 | `acad_calendar_events` | Academic calendar events & milestones | `id`, `title`, `event_type`, `start_date`, `end_date`, `is_holiday`, `institute_id` |
| 16 | `acad_grading_systems` | Institutional grade points & scales | `id`, `name`, `scale_type`, `grade_point`, `letter_grade`, `min_percentage`, `max_percentage` |

---

### 3. Automated Timetable Conflict & Collision Engine

The `TimetableConflictEngine` runs during every slot creation and edit operation to prevent scheduling overlaps.

#### Overlap Algorithm
Two time intervals $[S_1, E_1)$ and $[S_2, E_2)$ collide if and only if:
$$\text{Collision} \iff (S_1 < E_2) \land (E_1 > S_2)$$

#### Verification Matrix
```python
stmt = select(TimetableSlot).where(
    TimetableSlot.day_of_week == day_of_week,
    TimetableSlot.start_time < end_time,
    TimetableSlot.end_time > start_time,
)
if faculty_user_id:
    # Ensures faculty cannot be in two classrooms at the same time
if classroom_id:
    # Ensures physical classroom cannot host two sections simultaneously
```

Whenever a conflict is detected, the engine raises an HTTP 409 `ConflictException` with exact resource and slot diagnostic details.

---

### 4. CBCS (Choice Based Credit System) & NEP Curriculum Architecture

Module 8 implements the UGC Choice Based Credit System (CBCS) aligned with the National Education Policy (NEP):

1. **Course Classifications**:
   - `CORE`: Mandatory foundational subjects.
   - `DISCIPLINE_ELECTIVE`: Specialized branch electives.
   - `GENERIC_ELECTIVE`: Interdisciplinary cross-departmental electives.
   - `SKILL_ENHANCEMENT (SEC)`: Practical, hands-on skill development courses.
   - `ABILITY_ENHANCEMENT (AEC)`: Environmental science, communication, and languages.
2. **Contact Hours and Credit Calculation**:
   - 1 Lecture Hour (L) / week = 1 Credit
   - 1 Tutorial Hour (T) / week = 1 Credit
   - 2 Laboratory Hours (P) / week = 1 Credit
3. **10-Point UGC Grading Scale**:
   - `O` (Outstanding): Grade Point 10.0 (90% - 100%)
   - `A+` (Excellent): Grade Point 9.0 (80% - 89.9%)
   - `A` (Very Good): Grade Point 8.0 (70% - 79.9%)
   - `B+` (Good): Grade Point 7.0 (60% - 69.9%)
   - `B` (Above Average): Grade Point 6.0 (55% - 59.9%)
   - `C` (Average): Grade Point 5.0 (50% - 54.9%)
   - `P` (Pass): Grade Point 4.0 (40% - 49.9%)
   - `F` (Fail): Grade Point 0.0 (< 40%)

---

### 5. Backend REST API Endpoints (`/api/v1/academics/`)

All endpoints are protected via Bearer JWT tokens and role-based permissions:

- `GET /api/v1/academics/departments`: List institutional academic departments.
- `POST /api/v1/academics/departments`: Provision new department with HOD assignment.
- `GET /api/v1/academics/programs`: List degree levels (UG, PG, Diploma, Doctorate).
- `POST /api/v1/academics/programs`: Provision academic degree program.
- `GET /api/v1/academics/courses`: Filter courses by department or degree level.
- `POST /api/v1/academics/courses`: Register course with semester/yearly structure and credits.
- `GET /api/v1/academics/subjects`: Retrieve catalog of subjects with L-T-P-C breakdowns.
- `POST /api/v1/academics/subjects`: Register new subject into master curriculum bank.
- `GET /api/v1/academics/batches`: Query active cohorts and section allotments.
- `POST /api/v1/academics/batches`: Initialize new batch with auto-provisioned default section.
- `POST /api/v1/academics/sections`: Create additional sections within batch cohorts.
- `GET /api/v1/academics/timetable`: Fetch weekly timetable grid for batch, section, or faculty.
- `POST /api/v1/academics/timetable/slots`: Allocate schedule slot with conflict engine validation.

---

### 6. Frontend Architecture (React 19 + TypeScript)

The Module 8 frontend resides in `frontend/src/modules/academics/` and features:
- **`AcademicDashboardPage.tsx`**: Executive overview displaying metrics for departments, courses, batches, and active subjects, with quick-action launchpads.
- **`DepartmentsPage.tsx`**: Department registry with real-time modal creation and HOD assignment.
- **`CoursesDirectoryPage.tsx`**: Course catalog displaying duration, degree type, and intake capacity.
- **`BatchesSectionsPage.tsx`**: Cohort tracking displaying batch strength, intake caps, and section distribution.
- **`InteractiveTimetablePage.tsx`**: Monday through Saturday multi-period interactive timetable grid with collision alerts.
- **`AdminSidebar.tsx`**: Dedicated navigation entry (`BookOpen` icon) pointing to `/admin/academics`.

---

### 7. Verification & Enterprise Compliance Audit

The automated test suite (`tests/unit/`) validates the integrity of all 8 implemented modules:
- **31 test cases passed cleanly** across Modules 1 through 8.
- **Zero Browser Storage Audit**: Validated that `localStorage`, `sessionStorage`, and `indexedDB` are nowhere invoked in frontend source code.
- **AST Compilation**: 100% of Python backend modules compile cleanly without syntax errors.
- **Strict PostgreSQL Engine**: Validated all database queries use asynchronous SQLAlchemy 2.x standards.
