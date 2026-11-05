# MY EDUCATION INSTITUTE &bull; Production Enterprise Institute Management System (PostgreSQL Edition)

A commercial-grade, multi-portal Institute Management System and Public Website engineered with clean modular architecture, 100% server-side persistence in Render PostgreSQL, SQLAlchemy 2.x ORM, and Alembic migrations.

---

## 🏛️ System Architecture & Technology Stack

- **Backend Framework**: Python 3.11+ / FastAPI (Asynchronous high-performance RESTful API)
- **Database Architecture**: 100% PostgreSQL with SQLAlchemy 2.x ORM, Alembic migrations, connection pooling (`pool_size=20`, `max_overflow=10`, `pool_pre_ping=True`), foreign key cascades, constraints, and indexes. Zero browser storage (localStorage, sessionStorage, IndexedDB, and SQLite completely eliminated).
- **Security Engineering**: Passlib (Bcrypt password hashing), Python-Jose (JWT cryptographic access tokens), strict CORS middleware, HTTP security headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, `Referrer-Policy`), brute force lockout protection (5 failed attempts), and automated audit logging.
- **Frontend SPA**: Responsive Blue & White themed single-page web app with Tailwind CSS, Chart.js analytics, FontAwesome icons, native dark mode, in-page confirmation modals, live countdown inactivity auto-logout (10 minutes), live announcement marquee ticker positioned under header (frozen while scrolling), admin public website section arranging tool, and print-ready ID card / fee invoice / ISO certificate engines.

---

## 🔐 Master User Roles & Default Demonstration Credentials

| Role | Portal Login ID | Default Password | Linked Profile / Notes |
| :--- | :--- | :--- | :--- |
| **Super Administrator** | `admin` | `Admin@1234` | Full root control over all modules, CMS, and credentials |
| **Faculty / Staff** | `staff.sharma` | `Staff@1234` | Prof. Rajesh Sharma &bull; HOD Computer Science (`STF-101`) |
| **Student (DCA)** | `STU-2026-1001` | `2004-05-15` | Rahul Verma &bull; Initial password is DOB (`YYYY-MM-DD` or `DDMMYYYY`) |
| **Student (PGDCA)** | `STU-2026-1002` | `2003-08-22` | Sneha Kulkarni &bull; Extracted from DOB (`2003-08-22`) |
| **Student (TCCP)** | `STU-2026-1003` | `2004-11-10` | Mohammad Zaid &bull; Extracted from DOB (`2004-11-10`) |

---

## 📦 Modular REST API Endpoints (`/api/v1`)

### 1. Authentication & Session (`/api/v1/auth`)
- `POST /api/v1/auth/login`: Authenticates Admin, Staff, or Students (via Roll Number + DOB matching). Returns JWT Bearer token.
- `POST /api/v1/auth/forgot-password`: Dispatches verification OTP code (`849201`).
- `POST /api/v1/auth/reset-password`: Verifies OTP token and updates account password in PostgreSQL.

### 2. Master User Accounts (`/api/v1/users`)
- `GET /api/v1/users`: List all registered accounts with role filter and search.
- `POST /api/v1/users`: Create user account with role assignment.
- `PUT /api/v1/users/{id}`: Modify full name, Login ID/Roll Number, email, or password.
- `POST /api/v1/users/{id}/reset-dob`: Instantly reset student password to recorded Date of Birth.
- `DELETE /api/v1/users/{id}`: Permanently remove user account.
- `GET /api/v1/users/roles`: List all system roles.
- `GET /api/v1/users/permissions`: Get RBAC permission matrix.
- `PUT /api/v1/users/permissions`: Update role permissions.

### 3. Student Management (`/api/v1/students`)
- `GET /api/v1/students`: List enrolled students with search, course, batch, and fee status filters.
- `POST /api/v1/students`: Enroll new student with auto Roll Number and auto user account.
- `GET /api/v1/students/{id}`: Retrieve detailed student profile and fee ledger.
- `PUT /api/v1/students/{id}`: Update student demographic, academic, and fee details.
- `DELETE /api/v1/students/{id}`: Remove student record and linked user account.
- `GET /api/v1/students/export/csv`: Export full student roster as CSV spreadsheet.

### 4. Faculty & Staff Management (`/api/v1/staff`)
- `GET /api/v1/staff`: List faculty members with assigned classroom batches.
- `POST /api/v1/staff`: Add staff member and generate user credentials.
- `PUT /api/v1/staff/{id}`: Update faculty designation, department, and salary fields.
- `DELETE /api/v1/staff/{id}`: Remove faculty record.
- `POST /api/v1/staff/leave/apply`: Submit staff leave request (Casual, Medical, Academic).
- `GET /api/v1/staff/leave`: List staff leave records and approval statuses.

### 5. Course Catalog & Curricula (`/api/v1/courses`)
- `GET /api/v1/courses`: List active academic programs (*T.C.C.P*, *C.C.A*, *D.C.A*, *P.G.D.C.A*, *Basic Computer*, *Data Entry Operator Professional*).
- `POST /api/v1/courses`: Add new course program with duration, fees, and eligibility.
- `PUT /api/v1/courses/{id}`: Update course syllabus parameters.
- `DELETE /api/v1/courses/{id}`: Remove course program.

