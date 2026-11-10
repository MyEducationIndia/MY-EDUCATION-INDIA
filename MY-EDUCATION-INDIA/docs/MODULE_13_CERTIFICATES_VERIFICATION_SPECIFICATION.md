# MY EDUCATION INDIA ERP V2
## Module 13: Enterprise Certificate, Document Generation & Digital Verification System Architecture & Technical Specification

---

### 1. Executive Summary & System Architecture

The **Enterprise Certificate, Document Generation & Digital Verification System (Module 13)** establishes an automated, template-driven credential issuance and public verification infrastructure for **MY EDUCATION INDIA ERP V2**. Designed for universities, institutes, polytechnics, and skill development academies across India, the subsystem manages the full lifecycle of institutional credentials: from drag-and-drop template authoring and dynamic placeholder substitution to batch PDF compilation, cryptographic HMAC SHA-256 digital signing, Universal Number Generator integration, and a zero-login public digital verification portal.

```
                              ┌────────────────────────────────────────┐
                              │      MY EDUCATION INDIA ERP V2         │
                              │ Module 13: Certificate & Verification  │
                              └───────────────────┬────────────────────┘
                                                  │
            ┌─────────────────────────────────────┼─────────────────────────────────────┐
            ▼                                     ▼                                     ▼
┌────────────────────────┐             ┌────────────────────────┐            ┌────────────────────────┐
│ Template & Generation  │             │ Security & Signatures  │            │ Public Verification    │
├────────────────────────┤             ├────────────────────────┤            ├────────────────────────┤
│ • Dynamic Placeholders │             │ • Module 3 Numbering   │            │ • Zero-Login Portal    │
│ • Visual Designer      │             │ • Cryptographic Hashes │            │ • 2D Optical QR Token  │
│ • PDF Print Compiler   │             │ • PKI Digital Sign     │            │ • Alphanumeric Code128 │
│ • Multi-Page Layouts   │             │ • Approval Workflow    │            │ • Masked Privacy Check │
│ • Smart CR80 ID Cards  │             │ • Revocation Audit Log │            │ • Real-time Hit Logs   │
└────────────────────────┘             └────────────────────────┘            └────────────────────────┘
```

#### Core Design Principles
1. **Template-Driven Flexibility (Zero Hardcoded Layouts)**: All certificates, diplomas, transcripts, transfer certificates (TC), bonafides, and ID cards are rendered from dynamic HTML/CSS templates supporting landscape/portrait orientations, custom fonts, borders, seals, and watermark overlays.
2. **Dynamic Placeholder Substitution**: Real-time evaluation and injection of student and academic attributes:
   - `{{student_name}}`, `{{enrollment_number}}`, `{{course_name}}`, `{{cgpa}}`, `{{classification}}`
   - `{{issue_date}}`, `{{certificate_number}}`, `{{verification_id}}`
