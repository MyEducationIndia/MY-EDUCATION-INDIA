# MY EDUCATION INDIA ERP V2 — MODULE 14 SPECIFICATION
## ENTERPRISE LIBRARY & DIGITAL KNOWLEDGE MANAGEMENT SYSTEM

### 1. Executive Summary & Architectural Overview
Module 14 delivers an enterprise-grade, integrated Library & Digital Knowledge Management System for MY EDUCATION INDIA ERP V2. It unifies physical cataloging and circulation operations with a cloud-native digital knowledge repository supporting eBooks, open-access research papers, faculty lecture notes, and past examination question papers.

Designed strictly without mock implementations or client-side storage, Module 14 integrates seamlessly with:
- **Module 1 & 2 (Architecture & Auth)**: Multi-tenant tenant isolation (`institute_id`), fine-grained RBAC roles (`LIBRARIAN`, `ASSISTANT_LIBRARIAN`, `STUDENT_MEMBER`, `FACULTY_MEMBER`).
- **Module 6 (SIMS)** & **Module 8 (Academics)**: Automatic library membership synchronization on student admission and academic batch assignment.
- **Module 9 (Fee & Finance)**: Automatic posting of uncollected overdue fines, lost book compensation fees, and digital access fees to the student financial ledger.
- **Module 11 & 12 (Examinations & CBT)**: Question paper archiving and syllabus-aligned digital study notes.
- **Module 13 (Certificates & Verification)**: Library No Dues Certificate generation and digital clearance verification for degree issuance.

---

### 2. Database Architecture (18 Enterprise Tables)
Module 14 provisions 18 relational tables via Alembic revision `0014_lib_knowledge`:
1. `library_categories`: Hierarchical Dewey Decimal / subject classification taxonomy.
2. `library_authors`: Author bio, nationality, credentials, and bibliography references.
3. `library_publishers`: Publisher addresses, vendor agreements, and contact profiles.
4. `library_locations`: Physical rack, shelf, floor, aisle, and room coordinates.
5. `library_books`: Master catalog titles, ISBN-10/13, editions, Dewey classification.
6. `library_book_copies`: Individual physical copy accession register with unique barcodes (`ACC-XXXX-XXXXXX`) and RFID tag identifiers.
7. `library_members`: Borrowing allowances, issue duration limits, active issue tallies, and fine balance ledgers.
8. `library_issue_transactions`: Issue date, dynamic loan duration, renewal extensions, and due dates.
9. `library_return_transactions`: Return date timestamps, condition ratings, and overdue fine calculations.
10. `library_reservations`: Hold queue, reservation rank, expiration timestamps, and availability alerts.
11. `library_fines`: Overdue penalties, damage assessments, waiver audits, and payment receipts.
12. `library_digital_resources`: eBooks, research papers, thesis publications with view/download telemetry.
13. `library_question_papers`: Past university & institutional exam papers indexed by program, semester, and year.
14. `library_notes`: Faculty lecture notes, syllabus topic outlines, and course guides.
15. `library_reading_histories`: Member borrow and digital access telemetry.
16. `library_notifications`: Automated SMS/Email alerts for loan due dates, overdue notices, and hold availability.
17. `library_reports`: Saved audit snapshots and accession registers.
18. `library_analytics`: Daily circulation volumes, return rates, fine accruals, and digital downloads.

---

### 3. Circulation & Overdue Fine Calculation Engine
- **Circulation Rules**:
  - Loan Period: Default 14 days (configurable per member type: Faculty = 30 days, Students = 14 days).
  - Maximum Renewals: 2 extensions before mandatory physical inventory check.
- **Fine Formula**:
  - $OverdueDays = ReturnDate - DueDate$
  - If $OverdueDays \le GracePeriod$ (default 1 day), $BillableDays = 0$.
  - If $OverdueDays > GracePeriod$, $BillableDays = OverdueDays - GracePeriod$.
  - $FineAmount = \min(BillableDays 	imes DailyRate, MaxCap)$ where $DailyRate = 	ext{INR } 5.00/	ext{day}$ and $MaxCap = 	ext{INR } 500.00$.

---

### 4. Public OPAC & Barcode Integration
- **Online Public Access Catalog (OPAC)**: Accessible at `/library/opac` with zero login requirement for institutional catalog search by title, author, subject, or ISBN.
- **Barcode & QR Generators**:
  - Accession Barcode: `ACC-{INSTITUTE_HASH}-{SEQUENCE:06d}`.
  - Book Copy QR: JSON-encoded payload with accession identifier, title, ISBN, and item type.

---

### 5. Frontend & Navigation Layout
- **Path**: `frontend/src/modules/library/`
- **11 Dedicated Submodules**:
  - `/admin/library`: Master Library Dashboard with real-time telemetry KPI cards.
  - `/admin/library/catalog`: Book Master Catalog with search & classification.
  - `/admin/library/copies`: Accession Register & Physical Copy Tracking.
  - `/admin/library/members`: Member Borrowing Directory & Privileges.
  - `/admin/library/circulation`: High-speed Barcode Issue/Return Terminal.
  - `/admin/library/reservations`: Hold Waitlist & Priority Queue.
  - `/admin/library/digital`: Digital Knowledge Repository (eBooks, Papers, Notes).
  - `/admin/library/reports`: Circulation, Overdue, and Accession Audit Reports.
  - `/admin/library/analytics`: Utilization Rates, Peak Hour Telemetry, and Leaderboards.
  - `/admin/library/settings`: Circulation Policies, Fine Rates, and RFID Gates.
  - `/library/opac`: Unauthenticated Public Catalog Search.
- **Strict Compliance**: Zero usage of `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 6. Verification & Test Suite
- Comprehensive test suite `tests/unit/test_module14_backend_library.py` validates:
  - Clean AST compilation across all 13 backend Python source files.
  - Schema serialization for books, categories, members, and transactions.
  - ISBN-10 and ISBN-13 format validation algorithms.
  - Circulation Engine due dates and renewal thresholds.
  - Library Fine Engine with on-time, grace period, overdue, and maximum cap cases.
  - Barcode and QR payload generators.
  - Zero browser storage audit across frontend sources.
