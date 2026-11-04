# MY EDUCATION INSTITUTE &bull; Production Enterprise Institute Management System

A commercial-grade, multi-portal Institute Management System and Public Website engineered with clean modular architecture.

---

## 🏛️ System Architecture & Technology Stack

- **Backend Framework**: Python 3.11+ / FastAPI (Asynchronous high-performance RESTful API)
- **Database Architecture**: Fully normalized relational schema with foreign key cascades, constraints, and indexes (SQLite for standalone deploy, fully compatible with PostgreSQL / MySQL via SQLAlchemy/aiosqlite)
- **Security Engineering**: Passlib (Bcrypt password hashing), Python-Jose (JWT cryptographic access tokens), strict CORS middleware, HTTP security headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, `Referrer-Policy`), brute force lockout protection (5 failed attempts), and automated audit logging.
- **Frontend SPA**: Responsive Blue & White themed single-page web app with Tailwind CSS, Chart.js analytics, FontAwesome icons, native dark mode, in-page confirmation modals, live countdown inactivity auto-logout (10 minutes), animated marquee announcement ticker, and print-ready ID card / fee invoice / ISO certificate engines.

---

## 🔐 Master User Roles & Default Demonstration Credentials

| Role | Portal Login ID | Default Password | Linked Profile / Notes |
| :--- | :--- | :--- | :--- |
| **Super Administrator** | `admin` | `Admin@1234` | Full root control over all modules, CMS, and credentials |
| **Faculty / Staff** | `staff.sharma` | `Staff@1234` | Prof. Rajesh Sharma &bull; HOD Computer Science (`STF-101`) |
| **Student (DCA)** | `STU-2026-1001` | `2004-05-15` | Rahul Verma &bull; Initial password is DOB (`YYYY-MM-DD` or `DDMMYYYY`) |
| **Student (PGDCA)** | `STU-2026-1002` | `2003-08-22` | Sneha Kulkarni &bull; Extracted from DOB (`2003-08-22`) |
| **Student (TCCP)** | `STU-2026-1003` | `2004-11-10` | Mohammad Zaid &bull; Extracted from DOB (`2004-11-10`) |

*Note: The Super Administrator has full authority in Tab 15 ("User IDs & Passwords") to change Login IDs and override passwords of any user, or reset student passwords back to their recorded Date of Birth.*

---

## 📦 Modular REST API Endpoints (`/api/v1`)

### 1. Authentication & Session (`/api/v1/auth`)
- `POST /api/v1/auth/login`: Authenticates Admin, Staff, or Students (via Roll Number + DOB matching). Returns JWT Bearer token.
- `POST /api/v1/auth/forgot-password`: Dispatches verification OTP code (`849201`).
- `POST /api/v1/auth/reset-password`: Verifies OTP token and updates account password.

### 2. Master User Accounts (`/api/v1/users`)
- `GET /api/v1/users`: List all registered accounts with role filter and search.
- `POST /api/v1/users`: Create user account with role assignment.
- `PUT /api/v1/users/{id}`: Modify full name, Login ID/Roll Number, email, or password.
- `POST /api/v1/users/{id}/reset-dob`: Instantly reset student password to recorded Date of Birth.
- `DELETE /api/v1/users/{id}`: Permanently remove user account.

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
- `POST /api/v1/fees/pay`: Record tuition fee collection and auto-update student dues.
- `GET /api/v1/fees/invoice/{inv_no}`: Retrieve itemized invoice receipt data.

### 9. Attendance Register (`/api/v1/attendance`)
- `POST /api/v1/attendance`: Submit batch daily attendance (Present/Absent/Late).
- `GET /api/v1/attendance/batch/{batch_id}`: Retrieve attendance sheet for specific date.
- `GET /api/v1/attendance/student/{student_id}`: Retrieve student attendance history.

### 10. Study Materials & CMS (`/api/v1/materials`, `/api/v1/notices`, `/api/v1/cms`)
- Full study materials upload and download management.
- Institutional circulars with marquee synchronization and pinning.
- Dynamic CMS config, Testimonials CRUD, FAQs CRUD, Gallery CRUD, Blogs CRUD, and Public Enquiries.

### 11. Reports, Analytics & Backup (`/api/v1/reports`, `/api/v1/settings`)
- `/api/v1/reports/summary`: Overall KPI metrics, total collections, student counts.
- `/api/v1/settings`: Update institute parameters.
- `/api/v1/settings/backup/json`: Download complete relational JSON database snapshot.
- `/api/v1/settings/restore/verify`: Execute automated SQLite integrity check.
- `/api/v1/settings/audit-logs`: Paginated security and activity audit logs.

---

## 🚀 Quick Start & Installation

```bash
# 1. Clone or extract package
unzip my_education_erp_production_suite.zip
cd my_education_erp

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize and seed database
python3 -m app.db.init_db
python3 -m app.db.seed_data

# 5. Run automated test suite
python3 -m tests.test_api_suite

# 6. Launch production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access the application in your web browser:
- Public Website & Management Suite Single Page App: `http://localhost:8000/`
- Interactive OpenAPI Swagger Docs: `http://localhost:8000/docs`
- ReDoc API Specification: `http://localhost:8000/redoc`
- System Healthcheck: `http://localhost:8000/health`
