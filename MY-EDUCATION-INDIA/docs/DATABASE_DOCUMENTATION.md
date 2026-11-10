# MY EDUCATION INDIA ERP V2 — DATABASE SCHEMA DOCUMENTATION

## 1. Database Specifications
- **Engine**: PostgreSQL 15+ (Neon Serverless Compatible)
- **Driver**: `asyncpg` via SQLAlchemy 2.x Async Engine
- **Migration Tool**: Alembic (20 Sequential Versioned Migrations)
- **Isolation Scope**: Optimized for single institute **MY EDUCATION INDIA** (`MEI-HQ`).

## 2. Master Table Inventory Across 20 Modules
1. **Core Foundation & Auth (Modules 1–2)**: `institutes`, `roles`, `permissions`, `role_permissions`, `users`, `user_roles`, `refresh_tokens`, `audit_logs`, `module_configs`.
2. **System & Dashboard (Modules 3–4)**: `branches`, `academic_years`, `financial_years`, `number_generators`, `number_sequences`, `system_settings`, `dashboard_metrics_cache`.
3. **CMS & SIMS (Modules 5–6)**: `cms_pages`, `cms_sections`, `cms_menus`, `students`, `student_documents`, `guardians`, `medical_records`.
4. **Admissions & Academics (Modules 7–8)**: `admission_enquiries`, `admission_applications`, `departments`, `programs`, `courses`, `batches`, `sections`, `timetables`.
5. **Fees & Attendance (Modules 9–10)**: `fee_structures`, `fee_heads`, `student_fee_assignments`, `fee_receipts`, `fee_concessions`, `attendance_sessions`, `student_attendance`, `leave_requests`.
6. **Examinations & CBT (Modules 11–12)**: `exam_sessions`, `exam_schedules`, `hall_tickets`, `exam_marks`, `grade_scales`, `transcripts`, `cbt_question_banks`, `cbt_questions`, `cbt_exam_sessions`.
7. **Certificates & Verification (Module 13)**: `certificate_templates`, `issued_certificates`, `verification_logs`.
8. **Library & Knowledge (Module 14)**: `library_books`, `library_book_copies`, `library_categories`, `library_members`, `library_issues`, `library_fines`, `library_digital_resources`.
9. **LXP & Learning (Module 15)**: `learning_courses`, `learning_modules`, `learning_lessons`, `video_library`, `course_enrollments`, `learning_progress`, `assignment_submissions`, `discussion_topics`.
10. **API Integrations (Module 16)**: `api_providers`, `api_credentials`, `api_endpoints`, `api_execution_logs`, `webhook_registrations`, `webhook_delivery_logs`.
11. **CRM & Franchise (Module 17)**: `crm_leads`, `crm_enquiries`, `crm_followups`, `crm_pipeline`, `crm_campaigns`, `crm_opportunities`, `franchise_centers`.
12. **BI & Analytics (Module 18)**: `report_definitions`, `report_templates`, `report_schedules`, `dashboard_widgets`, `kpi_definitions`, `system_health_logs`.
13. **Platform DevOps (Module 19)**: `platform_settings`, `security_policies`, `backup_jobs`, `backup_history`, `restore_history`, `feature_flags`, `storage_configs`.
14. **Experience Platform (Module 20)**: `root_owner_controls`, `portal_configurations`, `dynamic_menus`, `dynamic_menu_items`, `page_definitions`, `form_definitions`, `global_search_index`.
