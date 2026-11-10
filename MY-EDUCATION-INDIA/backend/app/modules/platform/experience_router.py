"""
Module 20: Enterprise Experience Platform & Unified Portal Experience Router
Mounted under /api/v1/experience
"""
import uuid
from datetime import datetime, timezone, date
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status

experience_router = APIRouter(prefix="/experience", tags=["Enterprise Experience Platform & Unified Portals"])

_PORTALS_STORE = [
    {
        "portal_type": "ROOT_OWNER",
        "display_title": "Root Sovereign Master Console",
        "default_route": "/admin/dashboard",
        "allowed_roles": ["ROOT_OWNER"],
        "accent_color": "#4f46e5",
        "tagline": "Sovereign platform encryption, emergency lockouts, and license provisioning.",
        "icon": "ShieldAlert"
    },
    {
        "portal_type": "SUPER_ADMIN",
        "display_title": "Super Admin Command Center",
        "default_route": "/admin/dashboard",
        "allowed_roles": ["SUPER_ADMIN"],
        "accent_color": "#1e40af",
        "tagline": "Campus governance, 20-module subsystem control matrix, and user provisioning.",
        "icon": "Sliders"
    },
    {
        "portal_type": "INSTITUTE_ADMIN",
        "display_title": "Academic Director & Principal Portal",
        "default_route": "/admin/academics",
        "allowed_roles": ["INSTITUTE_ADMIN"],
        "accent_color": "#0d9488",
        "tagline": "Faculty workload distribution, curriculum approvals, and CBT proctoring.",
        "icon": "Building2"
    },
    {
        "portal_type": "FACULTY",
        "display_title": "Professor & Academic Desk",
        "default_route": "/faculty",
        "allowed_roles": ["FACULTY"],
        "accent_color": "#059669",
        "tagline": "Attendance rollcalls, marksheet moderation, and research publication repositories.",
        "icon": "GraduationCap"
    },
    {
        "portal_type": "STUDENT",
        "display_title": "Student Scholar 360° Portal",
        "default_route": "/student",
        "allowed_roles": ["STUDENT"],
        "accent_color": "#2563eb",
        "tagline": "Course registrations, digital admit cards, fee receipts, and CBT exams.",
        "icon": "BookOpen"
    },
    {
        "portal_type": "COUNSELLOR",
        "display_title": "Admissions & Lead Triage Desk",
        "default_route": "/admin/crm",
        "allowed_roles": ["COUNSELLOR"],
        "accent_color": "#d97706",
        "tagline": "Multi-stage pipeline, outreach calls, WhatsApp follow-ups, and seat allocations.",
        "icon": "Target"
    },
    {
        "portal_type": "ACCOUNTANT",
        "display_title": "Bursar & Finance Desk",
        "default_route": "/admin/fees",
        "allowed_roles": ["ACCOUNTANT"],
        "accent_color": "#0891b2",
        "tagline": "GST fee invoicing, scholarship concessions, payment gateway reconciliations.",
        "icon": "IndianRupee"
    },
    {
        "portal_type": "RECEPTION",
        "display_title": "Front Desk & Public Inquiries",
        "default_route": "/admin/contact",
        "allowed_roles": ["RECEPTION"],
        "accent_color": "#7c3aed",
        "tagline": "Visitor badges, helpline hotline triage, and campus tour bookings.",
        "icon": "PhoneCall"
    },
    {
        "portal_type": "ALUMNI",
        "display_title": "Global Alumni Network",
        "default_route": "/stories",
        "allowed_roles": ["ALUMNI"],
        "accent_color": "#ea580c",
        "tagline": "Mentorship connections, transcript requests, and career networking.",
        "icon": "Award"
    },
    {
        "portal_type": "RECRUITER",
        "display_title": "Corporate Hiring Partner Portal",
        "default_route": "/recruiters",
        "allowed_roles": ["RECRUITER"],
        "accent_color": "#db2777",
        "tagline": "Placement drive shortlists, campus interview slots, and offer letters.",
        "icon": "Briefcase"
    }
]

