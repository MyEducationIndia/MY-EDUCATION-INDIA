from typing import List, Set
from app.modules.auth.models import User


class PermissionEngine:
    """Fine-grained RBAC and permission evaluation engine."""

    @staticmethod
    def get_effective_permissions(user: User) -> Set[str]:
        if user.is_super_admin:
            return {"*"}

        perms: Set[str] = set()
        for role in user.roles:
            for p in role.permissions:
                perms.add(p.code)
        return perms

    @staticmethod
    def has_permission(user: User, required_permission: str) -> bool:
        if user.is_super_admin:
            return True

        user_perms = PermissionEngine.get_effective_permissions(user)
        if "*" in user_perms:
            return True

        if required_permission in user_perms:
            return True

        # Wildcard scope evaluation (e.g. 'student.*' satisfies 'student.view')
        if "." in required_permission:
            module_wildcard = required_permission.split(".", 1)[0] + ".*"
            if module_wildcard in user_perms:
                return True

        return False

    @staticmethod
    def has_any_permission(user: User, required_permissions: List[str]) -> bool:
        return any(PermissionEngine.has_permission(user, p) for p in required_permissions)

    @staticmethod
    def has_all_permissions(user: User, required_permissions: List[str]) -> bool:
        return all(PermissionEngine.has_permission(user, p) for p in required_permissions)

    @staticmethod
    def has_role(user: User, role_code: str) -> bool:
        if user.is_super_admin:
            return True
        return any(r.code == role_code.upper() for r in user.roles)
