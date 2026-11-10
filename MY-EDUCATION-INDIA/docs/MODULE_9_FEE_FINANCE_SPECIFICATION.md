# MY EDUCATION INDIA ERP V2
## Module 9: Enterprise Fee & Finance Management System Architecture & Technical Specification

---

### 1. Executive Summary & System Architecture

The **Enterprise Fee & Finance Management System (Module 9)** serves as the financial engine and revenue ledger of the **MY EDUCATION INDIA ERP V2** ecosystem. It governs the end-to-end institutional financial lifecycle: from multi-tiered fee structure creation and installment scheduling to counter payment collection, universal receipt generation, scholarships, concessions, automated late fee penalties, audited refund disbursements, and multi-dimensional regulatory financial reporting.

```
                              ┌────────────────────────────────────────┐
                              │      MY EDUCATION INDIA ERP V2         │
                              │ Module 9: Fee & Finance Engine         │
                              └───────────────────┬────────────────────┘
                                                  │
            ┌─────────────────────────────────────┼─────────────────────────────────────┐
            ▼                                     ▼                                     ▼
┌────────────────────────┐             ┌────────────────────────┐            ┌────────────────────────┐
│ Fee Structuring & Plan │             │ Transaction Processing │            │ Concessions & Audit    │
├────────────────────────┤             ├────────────────────────┤            ├────────────────────────┤
│ • Unlimited Categories │             │ • Counter & Gateways   │            │ • Merit Scholarships   │
│ • Custom Fee Heads     │             │ • Multi-Mode Payments  │            │ • Sibling / Staff Disc │
│ • Multi-Term Structures│             │ • Universal Receipts   │            │ • Grace / Late Fees    │
│ • Installment Engine   │             │ • Indian Number Words  │            │ • Audited Refunds      │
│ • Automatic Assignment │             │ • QR / Barcode Hashes  │            │ • Daily / Monthly Reps │
└────────────────────────┘             └────────────────────────┘            └────────────────────────┘
```

#### Core Design Principles
1. **Multi-Institute & Multi-Branch Segregation**: Every fee category, structure, transaction, and receipt is scoped with an `institute_id` and optional `branch_id`, ensuring strict accounting isolation.
2. **Universal Receipt Generator**: Automatically issues sequentially unique receipt numbers (`REC-MEI-YYYYMMDD-XXXX`), renders payment totals in official Indian Currency words (Crores, Lakhs, Thousands, Hundreds), generates verification QR code JSON payloads, and signs receipts with cryptographic HMAC SHA-256 digital signature hashes.
3. **Double-Entry Balance Accounting**: Student fee assignments maintain strict integrity:
   $$\text{Total Payable} = \text{Total Fee} - (\text{Total Scholarships} + \text{Total Discounts})$$
   $$\text{Total Remaining Due} = \text{Total Payable} - \text{Total Paid}$$
