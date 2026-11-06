import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig


class InstituteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, institute_id: uuid.UUID) -> Institute | None:
        stmt = (
            select(Institute)
            .options(selectinload(Institute.module_configs))
            .where(Institute.id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Institute | None:
        stmt = (
            select(Institute)
            .options(selectinload(Institute.module_configs))
            .where(Institute.code == code.upper())
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_all(self) -> List[Institute]:
        stmt = (
            select(Institute)
            .options(selectinload(Institute.module_configs))
            .order_by(Institute.created_at.asc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create(self, institute: Institute) -> Institute:
        self.session.add(institute)
        await self.session.flush()
        return institute

    async def get_module_config(
        self, institute_id: uuid.UUID, module_key: str
    ) -> SystemModuleConfig | None:
        stmt = select(SystemModuleConfig).where(
            SystemModuleConfig.institute_id == institute_id,
            SystemModuleConfig.module_key == module_key,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
