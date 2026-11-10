# MY EDUCATION INDIA ERP V2
## Module 10: Enterprise Attendance & Leave Management System Architecture & Technical Specification

---

### 1. Executive Summary & System Architecture

The **Enterprise Attendance & Leave Management System (Module 10)** establishes an automated, multi-tiered presence recording and workforce compliance infrastructure for **MY EDUCATION INDIA ERP V2**. It unifies attendance monitoring across three primary institutional populations—**Students**, **Academic Faculty**, and **Administrative/Support Staff**—while managing multi-tier leave approval workflows, optical QR code gate check-ins, biometric time clocks, and statutory UGC/AICTE minimum attendance threshold enforcement.

```
                              ┌────────────────────────────────────────┐
                              │      MY EDUCATION INDIA ERP V2         │
                              │ Module 10: Attendance & Leaves Engine  │
                              └───────────────────┬────────────────────┘
                                                  │
            ┌─────────────────────────────────────┼─────────────────────────────────────┐
            ▼                                     ▼                                     ▼
┌────────────────────────┐             ┌────────────────────────┐            ┌────────────────────────┐
│ Attendance Modalities  │             │ Regulatory Rule Engine │            │ Leave & Duty Workflow  │
├────────────────────────┤             ├────────────────────────┤            ├────────────────────────┤
│ • Classroom Roll Calls │             │ • UGC/AICTE 75% Rule   │            │ • Casual & Medical     │
│ • Period-wise Sessions │             │ • Shortfall Calculator │            │ • Duty & Exam Leave    │
│ • Optical QR Scanner   │             │ • Exam Debarment Lists │            │ • Annual Quota Tracker │
│ • Biometric Clock In   │             │ • Grace Time & Lates   │            │ • Multi-Level Approval │
│ • Staff Shift Manager  │             │ • Lock Day Boundaries  │            │ • Absence Notifications│
└────────────────────────┘             └────────────────────────┘            └────────────────────────┘
```

#### Core Design Principles
1. **Multi-Tenancy & Branch Isolation**: Institutional scoping (`institute_id`, `branch_id`) across all session rosters, biometric clockings, and leave balance accounts.
2. **Statutory UGC/AICTE 75% Rule Engine**: Automated evaluation of semester exam eligibility:
   $$\text{Attendance Percentage} = \frac{\text{Attended Classes}}{\text{Total Conducted Classes}} \times 100$$
   $$\text{Shortfall Classes Required} = \left\lceil \frac{0.75 \times \text{Total} - \text{Attended}}{0.25} \right\rceil$$
