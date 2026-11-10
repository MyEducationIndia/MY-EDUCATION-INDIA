"""Module 20: Enterprise Portal Engine"""
PORTAL_ROLES_MAP = {
    "ROOT_OWNER": ["ROOT_OWNER"],
    "SUPER_ADMIN": ["SUPER_ADMIN"],
    "INSTITUTE_ADMIN": ["INSTITUTE_ADMIN"],
    "BRANCH_ADMIN": ["BRANCH_ADMIN"],
    "FACULTY": ["FACULTY", "PROFESSOR", "LECTURER", "DEAN"],
    "STUDENT": ["STUDENT", "SCHOLAR", "PUPIL"],
    "COUNSELLOR": ["COUNSELLOR", "ADMISSION_COUNSELLOR"],
    "ACCOUNTANT": ["ACCOUNTANT", "BURSAR", "FINANCE_OFFICER"],
    "RECEPTION": ["RECEPTIONIST", "FRONT_DESK"],
    "DEVELOPER": ["DEVELOPER", "SYSTEM_ARCHITECT"]
}

class EnterprisePortalEngine:
    @staticmethod
    def resolve_portal_for_role(role: str) -> str:
        r = role.upper().strip()
        for portal, roles in PORTAL_ROLES_MAP.items():
            if r in roles:
                return portal
        return "STUDENT"

    @staticmethod
    def can_access_portal(user_role: str, target_portal: str) -> bool:
        allowed = PORTAL_ROLES_MAP.get(target_portal.upper(), [])
        return user_role.upper() in allowed or user_role.upper() == "ROOT_OWNER"
