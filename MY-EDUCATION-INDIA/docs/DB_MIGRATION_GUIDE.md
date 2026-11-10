# MY EDUCATION INDIA – Database Migration Guide

This guide documents the Alembic migration history, database schema evolution, and deployment steps for Neon PostgreSQL.

---

## 1. Migration Overview

The platform uses Alembic for declarative schema versioning. The migration chain comprises 21 sequentially ordered migrations:

| Migration File | Revision ID | Down Revision | Description |
| :--- | :--- | :--- | :--- |
| `0001_initial_module1_schema.py` | `0001_initial_schema` | None (Base) | Core institutional models, users, roles, sessions, campuses |
| `0002_module2_enterprise_auth.py` | `0002_enterprise_auth` | `0001_initial_schema` | Security policies, MFA, login audit, IP security |
| `0003_module3_core_system_engine.py` | `0003_system_engine` | `0002_enterprise_auth` | Workflow engines, notifications, audit log tables |
| `0003_public_website_framework.py` | `0003_website_fw` | `0003_system_engine` | Public website CMS base tables |
| `0004_module2_home_page_cms.py` | `0004_home_cms` | `0003_website_fw` | Homepage dynamic tiles, hero slider, accreditation badges |
| `0004_module4_dashboard_control_center.py` | `0004_dash_control` | `0004_home_cms` | Executive dashboard engines, KPI aggregations |
| `0005_module3_about_cms.py` | `0005_about_cms` | `0004_dash_control` | About campus vision, mission, governance hierarchy |
| `0005_module5_cms_engine.py` | `0005_cms_engine` | `0005_about_cms` | Central CMS article, news, events, notices tables |
| `0006_module4_courses_cms.py` | `0006_courses_cms` | `0005_cms_engine` | Academic course discovery catalog |
| `0006_module6_sims_engine.py` | `0006_sims_engine` | `0006_courses_cms` | Student Information System (SIS) core master records |
| `0007_module7_admission_crm.py` | `0007_admission_crm` | `0006_sims_engine` | Admission leads, counselor workflows, application desk |
| `0008_module8_academic_engine.py` | `0008_academic_engine` | `0007_admission_crm` | Academic calendar, syllabus, curriculum, credit structure |
| `0009_module9_fee_finance.py` | `0009_fee_finance` | `0008_academic_engine` | Fee structures, ledgers, double-entry bookkeeping |
| `0010_module10_attendance_leave.py`| `0010_attendance` | `0009_fee_finance` | Daily attendance, leave requests, biometric machine logs |
| `0011_module11_examination_results.py` | `0011_exam_results`| `0010_attendance` | Conventional university exam marks and SGPA engine |
| `0012_module12_cbt_platform.py` | `0012_cbt_platform` | `0011_exam_results` | CBT question bank, exam builder, live delivery engine |
| `0013_module13_certificates_verification.py`| `0013_certificates`| `0012_cbt_platform` | Digital credentials, anti-counterfeiting QR codes |
| `0014_module14_library_knowledge.py` | `0014_lib_knowledge`| `0013_certificates`| Accession registry, catalog, book issue/return, fines |
| `0015_module15_enterprise_lxp.py` | `0015_lxp_platform` | `0014_lib_knowledge`| LMS courses, lessons, HLS video lectures, discussions |
| `0016_future_api_integration_framework.py` | `0016_api_framework` | `0015_lxp_platform` | External REST connectors, webhooks, banking integrations |
| `0017_module17_crm_marketing_franchise.py` | `0017_crm_franchise`| `0016_api_framework`| Franchise partner inquiries and CRM campaign analytics |
| `0018_module18_bi_analytics_reports.py` | `0018_bi_platform` | `0017_crm_franchise`| BI reporting cubes, executive analytics dashboards |
| `0019_module19_platform_admin_devops.py` | `0019_platform_devops`| `0018_bi_platform` | Telemetry, log aggregator, database schema inspector |
| `0020_module20_enterprise_experience_platform.py` | `0020_experience_platform` | `0019_platform_devops` | Unified portals, root owner sovereign console |
| `0021_enterprise_feature_control_and_security.py` | `0021_feature_control` | `0020_experience_platform` | Master switch feature flags, login policies, admin password reset audit |

---

## 2. Executing Migrations in Production

```bash
cd backend

# Verify current revision
poetry run alembic current

# Upgrade database to latest revision
poetry run alembic upgrade head

# Verify target revision head
poetry run alembic heads
# Output: 0021_feature_control (head)
```

---

## 3. Rollback Procedure

To roll back the most recent migration:

```bash
poetry run alembic downgrade -1
```
