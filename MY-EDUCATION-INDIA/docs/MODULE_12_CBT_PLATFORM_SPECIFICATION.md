# MY EDUCATION INDIA ERP V2
## Module 12: Enterprise Computer Based Testing (CBT) Platform Architecture & Technical Specification

---

### 1. Executive Summary & System Architecture

The **Enterprise Computer Based Testing (CBT) Platform (Module 12)** serves as the high-concurrency, multi-modal examination delivery and testing execution engine of **MY EDUCATION INDIA ERP V2**. Operating strictly under the academic governance of **Module 11 (Enterprise Examination & Result Management System)**, Module 12 functions as the secure delivery layer: executing LAN-based, online, offline, and hybrid tests while synchronizing candidate scores directly back to Module 11 without duplicating grading or result computation logic.

```
                              ┌────────────────────────────────────────┐
                              │      MY EDUCATION INDIA ERP V2         │
                              │ Module 12: Enterprise CBT Platform     │
                              └───────────────────┬────────────────────┘
                                                  │
            ┌─────────────────────────────────────┼─────────────────────────────────────┐
            ▼                                     ▼                                     ▼
┌────────────────────────┐             ┌────────────────────────┐            ┌────────────────────────┐
│ Question Bank & Pool   │             │ Delivery & Offline LAN │            │ Proctoring & Sync      │
├────────────────────────┤             ├────────────────────────┤            ├────────────────────────┤
│ • Master Question Bank │             │ • Online / LAN / Hybrid│            │ • Real-time Heartbeat  │
│ • MCQ, MSQ, Numerical  │             │ • Seed Randomization   │            │ • Fullscreen Lockdown  │
│ • LaTeX & Rich Media   │             │ • Autosave Every 3 Sec │            │ • Anti-Tamper Checksum │
│ • Difficulty Balancer  │             │ • Sub-second Resumption│            │ • Live Telemetry Feed  │
│ • Bloom Taxonomy Tags  │             │ • Offline Checksum Sync│            │ • Sync to Module 11    │
└────────────────────────┘             └────────────────────────┘            └────────────────────────┘
```

#### Core Design Principles
1. **Module 11 Examination Master Integration**: The CBT module acts exclusively as an exam delivery pipeline. Candidate test marks are directly fed into `Module 11 (ExamSubject / MarkEntry)` where institutional SGPA/CGPA calculations, grade cards, and official transcripts are computed.
2. **Deterministic Seed Randomization**: Every candidate session generates a unique integer seed:
   $$\text{Seed} = \text{Hash}(\text{Session ID} + \text{Student ID} + \text{Salt})$$
   Questions and multiple-choice options are pseudo-randomly permuted per candidate, preventing screen copying while maintaining identical difficulty balances across cohorts.
3. **Offline LAN Survivability & Auto-Sync**: In the event of network disruption or power instability in testing centers, candidate responses are preserved locally in memory cache and synchronized with cloud servers upon reconnection using SHA-256 cryptographic checksum batches.
4. **Active Proctoring & Browser Lockdown**: Fullscreen enforcement, tab-switch telemetry tracking, copy-paste prevention, right-click disabling, and administrative remote force-submission controls.
5. **Zero-Trust Client-Side Storage**: In full compliance with enterprise specifications, zero test question answers or sensitive candidate sessions are permanently preserved in browser `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (Alembic Migration `0012_module12_cbt_platform.py`)

Module 12 provisions 18 relational database tables with foreign keys, composite unique constraints, and cascade protections:

| # | Table Name | Description | Key Attributes |
|---|---|---|---|
| 1 | `question_banks` | Subject-level item bank repositories | `id`, `institute_id`, `code`, `name`, `subject_id`, `is_active` |
| 2 | `question_categories` | Curricular categories within item banks | `id`, `question_bank_id`, `code`, `name` |
| 3 | `question_topics` | Granular unit and lesson topics | `id`, `category_id`, `name` |
| 4 | `question_tags` | Cross-disciplinary taxonomy labels | `id`, `institute_id`, `tag_name` |
| 5 | `question_versions` | Versioned questions (MCQ, MSQ, Numerical, LaTeX) | `id`, `topic_id`, `question_code`, `question_type`, `difficulty_level`, `question_text`, `options_json`, `default_marks`, `negative_marks` |
| 6 | `question_media` | Diagrams, audio, and video attachments | `id`, `question_id`, `media_type` (IMAGE, AUDIO, VIDEO), `media_url` |
| 7 | `question_pools` | Dynamic question selection criteria | `id`, `institute_id`, `name`, `selection_rules_json` |
| 8 | `exam_templates` | Blueprint configurations and blueprints | `id`, `title`, `duration_minutes`, `total_marks`, `passing_marks`, `shuffle_questions`, `allow_calculator` |
| 9 | `cbt_sessions` | Active testing windows and schedules | `id`, `template_id`, `exam_subject_id` (Module 11 link), `session_code`, `start_window`, `end_window`, `delivery_mode` |
| 10 | `candidate_sessions` | Individual student active test instances | `id`, `cbt_session_id`, `student_id`, `random_seed`, `remaining_seconds`, `status`, `total_score`, `marks_synced_to_module11` |
| 11 | `candidate_answers` | Student response records per question | `id`, `candidate_session_id`, `question_id`, `selected_options_json`, `is_marked_for_review`, `is_correct`, `awarded_marks` |
| 12 | `answer_logs` | Audit trail of click events and changes | `id`, `candidate_session_id`, `question_id`, `action_type`, `payload_json`, `timestamp` |
| 13 | `offline_sync_logs` | Checksum verification of offline LAN syncs | `id`, `candidate_session_id`, `batch_count`, `checksum`, `status`, `synced_at` |
| 14 | `live_monitor_logs` | Real-time proctor alerts & tab switches | `id`, `cbt_session_id`, `candidate_session_id`, `event_type`, `warning_count`, `logged_at` |
| 15 | `question_statistics`| Item Response Theory (IRT) difficulty & discrimination | `id`, `question_id`, `total_attempts`, `difficulty_index` (P), `discrimination_index` (D), `average_time_seconds` |
| 16 | `candidate_statistics`| Speed and accuracy metrics per candidate | `id`, `candidate_session_id`, `attempted_count`, `correct_count`, `accuracy_percentage`, `speed_questions_per_minute` |
| 17 | `exam_statistics` | Aggregate session metrics | `id`, `cbt_session_id`, `total_registered`, `total_appeared`, `average_score`, `highest_score` |
| 18 | `cbt_reports` | Generated test ledgers and regulatory exports | `id`, `institute_id`, `report_type`, `parameters_json`, `generated_by_user_id` |

---

### 3. Question Evaluation & Randomization Engine

#### Supported Question Types
1. **Multiple Choice Question (MCQ)**: Single correct choice. Returns $+M_{\text{pos}}$ on exact match, $-M_{\text{neg}}$ on mismatch.
2. **Multiple Select Question (MSQ)**: Multi-selection option sets. Requires exact set equivalence $U_{\text{selected}} = C_{\text{correct}}$ for full credit.
3. **Numerical Input**: Precision floating point evaluation within tolerance $\epsilon = 0.01$.
4. **True / False & Fill in the Blanks**: Binary and text-normalized token validation.

#### Deterministic Seeded Randomization
```python
# Shuffling questions and option alternatives:
paper = PseudoRandomizer.shuffle_items_with_seed(questions, candidate_seed)
for idx, q in enumerate(paper):
    opt_seed = candidate_seed + idx + 997
    q["options"] = PseudoRandomizer.shuffle_items_with_seed(q["options"], opt_seed)
