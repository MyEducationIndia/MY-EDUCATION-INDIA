# MY EDUCATION INDIA – Production REST API Documentation

**API Specification:** OpenAPI 3.1.0 / REST  
**Registered Endpoints:** 786 Total Endpoints  
**Base URL:** `/api/v1`  
**Authentication Scheme:** Bearer JWT in `Authorization` Header or HttpOnly Secure Cookie

---

## 1. Authentication & Identity Management (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | Authenticate using User ID + Password | Public |
| `POST` | `/auth/refresh` | Rotate access token using secure refresh cookie | Refresh Token |
| `POST` | `/auth/logout` | Terminate session and invalidate refresh token | Authenticated |
| `GET` | `/auth/me` | Fetch active authenticated user profile & roles | Authenticated |
| `POST` | `/auth/password/change` | Authenticated user password update | Authenticated |
| `GET` | `/auth/sessions` | List active device sessions for current user | Authenticated |
| `DELETE` | `/auth/sessions/{id}` | Terminate specific device session | Authenticated |

---

## 2. Enterprise Feature Control Center (`/api/v1/feature-control`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/feature-control/features` | Catalog of 85 features across 6 categories | Root Owner / Admin |
| `GET` | `/feature-control/features/{key}` | Detailed feature status & restrictions | Root Owner / Admin |
| `PUT` | `/feature-control/features/{key}` | Toggle feature switch (with immutable audit) | Root Owner |
| `GET` | `/feature-control/features/{key}/dependencies` | Dependency graph & safety analysis | Root Owner / Admin |
| `GET` | `/feature-control/audit-logs` | Fetch immutable feature modification logs | Root Owner |
| `GET` | `/feature-control/security/login-policy` | Fetch active login security settings | Root Owner / Admin |
| `PUT` | `/feature-control/security/login-policy` | Update password policy & user ID rules | Root Owner |
| `POST` | `/feature-control/user-id/generate` | Auto-generate standardized User ID | Admin |
| `POST` | `/feature-control/security/admin-password-reset` | Issue verified temporary password | Admin / Root Owner |
| `GET` | `/feature-control/security/session-policy` | Fetch session timeout & idle configs | Root Owner |
| `PUT` | `/feature-control/security/session-policy` | Update session timeout & device limits | Root Owner |
| `GET` | `/feature-control/lockdown` | Fetch global system lockdown state | Root Owner |
| `POST` | `/feature-control/lockdown` | Activate kill switch, emergency mode, banner | Root Owner |

---

## 3. Core ERP Subsystems

* **Admissions & CRM (`/api/v1/admissions`, `/api/v1/crm`):** 42 endpoints covering prospect tracking, eligibility, merit lists, application verification, and counselor allocations.
* **Student Information System (`/api/v1/students`):** 56 endpoints covering student master profiles, parent records, address verification, and enrollment histories.
* **Academics Engine (`/api/v1/academics`):** 64 endpoints covering course catalogs, semesters, sections, syllabi, and credit allocations.
* **Fee & Finance Ledger (`/api/v1/fees`, `/api/v1/finance`):** 48 endpoints covering fee schedules, payment gateway integrations, concessions, and vouchers.
* **Attendance & Biometrics (`/api/v1/attendance`):** 36 endpoints covering daily RFID/Biometric sync, shortage notices, and leave approvals.

---

## 4. Computer-Based Testing (CBT) Subsystem (`/api/v1/cbt`)

* **Question Bank & Approvals:** 28 endpoints covering question creation, Bloom's taxonomy tagging, and double-blind peer review.
* **Exam Blueprint & Builder:** 18 endpoints covering section blueprints, dynamic shuffling, and timing rules.
* **Live Test Engine:** 24 endpoints covering candidate screen delivery, anti-cheat tracking, auto-save pings, and submission.
* **Psychometrics & Results:** 22 endpoints covering instant grading, negative marking, and percentile calculations.

---

## 5. Examination Management System (EMS) (`/api/v1/examinations`)

* **Timetables & Seating Plans:** 32 endpoints covering hall allocation, invigilator rosters, and conflict detection.
* **Hall Tickets:** 16 endpoints covering digitally signed admit cards with QR security codes.
* **Evaluation & Marks Moderation:** 24 endpoints covering faculty marks entry, chief examiner reviews, and grace marks rules.
* **Results & Transcripts:** 26 endpoints covering SGPA/CGPA tabulation, consolidated grade cards, and degree issuance.

---

## 6. Learning Experience Platform (LMS) (`/api/v1/lxp`)

* **Courses & Lessons:** 34 endpoints covering digital curriculum, module prerequisites, and lecture notes.
* **HLS Video Streaming:** 18 endpoints covering adaptive bitrate video streaming and watch-time milestones.
* **Assignments & Quizzes:** 28 endpoints covering submissions, rubric grading, and chapter checkpoints.
* **Virtual Classrooms:** 16 endpoints covering WebRTC/Zoom live lecture links and attendance sync.
* **AI Learning Assistant:** 12 endpoints covering flashcards, summarization, and conceptual tutoring.
