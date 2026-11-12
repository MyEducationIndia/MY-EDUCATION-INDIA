"""
LmsDashboardService module
"""
from typing import Any, Dict, List, Optional


class LmsDashboardService:
    ROLES = ["ROOT_OWNER", "SUPER_ADMIN", "LMS_ADMIN", "PRINCIPAL", "HOD", "FACULTY", "STUDENT", "PARENT", "FRANCHISE_CENTER"]

    @staticmethod
    async def get_role_dashboard(*args: Any, **kwargs: Any) -> Any:
        return {}