4. **Permanent Transaction Ledger (No Hard Deletes)**: Financial transaction records, receipt sequences, and refund logs are permanently preserved with audit trails and user stamps.
5. **Zero-Trust Client-Side Storage**: In full compliance with enterprise specifications, zero financial or authentication data is stored in browser `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (Alembic Migration `0009_module9_fee_finance.py`)

Module 9 provisions 16 relational database tables configured with enterprise foreign keys, cascade rules, and composite indexes:

| # | Table Name | Description | Key Attributes |
|---|---|---|---|
| 1 | `fee_categories` | Institutional fee classifications | `id`, `code`, `name`, `description`, `institute_id`, `branch_id`, `is_active` |
| 2 | `fee_heads` | Specific accounting fee line items | `id`, `category_id`, `code`, `name`, `is_refundable`, `default_amount`, `institute_id` |
| 3 | `late_fee_rules` | Grace period and overdue penalty rules | `id`, `institute_id`, `code`, `name`, `calculation_type`, `rate`, `maximum_limit`, `grace_period_days` |
| 4 | `fee_structures` | Versioned fee schedule templates | `id`, `code`, `name`, `version`, `academic_year_id`, `effective_date`, `validity_date`, `total_amount`, `status` |
| 5 | `fee_structure_items` | Individual fee head item mappings | `id`, `fee_structure_id`, `fee_head_id`, `amount`, `is_optional`, `frequency`, `due_period` |
| 6 | `installments` | Scheduled payment installment plans | `id`, `fee_structure_id`, `installment_number`, `title`, `due_date`, `percentage`, `amount`, `grace_days` |
| 7 | `student_fee_assignments` | Student-specific fee accounts | `id`, `student_id`, `fee_structure_id`, `total_fee_amount`, `total_payable_amount`, `total_paid_amount`, `total_due_amount`, `status` |
| 8 | `payment_methods` | Supported offline & online gateways | `id`, `code`, `name`, `is_online`, `is_active`, `configuration_json` |
| 9 | `payments` | Immutable transaction ledger | `id`, `student_fee_assignment_id`, `payment_number`, `amount_paid`, `payment_mode`, `transaction_reference`, `status` |
| 10 | `receipts` | Official verified receipts | `id`, `receipt_number`, `payment_id`, `total_amount`, `amount_in_words`, `qr_code_data`, `digital_signature_hash` |
| 11 | `scholarships` | Institutional and government aid schemes| `id`, `code`, `name`, `scholarship_type`, `calculation_type`, `value`, `max_beneficiaries` |
| 12 | `discounts` | Sibling, early-bird, and employee discounts| `id`, `code`, `name`, `discount_type`, `calculation_type`, `value`, `max_discount_amount` |
| 13 | `concessions` | Concession disbursements to students | `id`, `student_fee_assignment_id`, `student_id`, `amount`, `reason`, `approval_status` |
| 14 | `refunds` | Approved and audited refund vouchers | `id`, `payment_id`, `refund_number`, `amount`, `refund_type`, `reason`, `approval_status`, `payment_mode` |
| 15 | `fee_due_history` | Historical tracking of unpaid dues | `id`, `student_fee_assignment_id`, `due_date`, `due_amount`, `penalty_amount`, `reminder_count` |
| 16 | `financial_reports` | Generated daily/monthly financial snapshots| `id`, `institute_id`, `report_type`, `start_date`, `end_date`, `total_amount_calculated`, `parameters_json` |

---

### 3. Universal Receipt Generator & Indian Currency Words Engine

Module 9 implements a dedicated Indian numbering system converter (`number_to_indian_currency_words`) handling:
- **Crores** ($10^7$)
- **Lakhs** ($10^5$)
- **Thousands** ($10^3$)
- **Hundreds & Tens**

```python
# Example Conversions:
145000.00   -> "One Lakh Forty Five Thousand Rupees Only"
72500.00    -> "Seventy Two Thousand Five Hundred Rupees Only"
25000000.00 -> "Two Crore Fifty Lakh Rupees Only"
```

Each generated receipt contains:
- **Sequenced Receipt Number**: `REC-MEI-YYYYMMDD-XXXX`
- **QR Code Payload**: Encrypted JSON containing institute name, receipt number, student ID, payment timestamp, and verified status.
- **HMAC SHA-256 Digital Signature**: Tamper-proof hash certifying payment authenticity.

---

### 4. Financial Business Validators & Rule Engine

The `FeeBusinessValidators` class strictly validates:
1. **Date Consistency**: Fee structure `effective_date` must precede `validity_date`.
2. **Non-Duplicate Fee Heads**: Ensures an individual fee head cannot appear more than once within a single fee structure.
3. **100% Installment Allocation**: Verifies that installment percentages strictly sum to 100.0%.
4. **Refund Safeguards**: Ensures requested refund amounts do not exceed the payment amount minus previously settled refunds.

---

### 5. Backend REST API Endpoints (`/api/v1/fees/`)

All endpoints are protected via Bearer JWT tokens and RBAC permissions:

- `GET /api/v1/fees/categories`: Query institutional fee categories.
- `POST /api/v1/fees/categories`: Provision new category (`fees.manage`).
- `GET /api/v1/fees/heads`: Retrieve accounting fee heads.
- `POST /api/v1/fees/heads`: Register new fee head (`fees.manage`).
- `GET /api/v1/fees/structures`: List active fee structure templates with items and installment schedules.
- `POST /api/v1/fees/structures`: Create versioned fee structure (`fees.manage`).
- `POST /api/v1/fees/assignments`: Assign fee structure to a student account.
- `POST /api/v1/fees/collections`: Record payment, recalculate due balances, and issue receipt (`fees.collect`).
- `GET /api/v1/fees/receipts/{payment_id}`: Retrieve official receipt data with QR code payload.
- `POST /api/v1/fees/concessions/apply`: Apply scholarship or discount concession to a student assignment.
- `GET /api/v1/fees/scholarships`: List active institutional scholarships.
- `POST /api/v1/fees/scholarships`: Define scholarship program.
- `GET /api/v1/fees/discounts`: List discount schemes.
- `POST /api/v1/fees/discounts`: Define discount rule.
- `GET /api/v1/fees/late-fees`: Query late fee penalty rules.
- `POST /api/v1/fees/late-fees`: Create late fee rule.
- `POST /api/v1/fees/refunds`: Process audited student refund voucher (`fees.refund`).
- `GET /api/v1/fees/reports/daily-collection`: Generate daily cashier collection breakdown by payment mode.
- `GET /api/v1/fees/reports/outstanding`: Generate aging outstanding dues report.
- `GET /api/v1/fees/analytics`: Real-time dashboard KPI summary.

---

### 6. Frontend Architecture (React 19 + TypeScript)

The Module 9 frontend resides in `frontend/src/modules/fees/`:
- **`FeeDashboardPage.tsx`**: Executive overview displaying projected revenue, total realized revenue, outstanding dues, today's counter collections, mode breakdowns, and fast action hubs.
- **`FeeStructuresPage.tsx`**: Fee structure catalog with itemized breakdowns and scheduled installment plans.
- **`FeeCategoriesPage.tsx`**: Category and fee head management.
- **`FeeCollectionPage.tsx`**: Counter payment terminal supporting Cash, UPI, Cards, Net Banking, and Cheques with live balance reconciliation.
- **`ReceiptViewModal.tsx`**: Printable official institutional fee receipt modal with digital signature hash and QR verification.
- **`ScholarshipsPage.tsx`**: Scholarship catalog displaying criteria, max beneficiaries, and percentage/fixed benefit values.
- **`RefundsManagementPage.tsx`**: Refund request tracking and status indicators.
- **`FinancialReportsPage.tsx`**: Exportable daily cashier sheets and outstanding dues ledgers.
- **`AdminSidebar.tsx`**: Primary navigation item (`IndianRupee` icon) pointing to `/admin/fees`.

---

### 7. Verification & Enterprise Compliance Audit

- **Automated Test Suite**: 37 unit and integration tests passed across Modules 1 through 9 with 0 failures:
  ```text
  Ran 37 tests in 7.279s
  OK (Total tests run: 37, Errors: 0, Failures: 0)
  ALL ENTERPRISE SUITE TESTS (MODULES 1-9) COMPLETED SUCCESSFULLY!
  ```
- **Zero Browser Storage Audit**: Confirmed zero invocations of `localStorage`, `sessionStorage`, or `indexedDB` across all frontend code.
- **AST Compilation**: 100% of Python backend modules compile cleanly.