3. **High-Speed Contactless QR Gate Scanner**: Leverages existing encrypted QR identity cards from Module 6 (SIMS) with client-side hardware scanner hooks, sub-second logging, and duplicate check-in prevention.
4. **Audit Immutability & Anti-Tamper Locks**: Automated locking of past attendance sessions after a configurable grace period (default 2 days) to prevent retroactive attendance manipulation without Super Admin intervention.
5. **Zero-Trust Client-Side Storage**: In full compliance with enterprise specifications, zero attendance or authentication state is saved in browser `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (Alembic Migration `0010_module10_attendance_leave.py`)

Module 10 provisions 13 relational database tables with enterprise foreign keys, unique constraints, and cascade rules:

| # | Table Name | Description | Key Attributes |
|---|---|---|---|
| 1 | `attendance_sessions` | Classroom and lecture roll call sessions | `id`, `institute_id`, `course_id`, `batch_id`, `section_id`, `subject_id`, `session_date`, `session_type`, `is_locked` |
| 2 | `student_attendance` | Individual student session records | `id`, `session_id`, `student_id`, `status`, `check_in_time`, `attendance_method`, `remarks` (Unique on `[session_id, student_id]`) |
| 3 | `faculty_attendance` | Daily academic faculty clock-in/out logs | `id`, `faculty_user_id`, `institute_id`, `attendance_date`, `clock_in_time`, `clock_out_time`, `total_working_hours`, `status` |
| 4 | `staff_attendance` | Daily administrative staff shift logs | `id`, `staff_user_id`, `institute_id`, `attendance_date`, `clock_in_time`, `clock_out_time`, `total_working_hours`, `status` |
| 5 | `attendance_methods` | Enabled identification modalities | `id`, `institute_id`, `method_code` (MANUAL, QR_CODE, RFID, BIOMETRIC, GEO_FENCE), `is_enabled` |
| 6 | `attendance_rules` | Institutional regulatory compliance policies| `id`, `institute_id`, `minimum_attendance_pct`, `grace_time_minutes`, `lock_attendance_after_days`, `auto_notify_parents_on_absence` |
| 7 | `attendance_logs` | Immutable audit stream from optical/biometric devices | `id`, `user_id`, `user_type`, `log_timestamp`, `log_type` (IN, OUT), `device_id`, `method`, `location_coordinates` |
| 8 | `leave_types` | Master repository of leave categories | `id`, `institute_id`, `code`, `name`, `applicable_to`, `annual_quota_days`, `requires_attachment`, `is_carry_forward` |
| 9 | `leave_requests` | Submitted leave applications | `id`, `institute_id`, `user_id`, `user_type`, `leave_type_id`, `start_date`, `end_date`, `total_days`, `reason`, `status` |
| 10 | `leave_approvals` | HOD and administrative decision trail | `id`, `leave_request_id`, `approver_user_id`, `action` (APPROVED, REJECTED), `comments`, `action_at` |
| 11 | `attendance_reports` | Generated daily/monthly regulatory ledgers | `id`, `institute_id`, `report_type`, `start_date`, `end_date`, `total_records`, `parameters_json` |
| 12 | `attendance_analytics`| Pre-aggregated attendance KPI snapshots | `id`, `institute_id`, `metric_date`, `student_attendance_pct`, `faculty_attendance_pct`, `staff_attendance_pct` |
| 13 | `attendance_notifications`| Absence alert queue for students and parents | `id`, `recipient_user_id`, `recipient_role`, `notification_type`, `title`, `message`, `is_sent` |

---

### 3. Attendance Calculation Engine & Exam Eligibility Verification

The `AttendanceCalculationEngine` executes strict mathematical evaluation:
- **Presence Statuses Counted**: `PRESENT`, `LATE` (within grace window), and `ON_DUTY` (sanctioned extracurricular/sports/NSS representation).
- **Exam Eligibility Shortfall**: For students below 75.0%, the engine computes the exact minimum number of consecutive future classes that must be attended to regain examination eligibility.
- **Deficiency Rosters**: Generates real-time regulatory debarment lists for semester examination controllers.

---

### 4. Leave Workflow Engine & Quota Balancing

The `LeaveWorkflowEngine` governs:
1. **State Machine Validation**:
   - `PENDING` $\to$ `APPROVED`, `REJECTED`, or `CANCELLED`
   - `APPROVED` $\to$ `CANCELLED` (revocation)
   - Disallows re-approving rejected or cancelled requests.
2. **Quota Availability**: Validates that accumulated leave days plus requested days do not exceed the institutional `annual_quota_days` for Casual, Medical, or Earned leave types.
3. **Medical Leave Attachments**: Enforces mandatory medical certificate uploads for leave requests exceeding 2 consecutive days.

---

### 5. Backend REST API Endpoints (`/api/v1/attendance/`)

All endpoints are protected via Bearer JWT tokens and role-based permissions:

- `POST /api/v1/attendance/sessions`: Initialize classroom attendance session with student roster (`attendance.mark`).
- `POST /api/v1/attendance/qr-scan`: Contactless check-in via student identity QR token with duplicate scan prevention (`attendance.mark`).
- `POST /api/v1/attendance/faculty/clock`: Clock in / clock out for academic faculty with working hours tally.
- `GET /api/v1/attendance/leave-types`: List institutional leave categories and quotas.
- `POST /api/v1/attendance/leave-types`: Register new leave category (`leaves.manage`).
- `POST /api/v1/attendance/leaves/apply`: Submit student or employee leave application.
- `POST /api/v1/attendance/leaves/action`: Review, approve, or reject leave with audit comments (`leaves.approve`).
- `GET /api/v1/attendance/reports/daily`: Generate daily presence registers and absentee rosters (`attendance.view`).
- `GET /api/v1/attendance/analytics`: Real-time dashboard KPI summary (`attendance.view`).
- `POST /api/v1/attendance/rules`: Configure statutory minimum percentages, grace periods, and lock days (`attendance.manage`).

---

### 6. Frontend Architecture (React 19 + TypeScript)

The Module 10 frontend resides in `frontend/src/modules/attendance/`:
- **`AttendanceDashboardPage.tsx`**: Executive overview displaying student presence rates, faculty biometric logs, pending leave counters, deficiency alerts, and weekly trend bars.
- **`StudentAttendancePage.tsx`**: Interactive classroom roll call grid with batch/section filtering and quick 'Mark All Present' controls.
- **`QRAttendanceScannerPage.tsx`**: High-speed QR gate scanner interface with simulated hardware hooks and live check-in streams.
- **`FacultyAttendancePage.tsx`**: Academic faculty shift log with biometric clock-in/out timestamps and working hour totals.
- **`StaffAttendancePage.tsx`**: Administrative and support staff shift roster.
- **`LeaveManagementPage.tsx`**: Tabular leave application inbox with one-click approval and rejection workflows.
- **`AttendanceReportsPage.tsx`**: Exportable UGC/AICTE regulatory attendance registers and debarment warnings.
- **`AttendanceSettingsPage.tsx`**: Institutional policy configuration for grace times, lock day boundaries, and minimum threshold percentages.
- **`AdminSidebar.tsx`**: Primary navigation link (`CalendarCheck` icon) pointing to `/admin/attendance`.

---

### 7. Verification & Enterprise Compliance Audit

- **Automated Test Suite**: 43 unit and integration tests passed cleanly across Modules 1 through 10 with 0 errors and 0 failures:
  ```text
  Ran 43 tests in 2.382s
  OK (Total tests run: 43, Errors: 0, Failures: 0)
  ALL ENTERPRISE SUITE TESTS (MODULES 1-10) COMPLETED SUCCESSFULLY!
  ```
- **Zero Browser Storage Audit**: Validated that `localStorage`, `sessionStorage`, and `indexedDB` are nowhere invoked in frontend code.
- **AST Compilation**: 100% of Python backend modules compile cleanly.
