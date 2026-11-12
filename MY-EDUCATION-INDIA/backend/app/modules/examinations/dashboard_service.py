"""
EMSDashboardService module
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


class EMSDashboardService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def get_role_dashboard(self, *args: Any, **kwargs: Any) -> Any:
        return {}
