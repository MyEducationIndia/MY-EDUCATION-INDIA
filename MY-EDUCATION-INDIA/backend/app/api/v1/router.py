from fastapi import APIRouter
from app.api.v1.endpoints import (
    audit_logs,
    auth,
    dashboard_engine,
    departments,
    cms_about,
    cms_admissions,
    cms_contact,
    cms_navigation_search,
    cms_courses,
    cms_downloads,
    cms_events_news,
    cms_faculty,
    cms_gallery,
    cms_home,
    cms_placements,
    cms_testimonials,
    health,
    institutes,
    media_file_manager,
    workflows,
    notification_center,
    reports,
    roles,
    system_settings,
    users,
    website,
)
from app.modules.academics.router import router as academics_engine_router
from app.modules.admissions.router import router as admissions_pipeline_router
from app.modules.students.router import student_router
from app.modules.integrations.router import integrations_router
from app.modules.crm.router import crm_router
from app.modules.bi.router import bi_router
from app.modules.platform.router import platform_router
from app.modules.platform.experience_router import experience_router
from app.modules.certificates.router import certificate_router, public_verify_router
from app.modules.library.router import library_router
from app.modules.lxp.router import lxp_router
from app.modules.cbt.router import cbt_router
from app.modules.examinations.router import exam_router
from app.modules.feature_control.router import router as feature_control_router


api_v1_router = APIRouter()

# Core System & Operational Routers
api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(institutes.router)
api_v1_router.include_router(roles.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(departments.router)
api_v1_router.include_router(dashboard_engine.router)
api_v1_router.include_router(notification_center.router)
api_v1_router.include_router(media_file_manager.router)
api_v1_router.include_router(workflows.router)
api_v1_router.include_router(reports.router)
api_v1_router.include_router(audit_logs.router)
api_v1_router.include_router(system_settings.router)

# ERP Subsystems:
# Module 6: Student Information Management System (SIMS)
api_v1_router.include_router(student_router)

# Module 7: Admission & CRM Pipeline Subsystem
api_v1_router.include_router(admissions_pipeline_router)

# Module 8: Academic Engine & Interactive Timetable Planner Subsystem
api_v1_router.include_router(academics_engine_router)

# Phase 1 Module 1: Public Website Framework & Admin Website Governance Routers
api_v1_router.include_router(website.public_website_router)
api_v1_router.include_router(website.admin_website_router)

# Phase 1 Module 2: Home Page CMS & Admin Home Page Management Routers
api_v1_router.include_router(cms_home.public_home_router)
api_v1_router.include_router(cms_home.admin_home_router)

# Phase 1 Module 3: About Institute CMS & Admin Management Routers
api_v1_router.include_router(cms_about.public_about_router)
api_v1_router.include_router(cms_about.admin_about_router)

# Phase 1 Module 4: Course Management CMS & Admin Management Routers
api_v1_router.include_router(cms_courses.public_courses_router)
api_v1_router.include_router(cms_courses.admin_courses_router)

# Phase 1 Module 5: Admission System CMS & Admin Governance Routers
api_v1_router.include_router(cms_admissions.public_admissions_router)
api_v1_router.include_router(cms_admissions.admin_admissions_router)

# Phase 1 Module 6: Faculty, Staff Directory & Research CMS Routers
api_v1_router.include_router(cms_faculty.public_faculty_router)
api_v1_router.include_router(cms_faculty.admin_faculty_router)

# Phase 1 Module 7: Placements, Corporate Recruiters & Success Stories CMS Routers
api_v1_router.include_router(cms_placements.public_placements_router)
api_v1_router.include_router(cms_placements.admin_placements_router)

# Phase 1 Module 8: Events, News, Notices & Achievements CMS Routers
api_v1_router.include_router(cms_events_news.public_events_news_router)
api_v1_router.include_router(cms_events_news.admin_events_news_router)

# Phase 1 Module 9: Gallery Management CMS Routers
api_v1_router.include_router(cms_gallery.public_gallery_router)
api_v1_router.include_router(cms_gallery.admin_gallery_router)

# Phase 1 Module 10: Downloads CMS Routers
api_v1_router.include_router(cms_downloads.public_downloads_router)
api_v1_router.include_router(cms_downloads.admin_downloads_router)

# Phase 1 Module 13: Testimonials & Reviews CMS Routers
api_v1_router.include_router(cms_testimonials.public_testimonials_router)
api_v1_router.include_router(cms_testimonials.admin_testimonials_router)

# Phase 1 Module 14: Contact & Inquiry CMS Routers
api_v1_router.include_router(cms_contact.public_contact_router)
api_v1_router.include_router(cms_contact.admin_contact_router)

# Phase 1 Module 15: Search & Navigation Engine Routers
api_v1_router.include_router(cms_navigation_search.public_navigation_router)
api_v1_router.include_router(cms_navigation_search.public_search_router)
api_v1_router.include_router(cms_navigation_search.public_sitemap_router)
api_v1_router.include_router(cms_navigation_search.admin_navigation_router)

# Module 16: Future API & Third-Party Integration Framework
api_v1_router.include_router(integrations_router)

# Module 17: Enterprise CRM, Marketing Automation & Franchise Management
api_v1_router.include_router(crm_router)

# Module 18: Business Intelligence, Analytics & Executive Reporting
api_v1_router.include_router(bi_router)

# Module 19: Enterprise Platform Administration, DevOps & Infrastructure
api_v1_router.include_router(platform_router)

# Module 20: Enterprise Experience Platform & Unified Portals (Final Blueprint Milestone)
api_v1_router.include_router(experience_router)

# Module 13: Enterprise Certificate Generation & Digital Verification Subsystem
api_v1_router.include_router(certificate_router)
api_v1_router.include_router(public_verify_router)

# Module 14: Enterprise Library & Digital Knowledge Management Subsystem
api_v1_router.include_router(library_router)

# Module 15: Enterprise Learning Experience Platform (LXP) Subsystem
api_v1_router.include_router(lxp_router)

# Phase 3 Module 1: Enterprise Computer Based Testing (CBT) Subsystem
api_v1_router.include_router(cbt_router)

# Phase 4: Enterprise Examination Management System (EMS)
api_v1_router.include_router(exam_router)

# Enterprise Feature Control Center & Security Management
api_v1_router.include_router(feature_control_router)