_NOTIFICATIONS_STORE = [
    {
        "id": "notif_01",
        "title": "Semester CBT Examination Hall Tickets Issued",
        "category": "ACADEMIC",
        "message": "Hall tickets with encrypted QR hashes are live for B.Tech, M.Tech, and MBA cohorts.",
        "timestamp": "2026-11-09T17:00:00Z",
        "priority": "HIGH",
        "is_read": False
    },
    {
        "id": "notif_02",
        "title": "Admissions 2026-27 Intake Reaches 1,420 Enrolled",
        "category": "ADMISSIONS",
        "message": "Indore campus flagship CSE and Cloud programs have attained 100% quota fulfillment.",
        "timestamp": "2026-11-09T16:30:00Z",
        "priority": "MEDIUM",
        "is_read": True
    },
    {
        "id": "notif_03",
        "title": "PostgreSQL Neon Automated Snapshot Completed",
        "category": "DEVOPS",
        "message": "Nightly cluster snapshot (100.0 MB) verified with SHA-256 and backed up to S3 Glacier.",
        "timestamp": "2026-11-09T02:00:00Z",
        "priority": "LOW",
        "is_read": True
    }
]

_ROOT_STATE = {
    "owner_username": "root_master_admin",
    "emergency_lockdown_active": False,
    "developer_mode_enabled": True,
    "license_tier": "ENTERPRISE_LIFETIME_AUTONOMOUS_CAMPUS",
    "total_institutes_active": 1,
    "campus_name": "MY EDUCATION INDIA - Central Autonomous Campus (MEI-HQ)",
    "campus_location": "Indore, Madhya Pradesh, India",
    "total_modules_licensed": 20,
    "complete_blueprint_verified": True
}

ERP_MASTER_MODULES = [
    {"id": 1, "key": "MODULE_1_ARCHITECTURE", "name": "Architecture & Security Foundation", "subdomain": "admin", "category": "CORE", "status": "LIVE"},
    {"id": 2, "key": "MODULE_2_AUTH", "name": "Universal Single Login & RBAC Engine", "subdomain": "auth", "category": "ACCESS", "status": "LIVE"},
    {"id": 3, "key": "MODULE_3_SYSTEM", "name": "Core System Engine & Multitenancy", "subdomain": "admin", "category": "CORE", "status": "LIVE"},
    {"id": 4, "key": "MODULE_4_DASHBOARD", "name": "Command Center & Dashboard Metrics", "subdomain": "admin", "category": "GOVERNANCE", "status": "LIVE"},
    {"id": 5, "key": "MODULE_5_CMS", "name": "Website CMS Foundation & Framework", "subdomain": "website", "category": "CMS", "status": "LIVE"},
    {"id": 6, "key": "MODULE_6_SIMS", "name": "Student Information Management (SIMS)", "subdomain": "student", "category": "ACADEMIC", "status": "LIVE"},
    {"id": 7, "key": "MODULE_7_ADMISSIONS", "name": "Admissions CRM & Counseling Pipeline", "subdomain": "admission", "category": "ADMISSIONS", "status": "LIVE"},
    {"id": 8, "key": "MODULE_8_ACADEMICS", "name": "Academic Engine & Timetable Planner", "subdomain": "academic", "category": "ACADEMIC", "status": "LIVE"},
    {"id": 9, "key": "MODULE_9_FEES", "name": "Fee Collection, Invoices & Finance", "subdomain": "fees", "category": "FINANCE", "status": "LIVE"},
    {"id": 10, "key": "MODULE_10_ATTENDANCE", "name": "Attendance & Leave Management", "subdomain": "attendance", "category": "OPERATIONS", "status": "LIVE"},
    {"id": 11, "key": "MODULE_11_EXAMINATIONS", "name": "Examinations & SGPA/CGPA Grading", "subdomain": "exam", "category": "EXAMINATION", "status": "LIVE"},
    {"id": 12, "key": "MODULE_12_CBT", "name": "Computer Based Testing (CBT) Platform", "subdomain": "cbt", "category": "EXAMINATION", "status": "LIVE"},
    {"id": 13, "key": "MODULE_13_CERTIFICATES", "name": "Tamper-Proof Certificates & QR Verification", "subdomain": "certificate", "category": "ACADEMIC", "status": "LIVE"},
    {"id": 14, "key": "MODULE_14_LIBRARY", "name": "Contact & Helpdesk Inquiry CMS", "subdomain": "website", "category": "CMS", "status": "LIVE"},
    {"id": 15, "key": "MODULE_15_LXP", "name": "Global Site Search & Megamenu Engine", "subdomain": "website", "category": "CMS", "status": "LIVE"},
    {"id": 16, "key": "MODULE_16_COMMUNICATION", "name": "Future API & Third-Party Integrations", "subdomain": "integration", "category": "PLATFORM", "status": "LIVE"},
    {"id": 17, "key": "MODULE_17_CRM", "name": "Enterprise CRM & Regional Franchise Centers", "subdomain": "crm", "category": "MARKETING", "status": "LIVE"},
    {"id": 18, "key": "MODULE_18_BI", "name": "Executive Reports, BI & NIRF Dossier", "subdomain": "bi", "category": "ANALYTICS", "status": "LIVE"},
    {"id": 19, "key": "MODULE_19_PLATFORM", "name": "Platform Administration, Backups & DevOps", "subdomain": "devops", "category": "PLATFORM", "status": "LIVE"},
    {"id": 20, "key": "MODULE_20_EXPERIENCE", "name": "Enterprise Experience Platform & Portals", "subdomain": "experience", "category": "EXPERIENCE", "status": "LIVE"}
]

