# MY EDUCATION INDIA ERP V2 — MODULE 17 SPECIFICATION
## ENTERPRISE CRM, SALES, MARKETING & FRANCHISE MANAGEMENT SYSTEM

### 1. Executive Summary & Architectural Overview
Module 17 provides an enterprise-class **Customer Relationship Management (CRM), Sales Pipeline, Multi-Channel Marketing, and Regional Franchise Operations Platform** for MY EDUCATION INDIA ERP V2. It orchestrates the full student prospective journey—from initial multi-channel lead capture to counselling, follow-up cadence, fee discussions, and automated conversion into academic admissions.

#### Key Architectural Highlights
- **Universal Multi-Channel Inbound Capture**: Ingestion from Website forms (Module 5), Walk-in terminals, Phone enquiries, Meta/Google Ad leads, WhatsApp bots, and education fairs.
- **Dynamic 9-Stage Sales Pipeline**: Configurable Kanban progression:
  $$	ext{New Lead} \longrightarrow 	ext{Contacted} \longrightarrow 	ext{Counselling} \longrightarrow 	ext{Demo Given} \longrightarrow 	ext{Interested} \longrightarrow 	ext{Documents Pending} \longrightarrow 	ext{Fee Discussion} \longrightarrow 	ext{Admission Confirmed} \ / \ 	ext{Lost}$$
- **Intelligent Lead Scoring Engine (`lead_engine.py`)**: Algorithmic lead prioritization (scores 40–100) based on source reliability, priority weighting, and contact data completeness. Also enforces smart mobile (+91 national normalization) and email deduplication.
- **Follow-up & Communications Broker (`automation_engine.py`)**: Dynamic callback interval calculation with direct integration into Module 16 (Communication Center & API Integration Framework) for SMS, WhatsApp, and Email triggers.
- **Marketing Campaign ROI Engine (`campaign_engine.py`)**: Tracks marketing spends vs. admissions revenue to compute accurate Cost Per Lead (CPL) and Campaign Return on Investment (ROI%).
- **Franchise & Regional Center Readiness**: Multitenant architecture with dedicated regional center ledgers, counselor user mappings, royalty tracking, and performance analytics without modifying core ERP tables.
- **Zero Client-Side Storage**: 100% compliant with zero usage of `localStorage`, `sessionStorage`, or `indexedDB`.

---

### 2. Database Schema (16 Enterprise Relational Tables)
Provisioned via Alembic revision `0017_crm_franchise`:
1. `crm_leads`: Master prospective student profiles, lead codes, contact info, priority, assigned counselor, stage, and scores.
2. `crm_enquiries`: Unqualified enquiries from website, phone, walk-ins, and social campaigns with 1-click lead promotion.
3. `crm_followups`: Scheduled callbacks, disposition notes, channels (Call, WhatsApp, Email, Meeting), and reminder flags.
4. `crm_pipeline`: Configurable pipeline stages, win/lost stage flags, order indices, and conversion probabilities.
5. `crm_campaigns`: Campaign budgets, actual expenditure, UTM parameters, channel types, and schedules.
6. `crm_campaign_results`: Generated leads, converted admissions, total revenue, CPL, and ROI percentages.
7. `crm_lead_sources`: Standardized acquisition channels (Google Ads, Meta, Website, Referrals, Walk-ins).
8. `crm_referrals`: Student, staff, and partner referral tracking with coupon codes and commission disbursement states.
9. `crm_tasks`: Admission quota assignments, document verification tasks, and priority deadlines.
10. `crm_opportunities`: Deal value, expected closing dates, probability weightings, and revenue forecasts.
11. `crm_activity_logs`: Chronological audit trail of counselor interactions, stage transitions, and notes.
12. `crm_reports`: Pre-aggregated reports for conversions, counselor scorecards, and campaign audits.
13. `crm_analytics`: Daily snapshots of new leads, pipeline velocity, won revenue, and drop-off counts.
14. `franchise_centers`: Regional centers, city/state locations, center heads, and royalty percentage terms.
15. `franchise_users`: Counselor and administrative staff assignments linked to franchise centers.
16. `franchise_settings`: Key-value configuration for center-specific admission rules and branding.