```

---

### 4. Offline LAN Synchronization & Checksum Verification

To ensure tamper-proof offline examination execution in local campus laboratories:
- **Checksum Algorithm**: SHA-256 over deterministically serialized JSON payloads.
- **Verification Rule**:
  $$\text{Data Valid} \iff \text{SHA256}(\text{Batch JSON}) = \text{Client Checksum}$$
- **Conflict Handling**: Server retains highest timestamp version upon network reconciliation.

---

### 5. Backend REST API Endpoints (`/api/v1/cbt/`)

All endpoints are protected via Bearer JWT tokens and role-based permissions:

- `GET /api/v1/cbt/dashboard`: Real-time dashboard KPI summary (`cbt.view`).
- `GET /api/v1/cbt/question-bank`: List master question banks.
- `POST /api/v1/cbt/question-bank`: Create question bank repository (`cbt.manage`).
- `POST /api/v1/cbt/questions`: Add versioned question with options and marks (`cbt.manage`).
- `POST /api/v1/cbt/templates`: Create exam template blueprint with duration and marks (`cbt.manage`).
- `POST /api/v1/cbt/sessions`: Schedule live examination session (`cbt.manage`).
- `POST /api/v1/cbt/delivery/start`: Initialize candidate test instance with seed.
- `POST /api/v1/cbt/delivery/autosave`: Background response autosave endpoint.
- `POST /api/v1/cbt/delivery/submit`: Final paper submission and automatic synchronization to Module 11 marks.
- `POST /api/v1/cbt/offline-sync`: Batch sync offline answers with SHA-256 verification.
- `GET /api/v1/cbt/reports/score`: Candidate score summary report.

---

### 6. Frontend Architecture (React 19 + TypeScript)

The Module 12 frontend resides in `frontend/src/modules/cbt/`:
- **`CBTDashboardPage.tsx`**: Executive overview displaying live candidate meters, question bank volumes, LAN sync statuses, and active testing sessions.
- **`QuestionBankPage.tsx`**: Item repository directory with topic tags and bulk upload hooks.
- **`ExamBuilderPage.tsx`**: Interactive visual exam blueprint designer for duration, marks, question pools, and on-screen calculator toggles.
- **`CandidateExamInterfacePage.tsx`**: Candidate testing HUD featuring real-time countdown timer, question palette, review flagging, and autosave feedback.
- **`LiveProctorMonitorPage.tsx`**: Real-time invigilator monitor tracking active candidates, tab-switching warnings, and force-submit controls.
- **`QuestionAnalyticsPage.tsx`**: Item Response Theory (IRT) analytics for difficulty and discrimination indices.
- **`OfflineSyncStatusPage.tsx`**: Campus LAN synchronization and SHA-256 checksum audit tracker.
- **`CBTSecuritySettingsPage.tsx`**: Lockdown browser policies, copy-paste disabling, and disqualification thresholds.
- **`CBTReportsPage.tsx`**: Exportable test score sheets and Module 11 result integration verification.
- **`AdminSidebar.tsx`**: Primary navigation link (`MonitorPlay` icon) pointing to `/admin/cbt`.

---

### 7. Verification & Enterprise Compliance Audit

- **Automated Test Suite**: 58 unit and integration tests passed cleanly across Modules 1 through 12 with 0 errors and 0 failures:
  ```text
  Ran 58 tests in 2.296s
  OK (Total tests run: 58, Errors: 0, Failures: 0)
  ALL ENTERPRISE SUITE TESTS (MODULES 1-12) COMPLETED SUCCESSFULLY!
  ```
- **Zero Browser Storage Audit**: Confirmed zero invocations of `localStorage`, `sessionStorage`, or `indexedDB` across all frontend code.
- **AST Compilation Check**: 100% of Python backend modules compile with valid syntax.