### 6. Batch Scheduling (`/api/v1/batches`)
- `GET /api/v1/batches`: List batch schedules with assigned trainers, timings, and enrolled counts.
- `POST /api/v1/batches`: Schedule new classroom or laboratory batch.
- `PUT /api/v1/batches/{id}`: Update batch room or timing.
- `DELETE /api/v1/batches/{id}`: Remove batch schedule.

### 7. Admissions Queue (`/api/v1/admissions`)
- `GET /api/v1/admissions`: List online admission applications.
- `POST /api/v1/admissions/apply`: Submit public admission application.
- `POST /api/v1/admissions/{id}/approve`: Approve application and auto-enroll student with credentials.
- `POST /api/v1/admissions/{id}/reject`: Mark application as rejected.
- `DELETE /api/v1/admissions/{id}`: Delete application record.

### 8. Fees & Tax Invoices (`/api/v1/fees`)
- `GET /api/v1/fees`: List payment transactions and tax invoices.
- `POST /api/v1/fees/pay`: Record tuition fee collection and auto-update student dues in PostgreSQL.
- `GET /api/v1/fees/invoice/{inv_no}`: Retrieve itemized invoice receipt data.
- `PUT /api/v1/fees/{id}`: Update fee payment record.
- `DELETE /api/v1/fees/{id}`: Delete fee payment record and adjust student balance.

### 9. Attendance Register (`/api/v1/attendance`)
- `POST /api/v1/attendance`: Submit batch daily attendance (Present/Absent/Late).
- `GET /api/v1/attendance/batch/{batch_id}`: Retrieve attendance sheet for specific date.
- `GET /api/v1/attendance/student/{student_id}`: Retrieve student attendance history.

### 10. Study Materials & CMS (`/api/v1/materials`, `/api/v1/notices`, `/api/v1/cms`)
- Study materials upload and download management.
- Institutional circulars with marquee synchronization and pinning.
- Dynamic CMS config, Testimonials CRUD, FAQs CRUD, Gallery CRUD, Blogs CRUD, and Public Enquiries.
- `GET /api/v1/cms/sections`: Retrieve public website sections and their display order.
- `PUT /api/v1/cms/sections`: Reorder and toggle visibility of public website sections.
- `GET /api/v1/cms/custom-sections`: List custom admin-created website sections.
- `POST /api/v1/cms/custom-sections`: Create new promotional banner or announcement section.
- `DELETE /api/v1/cms/custom-sections/{id}`: Remove custom section.
- `GET /api/v1/cms/documents`: List public downloads and documents.
- `POST /api/v1/cms/documents`: Upload public documents.
- `DELETE /api/v1/cms/documents/{id}`: Delete public document.
- `GET /api/v1/cms/advertisements`: List active advertisements and banners.
- `POST /api/v1/cms/advertisements`: Create advertisement campaign.
- `DELETE /api/v1/cms/advertisements/{id}`: Delete advertisement.
- `GET /api/v1/cms/seo`: Retrieve SEO metadata.
- `PUT /api/v1/cms/seo`: Update website SEO parameters.

### 11. Exam Management, Question Bank & CBT (`/api/v1/exams`)
- `GET /api/v1/exams/config`: Get exam window and center configuration.
- `PUT /api/v1/exams/config`: Update examination parameters.
- `GET /api/v1/exams/forms`: List submitted examination forms.
- `POST /api/v1/exams/forms`: Register student for exams and generate admit card.
- `GET /api/v1/exams/questions`: List Question Bank for CBT examination.
- `POST /api/v1/exams/questions`: Add question with multiple choice options.
- `DELETE /api/v1/exams/questions/{id}`: Remove question.
- `GET /api/v1/exams/results`: List CBT examination results.
- `POST /api/v1/exams/results`: Submit and grade CBT examination.

### 12. Real-Time Cloud Synchronization (`/api/v1/sync`)
- `GET /api/v1/sync/state`: Read unified shared institutional state from PostgreSQL.
- `POST /api/v1/sync/state`: Persist full institutional state updates to PostgreSQL.
- `POST /api/v1/sync/reset`: Clear shared state from PostgreSQL.

### 13. Reports, Analytics & Backup (`/api/v1/reports`, `/api/v1/settings`)
- `/api/v1/reports/summary`: Overall KPI metrics, total collections, student counts.
- `/api/v1/settings`: Update institute parameters in PostgreSQL.
- `/api/v1/settings/restore-points`: Save and retrieve server-side restore checkpoints in PostgreSQL.
- `/api/v1/settings/backup/json`: Download complete relational JSON database snapshot.
- `/api/v1/settings/restore`: Restore database from JSON backup snapshot.
- `/api/v1/settings/restore/verify`: Execute automated PostgreSQL database integrity check.
- `/api/v1/settings/audit-logs`: Paginated security and activity audit logs.

---

## 🚀 Quick Start & Installation

```bash
# 1. Unzip production suite
cd my_education_erp

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set Render or Local PostgreSQL DATABASE_URL in .env
cp .env.example .env
nano .env

# 5. Run Alembic migrations and seed initial data
alembic upgrade head
python3 -m app.db.seed_data

# 6. Launch production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access the application in your web browser:
- Public Website & Management Suite Single Page App: `http://localhost:8000/`
- Interactive OpenAPI Swagger Docs: `http://localhost:8000/docs`
