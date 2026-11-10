from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.system.models import SystemSetting

SETTING_CATEGORIES: List[str] = [
    "general",
    "institute",
    "authentication",
    "communication",
    "website",
    "appearance",
    "security",
    "backup",
    "academic",
    "financial",
    "examination",
    "certificates",
    "attendance",
    "fees",
    "admissions",
    "library",
    "hostel",
    "transport",
    "inventory",
    "lms",
    "api",
    "developer",
]


class DynamicSettingsEngine:
    """Resolves dynamic configurations directly from PostgreSQL."""

    @staticmethod
    async def get_settings_by_category(
        session: AsyncSession,
        category: str,
        institute_id: Optional[uuid.UUID] = None,
    ) -> Dict[str, Any]:
        stmt = select(SystemSetting).where(SystemSetting.category == category)
        if institute_id:
            stmt = stmt.where((SystemSetting.institute_id == institute_id) | (SystemSetting.institute_id.is_(None)))
        else:
            stmt = stmt.where(SystemSetting.institute_id.is_(None))

        res = await session.execute(stmt)
        result_map: Dict[str, Any] = {}
        for row in res.scalars().all():
            result_map[row.key] = row.value
        return result_map

    @staticmethod
    async def get_single_setting(
        session: AsyncSession,
        category: str,
        key: str,
        institute_id: Optional[uuid.UUID] = None,
    ) -> Optional[Dict[str, Any]]:
        stmt = select(SystemSetting).where(
            SystemSetting.category == category,
            SystemSetting.key == key,
            SystemSetting.institute_id == institute_id,
        )
        res = await session.execute(stmt)
        row = res.scalar_one_or_none()
        return row.value if row else None
