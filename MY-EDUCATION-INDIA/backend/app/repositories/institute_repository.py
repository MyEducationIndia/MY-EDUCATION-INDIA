import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.academic_session import AcademicSession
from app.models.institute import Institute
from app.models.module_config import SystemModuleConfig


class InstituteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, institute_id: uuid.UUID) -> Institute | None:
        stmt = (
            select(Institute)
            .options(
                selectinload(Institute.module_configs),
                selectinload(Institute.academic_sessions),
            )
            .where(Institute.id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Institute | None:
        stmt = (
            select(Institute)
            .options(
                selectinload(Institute.module_configs),
                selectinload(Institute.academic_sessions),
            )
            .where(Institute.code == code.upper())
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_all(self) -> List[Institute]:
        stmt = (
            select(Institute)
            .options(
                selectinload(Institute.module_configs),
                selectinload(Institute.academic_sessions),
            )
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

    async def get_academic_session_by_id(self, session_id: uuid.UUID) -> AcademicSession | None:
        stmt = select(AcademicSession).where(AcademicSession.id == session_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_academic_session_by_code(
        self, institute_id: uuid.UUID, session_code: str
    ) -> AcademicSession | None:
        stmt = select(AcademicSession).where(
            AcademicSession.institute_id == institute_id,
            AcademicSession.session_code == session_code.upper(),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_academic_sessions(self, institute_id: uuid.UUID) -> List[AcademicSession]:
        stmt = (
            select(AcademicSession)
            .where(AcademicSession.institute_id == institute_id)
            .order_by(AcademicSession.start_date.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_academic_session(self, session: AcademicSession) -> AcademicSession:
        self.session.add(session)
        await self.session.flush()
        return session

    async def delete_academic_session(self, session: AcademicSession) -> None:
        await self.session.delete(session)
        await self.session.flush()