3. **Module 3 Universal Numbering Integration**: Automatically sequences certificate serials (`PREFIX-YEAR-COUNTER`, e.g., `DEG-2026-000042`, `BONA-2026-000120`) preventing duplicate numbers across institutional departments.
4. **Zero-Login Public Verification Portal**: Anyone—employers, foreign embassies, universities—can verify any issued credential in real time using a direct URL, optical QR scan, or certificate identifier. Personal data is privacy-masked (`A**** S****`).
5. **Tamper-Evident Revocation & Audit Immutability**: Revoking a credential immediately changes its public status from `VALID` to `REVOKED` with reason stamps while preserving a permanent, immutable audit ledger.
6. **Zero-Trust Client-Side Storage**: In full compliance with enterprise specifications, zero certificate keys, tokens, or personal identifiers are stored in browser `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (Alembic Migration `0013_module13_certificates_verification.py`)

Module 13 provisions 15 relational database tables with foreign keys, composite unique constraints, and cascade protections:

| # | Table Name | Description | Key Attributes |
|---|---|---|---|
| 1 | `document_types` | Master repository of document categories | `id`, `institute_id`, `code`, `name`, `category` (ACADEMIC, ADMINISTRATIVE, IDENTIFICATION), `validity_months` |
| 2 | `certificate_templates` | Template blueprints with HTML/CSS markup | `id`, `document_type_id`, `template_code`, `title`, `page_orientation`, `page_size`, `html_markup`, `css_styles` |
| 3 | `certificate_fields` | Dynamic placeholder definitions | `id`, `template_id`, `field_key`, `label`, `field_type`, `is_required`, `default_value` |
| 4 | `certificate_layouts` | Visual drag-and-drop element coordinates | `id`, `template_id`, `elements_json` (X, Y, width, height, z-index, typography) |
| 5 | `certificate_numbers` | Universal sequence counters per prefix/year| `id`, `institute_id`, `prefix`, `year`, `current_counter`, `updated_at` |
| 6 | `issued_certificates` | Official issued credentials ledger | `id`, `certificate_number`, `verification_id`, `template_id`, `recipient_user_id`, `issue_date`, `status` |
| 7 | `generated_documents` | Archive of compiled PDF files | `id`, `document_type_id`, `title`, `file_path`, `file_size_bytes`, `mime_type` |
| 8 | `verification_tokens` | Cryptographic public verification tokens | `id`, `certificate_id`, `token_hash`, `public_verification_url` |
| 9 | `verification_logs` | Audit trail of public verification requests| `id`, `token_id`, `ip_address`, `user_agent`, `verified_at`, `result_status` |
| 10 | `digital_signatures` | PKI / HMAC digital signature records | `id`, `certificate_id`, `signatory_user_id`, `signature_type`, `signature_hash`, `signed_at` |
| 11 | `certificate_status_history`| Status transition ledger (ISSUED -> REVOKED)| `id`, `certificate_id`, `previous_status`, `new_status`, `changed_by_user_id`, `reason` |
| 12 | `id_cards` | Campus CR80 smart identity cards | `id`, `card_number`, `holder_type`, `holder_user_id`, `blood_group`, `emergency_contact`, `valid_until` |
| 13 | `document_archives` | Permanent institutional archive records | `id`, `certificate_id`, `archived_reason`, `archived_by_user_id`, `archived_at` |
| 14 | `certificate_reports` | Generated issuance and verification ledgers| `id`, `institute_id`, `report_type`, `parameters_json`, `generated_by_user_id` |
| 15 | `certificate_analytics`| Aggregate monthly trends and usage rates | `id`, `institute_id`, `snapshot_date`, `total_issued`, `total_verified`, `total_revoked` |

---

### 3. PDF Placeholder Interpolation & Print Layout Engine

The `CertificatePDFCompiler` performs real-time regex placeholder resolution:
```python
# Substituting placeholders with actual academic and student data:
output = re.sub(r"\{\{\s*student_name\s*\}\}", "Aarav Sharma", template_html, flags=re.IGNORECASE)
output = re.sub(r"\{\{\s*course_name\s*\}\}", "B.Tech Computer Science & AI", output, flags=re.IGNORECASE)
output = re.sub(r"\{\{\s*cgpa\s*\}\}", "9.72", output, flags=re.IGNORECASE)
```
Injected CSS rules enforce page size (`A4`, `CR80`, `Letter`), margin resets (`@page { size: landscape; margin: 0; }`), and high-resolution typography.

---

### 4. Cryptographic Verification & QR Token Pipeline

- **Verification Identifier**: `VRF-` prefixed hexadecimal string (e.g. `VRF-98F12A09B42C`)
- **HMAC SHA-256 Token Hash**:
  $$\text{Hash} = \text{SHA256}(\text{Verification ID} : \text{Certificate Number} : \text{Recipient ID} : \text{Salt})$$
- **QR Code Payload**: Encrypted JSON string embedding verification ID, certificate serial number, and canonical public verification link:
  ```json
  {
    "entity": "MY EDUCATION INDIA ERP",
    "document": "OFFICIAL_DIGITAL_CREDENTIAL",
    "cert_no": "DEG-2026-000042",
    "verification_id": "VRF-98F12A09B42C",
    "verify_url": "https://myeducationindia.com/verify?id=VRF-98F12A09B42C",
    "tamper_proof": true
  }
  ```
- **Barcode Payload**: Alphanumeric sanitized Code 128 string (`DEG2026000042`).

---

### 5. Backend REST API Endpoints

All management endpoints are protected via Bearer JWT tokens and role-based permissions, while the verification endpoint is unauthenticated for public access:

- `GET /api/v1/certificates/dashboard`: Real-time dashboard KPI summary (`certificates.view`).
- `GET /api/v1/certificates/types`: List master document classifications (`certificates.view`).
- `POST /api/v1/certificates/types`: Provision custom document type (`certificates.manage`).
- `GET /api/v1/certificates/templates`: Query available HTML/CSS templates.
- `POST /api/v1/certificates/templates`: Save new template blueprint with orientation and layout (`certificates.manage`).
- `POST /api/v1/certificates/issue`: Issue single certificate with auto-generated serial and QR payload (`certificates.issue`).
- `POST /api/v1/certificates/revoke`: Revoke credential with reason and audit trail logging (`certificates.revoke`).
- `POST /api/v1/certificates/id-cards`: Issue smart campus CR80 ID card (`certificates.issue`).
- `GET /api/v1/certificates/reports/register`: Retrieve issuance ledger.
- `GET /api/v1/public/verify/{identifier}`: Unauthenticated public verification endpoint (accepts certificate number or verification ID).

---

### 6. Frontend Architecture (React 19 + TypeScript)

The Module 13 frontend resides in `frontend/src/modules/certificates/`:
- **`CertificateDashboardPage.tsx`**: Executive overview displaying total issued credentials, public verification hits, pending approvals, and document distribution bars.
- **`CertificateTemplatesPage.tsx`**: Template library displaying orientation, dimensions, and active statuses.
- **`VisualCertificateDesignerPage.tsx`**: Interactive layout designer with live SVG preview, institutional crests, and dynamic placeholders.
- **`BulkDocumentGeneratorPage.tsx`**: Batch generation interface for cohort-wide degree and marksheet production.
- **`PublicVerificationPortalPage.tsx`**: Unauthenticated public verification portal featuring search input, validation cards, masked privacy display, and digital signature authentication tags.
- **`IDCardGeneratorPage.tsx`**: Campus identity card issuance interface with blood group and emergency contact management.
- **`CertificateReportsPage.tsx`**: Issuance registers and audit ledgers.
- **`CertificateAnalyticsPage.tsx`**: Credential issuance trends and verification ratios.
- **`CertificateSettingsPage.tsx`**: Cryptographic DSC policies and QR code sizing.
- **`AdminSidebar.tsx`**: Primary navigation link (`FileBadge` icon) pointing to `/admin/certificates`.

---

### 7. Verification & Enterprise Compliance Audit

- **Automated Test Suite**: 65 unit and integration tests passed cleanly across Modules 1 through 13 with 0 errors and 0 failures:
  ```text
  Ran 65 tests in 10.759s
  OK (Total tests run: 65, Errors: 0, Failures: 0)
  ALL ENTERPRISE SUITE TESTS (MODULES 1-13) COMPLETED SUCCESSFULLY!
  ```
- **Zero Browser Storage Audit**: Confirmed zero invocations of `localStorage`, `sessionStorage`, or `indexedDB` across all frontend code.
- **AST Compilation Check**: 100% of Python backend modules compile with valid syntax.
