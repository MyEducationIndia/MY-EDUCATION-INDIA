# MY EDUCATION INDIA – Campus Administrator Manual

This manual details administrative workflows for Campus Administrators, Registrars, Finance Officers, and Exam Controllers.

---

## 1. User ID Provisioning & Management

Campus administrators can provision users via the Administrator Console or via batch CSV upload.
* **Format Standards:**
  * Student IDs: Auto-generated as `STU` + Year + 4-digit sequence (e.g. `STU240001`)
  * Faculty IDs: Auto-generated as `FAC` + Year + 4-digit sequence (e.g. `FAC240001`)
  * Staff IDs: Auto-generated as `EMP` + Year + 4-digit sequence (e.g. `EMP240001`)
  * Admin IDs: Formatted as `ADM000001`
* **Duplicate Detection:** The system performs atomic row-level uniqueness checks in PostgreSQL to prevent ID collisions.

---

## 2. Administrator-Only Password Reset Desk

Because self-service password recovery is removed from public login pages to prevent unauthorized account takeover, administrators manage password resets through the audited reset desk:

1. Navigate to **Security Desk > Password Reset Desk** (`/root/feature-control` under the "Admin Password Reset Desk" tab).
2. Enter the target **User ID** (e.g., `STU240001`).
3. Select the **Identity Verification Method**:
   * `IN_PERSON_CAMPUS_ID` – Physical institutional ID card inspected in-person.
   * `GOVT_ID_BIOMETRIC` – Government Aadhaar / Passport verified against biometric records.
   * `FACULTY_DEAN_RECOMMENDATION` – Written and signed memo from Department Head.
   * `REGISTRAR_BOARD_APPROVAL` – Official approval by the Board of Examinations.
4. Enter the **Administrative Justification** (mandatory reason).
5. Click **Generate Temporary Password & Force First-Login Change**.
6. Hand the temporary password to the user.
7. Upon initial login, the platform will immediately force the user to set a new password meeting all complexity rules.

---

## 3. Academic Operations & Registrars

* **Admission Pipeline:** Review submitted online applications, verify certificates, and generate merit lists.
* **Fee Structure:** Configure fee heads, semester tuition installments, concessions, and fine schedules.
* **Biometric & Attendance Tracking:** Audit daily RFID attendance sync jobs and issue warning notices to students falling below the 75% attendance threshold.
* **Examination Management:** Generate hall seating plans, issue signed hall tickets, moderate semester marks, and print consolidated academic transcripts.
