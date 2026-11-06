from fastapi import APIRouter
from app.api.v1.endpoints import (
    audit_logs,
    health,
    institutes,
    roles,
    users,
)
from app.modules.auth.router import admin_auth_router, auth_router
from app.modules.system.router import system_router
from app.modules.dashboard.router import dashboard_router
from app.modules.cms.router import cms_router
from app.modules.students.router import student_router
from app.modules.admissions.router import admission_router
from app.modules.academics.router import academic_router
from app.modules.fees.router import fee_router
from app.modules.attendance.router import attendance_router
from app.modules.examinations.router import exam_router
from app.modules.cbt.router import cbt_router
from app.modules.certificates.router import certificate_router, public_verify_router
from app.modules.library.router import library_router
from app.modules.lxp.router import lxp_router
from app.modules.integrations.router import integrations_router
from app.modules.crm.router import crm_router
from app.modules.bi.router import bi_router
from app.modules.platform.router import platform_router
from app.modules.platform.experience_router import experience_router

api_v1_router = APIRouter()

# Core System Routers
api_v1_router.include_router(health.router)
api_v1_router.include_router(institutes.router)
api_v1_router.include_router(roles.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(audit_logs.router)

# Enterprise Module 2 Authentication & Authorization Routers
api_v1_router.include_router(auth_router)
api_v1_router.include_router(admin_auth_router)

# Enterprise Module 3 Core System Engine Router (/api/v1/system)
api_v1_router.include_router(system_router)

# Enterprise Module 4 Admin Dashboard & Control Center Router (/api/v1/dashboard)
api_v1_router.include_router(dashboard_router)

# Enterprise Module 5 Website CMS & Page Builder Router (/api/v1/cms)
api_v1_router.include_router(cms_router)

# Enterprise Module 6 Student Information Management System Router (/api/v1/students)
api_v1_router.include_router(student_router)

# Enterprise Module 7 Admission & CRM System Router (/api/v1/admissions)
api_v1_router.include_router(admission_router)

# Enterprise Module 8 Academic Management System Router (/api/v1/academics)
api_v1_router.include_router(academic_router)

# Enterprise Module 9 Fee & Finance Management System Router (/api/v1/fees)
api_v1_router.include_router(fee_router)

# Enterprise Module 10 Attendance & Leave Management System Router (/api/v1/attendance)
api_v1_router.include_router(attendance_router)

# Enterprise Module 11 Examination & Result Management System Router (/api/v1/exams)
api_v1_router.include_router(exam_router)

# Enterprise Module 12 Computer Based Testing (CBT) Platform Router (/api/v1/cbt)
api_v1_router.include_router(cbt_router)

# Enterprise Module 13 Certificate, Document Generation & Digital Verification Router (/api/v1/certificates & /api/v1/public/verify)
api_v1_router.include_router(certificate_router)
api_v1_router.include_router(public_verify_router)

# Enterprise Module 14 Library & Digital Knowledge Management Router (/api/v1/library)
api_v1_router.include_router(library_router)

# Enterprise Module 15 Learning Experience Platform Router (/api/v1/lxp)
api_v1_router.include_router(lxp_router)

# Universal API Integration Framework Router (/api/v1/integrations)
api_v1_router.include_router(integrations_router)

# Enterprise Module 17 CRM, Sales, Marketing & Franchise Router (/api/v1/crm)
api_v1_router.include_router(crm_router)

# Enterprise Module 18 Reports, Analytics & BI Router (/api/v1/bi)
api_v1_router.include_router(bi_router)

# Enterprise Module 19 Platform Administration & DevOps Router (/api/v1/platform)
api_v1_router.include_router(platform_router)

# Enterprise Module 20 Experience Platform Master Router (/api/v1/experience)
api_v1_router.include_router(experience_router)