---

### 3. Business Logic & Calculation Engines
- **Lead Scoring & Deduplication Engine (`lead_engine.py`)**:
  - Baseline score: 40 points.
  - Priority bonuses: Urgent (+30), High (+20), Medium (+10).
  - Source weights: Walk-in (+25), Referral (+20), Phone (+15), Website (+10), Social Ads (+5).
  - Contact completeness: Guardian (+5), Email (+5). Capped at 100 points.
  - Mobile normalization: Strips international and formatting characters to compare trailing 10 digits.
- **Follow-up Automation Engine (`automation_engine.py`)**:
  - Stage-based follow-up intervals: New Lead (1 day), Contacted (2 days), Counselling (3 days), Documents Pending (4 days), Fee Discussion (2 days).
  - Interfacing with Module 16 Communication Center for multi-channel alerts.
- **Campaign ROI Engine (`campaign_engine.py`)**:
  $$	ext{Cost Per Lead (CPL)} = rac{	ext{Total Spent}}{	ext{Leads Generated}}$$
  $$	ext{ROI \%} = rac{	ext{Revenue Generated} - 	ext{Total Spent}}{	ext{Total Spent}} 	imes 100$$
- **Revenue Forecast Analytics (`analytics.py`)**:
  $$	ext{Weighted Pipeline Revenue} = \sum (	ext{Deal Value} 	imes 	ext{Probability \%})$$

---

### 4. Frontend & Navigation Architecture
- **Path**: `frontend/src/modules/crm/`
- **14 Submodules Delivered**:
  - `dashboard/CrmDashboardPage.tsx`: Executive CRM telemetry (128 Leads, 24 Follow-ups, 32.8% Conversion Rate, ₹42.50L Forecast).
  - `leads/LeadsDirectoryPage.tsx`: Searchable lead master with priority filters, counselor assignments, and stage indicators.
  - `enquiries/EnquiriesInboxPage.tsx`: Multi-channel enquiry inbox with 1-click lead conversion.
  - `followups/FollowupCalendarPage.tsx`: Counselor calendar with callback schedules and communication triggers.
  - `pipeline/SalesPipelineKanbanPage.tsx`: Interactive Kanban board for dragging leads across 9 stages.
  - `campaigns/MarketingCampaignsPage.tsx`: Campaign performance tracker with budget, CPL, and ROI metrics.
  - `referrals/ReferralProgramsPage.tsx`: Referral incentives, affiliate coupon codes, and reward status.
  - `tasks/CrmTasksPage.tsx`: Sales and counselling task queues with priority and due date alerts.
  - `franchise/FranchiseManagementPage.tsx`: Regional center management, royalty tracking, and center heads.
  - `reports/CrmReportsPage.tsx`: Audit reports, conversion rates, and counselor performance scorecards.
  - `analytics/CrmAnalyticsPage.tsx`: Revenue forecasting, conversion trends, and city demographics.
  - `settings/CrmSettingsPage.tsx`: Pipeline stage customizer, scoring rules, and auto-assignment hooks.
  - `types/crm.types.ts` & `services/crmService.ts`: TypeScript interfaces and API client.
- **Routing**: Mounted under `/admin/crm/*` in `AppRoutes.tsx` with navigation item `CRM & Sales` (`Contact2` icon).

---

### 5. Verification & Testing
- Unit test suite `tests/unit/test_module17_backend_crm.py` executed with 100% pass rate:
  - Clean AST syntax across all 13 Python files in `backend/app/modules/crm/`.
  - Pydantic schema validation for leads, enquiries, campaigns, opportunities, and franchise centers.
  - Mobile format validation (+91 normalization), email format validation, and pipeline stage checks.
  - Lead scoring calculation and duplicate detection across phone/email variants.
  - Follow-up interval scheduling and notification alert payload generation.
  - Campaign CPL and ROI percentage computations.
  - Conversion metrics and probability-weighted pipeline revenue forecasting.
  - Zero browser storage audit: 0 instances of `localStorage`, `sessionStorage`, or `indexedDB`.
