from typing import Dict, Any, List

# Standard Enterprise User Types / System Roles
DEFAULT_SYSTEM_ROLES: List[Dict[str, Any]] = [
    {"code": "SUPER_ADMIN", "name": "Super Admin", "description": "Unrestricted administrative access to entire platform", "portal_subdomain": "admin", "is_system_role": True},
    {"code": "INSTITUTE_ADMIN", "name": "Institute Admin", "description": "Full administrative access within specific institute", "portal_subdomain": "admin", "is_system_role": True},
    {"code": "BRANCH_ADMIN", "name": "Branch Admin", "description": "Administrative authority over specific institute branch", "portal_subdomain": "admin", "is_system_role": True},
    {"code": "RECEPTION", "name": "Reception", "description": "Front desk, visitor logs, and initial admission queries", "portal_subdomain": "admin", "is_system_role": True},
    {"code": "FACULTY", "name": "Faculty", "description": "Teacher and instructor academic portal access", "portal_subdomain": "teacher", "is_system_role": True},
    {"code": "ACCOUNTANT", "name": "Accountant", "description": "Fee collection, receipts, and finance ledger management", "portal_subdomain": "fees", "is_system_role": True},
    {"code": "EXAM_CONTROLLER", "name": "Exam Controller", "description": "Examination setup, CBT scheduling, and result publishing", "portal_subdomain": "exam", "is_system_role": True},
    {"code": "LIBRARY_STAFF", "name": "Library Staff", "description": "Book cataloging, issue/return circulation, and fines", "portal_subdomain": "library", "is_system_role": True},
    {"code": "HOSTEL_WARDEN", "name": "Hostel Warden", "description": "Hostel room allocation and dormitory warden governance", "portal_subdomain": "admin", "is_system_role": True},
    {"code": "TRANSPORT_MANAGER", "name": "Transport Manager", "description": "Fleet routes, buses, and transport pass allocations", "portal_subdomain": "admin", "is_system_role": True},
    {"code": "STUDENT", "name": "Student", "description": "Student LMS, attendance, homework, and CBT testing portal", "portal_subdomain": "student", "is_system_role": True},
    {"code": "PARENT", "name": "Parent", "description": "Parental monitoring, report cards, and fee payments", "portal_subdomain": "parent", "is_system_role": True},
    {"code": "GUEST", "name": "Guest", "description": "Prospective applicants and public inquiry guest access", "portal_subdomain": "website", "is_system_role": True},
]

# Standard Fine-grained Enterprise Permissions
DEFAULT_ENTERPRISE_PERMISSIONS: List[Dict[str, str]] = [
    # Student Module
    {"code": "student.view", "name": "View Student Records", "module_key": "student_management"},
    {"code": "student.create", "name": "Create Student Record", "module_key": "student_management"},
    {"code": "student.edit", "name": "Edit Student Record", "module_key": "student_management"},
    {"code": "student.delete", "name": "Delete Student Record", "module_key": "student_management"},
    # Fees Module
    {"code": "fees.manage", "name": "Manage Fees and Collections", "module_key": "fees"},
    {"code": "fees.view", "name": "View Fee Records and Receipts", "module_key": "fees"},
    # Attendance Module
    {"code": "attendance.manage", "name": "Manage Daily and Biometric Attendance", "module_key": "attendance"},
    {"code": "attendance.view", "name": "View Attendance Records", "module_key": "attendance"},
    # Examination & CBT
    {"code": "exam.manage", "name": "Manage Exams and Question Banks", "module_key": "exam_management"},
    {"code": "exam.view", "name": "View Exam Schedules and Marks", "module_key": "exam_management"},
    {"code": "cbt.take", "name": "Access and Submit CBT Tests", "module_key": "online_cbt"},
    # CMS & Communication
    {"code": "cms.manage", "name": "Manage Website CMS and Media", "module_key": "website_cms"},
    {"code": "communication.manage", "name": "Manage SMS, WhatsApp and Email Broadcasts", "module_key": "communication"},
    # Settings & Administration
    {"code": "settings.manage", "name": "Manage System and Auth Configuration", "module_key": "settings"},
    {"code": "backup.manage", "name": "Perform Database Backups", "module_key": "backup"},
    {"code": "restore.manage", "name": "Restore Database Archive", "module_key": "restore"},
    {"code": "reports.export", "name": "Export Comprehensive Institutional Reports", "module_key": "reports"},
    {"code": "audit.view", "name": "View Security Audit Trail and Login History", "module_key": "audit_logs"},
    {"code": "users.manage", "name": "Manage Users, Roles, and Sessions", "module_key": "role_management"},
]

# Supported Login Identifier Criteria (Configurable per institute/system)
VALID_LOGIN_CRITERIA = {
    "username",
    "email",
    "registration_number",
    "enrollment_number",
    "roll_number",
    "mobile_number",
    "erp_id",
    "student_id",
    "custom_field",
}

DEFAULT_AUTH_SETTINGS = {
    "login_criteria": ["email", "username", "mobile_number", "registration_number", "enrollment_number", "roll_number", "erp_id", "student_id"],
    "primary_login_field": "identifier",
    "password_min_length": 10,
    "password_require_uppercase": True,
    "password_require_lowercase": True,
    "password_require_number": True,
    "password_require_special": True,
    "password_expiry_days": 90,
    "password_history_limit": 5,
    "max_failed_attempts": 5,
    "lockout_duration_minutes": 15,
    "access_token_expire_minutes": 15,
    "refresh_token_expire_days": 7,
    "session_timeout_minutes": 60,
    "remember_me_refresh_days": 30,
    "enable_email_verification": True,
    "allow_remember_me": True,
}