@experience_router.get("/health")
async def experience_health():
    return {
        "status": "healthy",
        "module": "Module 20: Enterprise Experience Platform & Unified Portals (Final Milestone)",
        "campus": "MEI-HQ Indore",
        "total_portals_provisioned": len(_PORTALS_STORE),
        "erp_blueprint_completion": "20 / 20 MODULES COMPLETED",
        "lockdown_status": _ROOT_STATE["emergency_lockdown_active"]
    }

@experience_router.get("/root-owner/overview")
async def get_root_owner_overview():
    return _ROOT_STATE

@experience_router.post("/root-owner/lockdown")
async def toggle_root_lockdown(payload: Dict[str, Any] = {}):
    active = payload.get("active", not _ROOT_STATE["emergency_lockdown_active"])
    _ROOT_STATE["emergency_lockdown_active"] = active
    return {
        "status": "SUCCESS",
        "emergency_lockdown_active": active,
        "message": "Emergency campus platform lockdown toggled." if active else "Normal campus operations restored."
    }

@experience_router.get("/portals")
async def list_available_portals():
    return _PORTALS_STORE

@experience_router.get("/portals/{portal_type}/profile")
async def get_portal_profile(portal_type: str):
    portal = next((p for p in _PORTALS_STORE if p["portal_type"].upper() == portal_type.upper()), None)
    if not portal:
        raise HTTPException(status_code=404, detail="Portal type not found")
    return {
        "portal": portal,
        "user_preference": {
            "dark_mode": False,
            "accent_color": portal["accent_color"],
            "sidebar_collapsed": False,
            "notifications_enabled": True,
        },
        "allowed_subsystems": [m["name"] for m in ERP_MASTER_MODULES]
    }

@experience_router.get("/notifications")
async def list_notifications():
    return _NOTIFICATIONS_STORE

@experience_router.post("/notifications/broadcast", status_code=status.HTTP_201_CREATED)
async def broadcast_notification(payload: Dict[str, Any]):
    new_notif = {
        "id": f"notif_{uuid.uuid4().hex[:6]}",
        "title": payload.get("title", "Campus Announcement"),
        "category": payload.get("category", "GENERAL"),
        "message": payload.get("message", "System announcement dispatched across all active portals."),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "priority": payload.get("priority", "HIGH"),
        "is_read": False
    }
    _NOTIFICATIONS_STORE.insert(0, new_notif)
    return new_notif

@experience_router.get("/modules/registry")
async def get_full_erp_modules_registry():
    return {
        "total_modules": len(ERP_MASTER_MODULES),
        "completion_percentage": 100.0,
        "blueprint": "MY EDUCATION INDIA Autonomous Campus Flagship Blueprint",
        "modules": ERP_MASTER_MODULES
    }
