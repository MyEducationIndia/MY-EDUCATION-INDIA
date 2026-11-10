import uuid
from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.system.models import (
    AcademicYear,
    Branch,
    Currency,
    FinancialYear,
    Holiday,
    Institute,
    Language,
    NumberGenerator,
    NumberSequence,
    OrganizationSetting,
    SystemSetting,
    Theme,
    Timezone,
    WorkingDay,
)


class SystemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================== Institutes & Branches ====================
    async def get_institute_by_id(self, institute_id: uuid.UUID) -> Optional[Institute]:
        stmt = (
            select(Institute)
            .options(
                selectinload(Institute.branches),
                selectinload(Institute.academic_years),
                selectinload(Institute.financial_years),
            )
            .where(Institute.id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_institutes(self) -> List[Institute]:
        stmt = (
            select(Institute)
            .options(selectinload(Institute.branches))
            .order_by(Institute.name.asc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_branch_by_id(self, branch_id: uuid.UUID) -> Optional[Branch]:
        stmt = select(Branch).where(Branch.id == branch_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_branches(self, institute_id: uuid.UUID) -> List[Branch]:
        stmt = select(Branch).where(Branch.institute_id == institute_id).order_by(Branch.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_branch(self, branch: Branch) -> Branch:
        self.session.add(branch)
        await self.session.flush()
        return branch

    # ==================== Academic & Financial Years ====================
    async def list_academic_years(self, institute_id: uuid.UUID) -> List[AcademicYear]:
        stmt = (
            select(AcademicYear)
            .where(AcademicYear.institute_id == institute_id)
            .order_by(AcademicYear.start_date.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_academic_year_by_id(self, ay_id: uuid.UUID) -> Optional[AcademicYear]:
        stmt = select(AcademicYear).where(AcademicYear.id == ay_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_academic_year(self, ay: AcademicYear) -> AcademicYear:
        self.session.add(ay)
        await self.session.flush()
        return ay

    async def list_financial_years(self, institute_id: uuid.UUID) -> List[FinancialYear]:
        stmt = (
            select(FinancialYear)
            .where(FinancialYear.institute_id == institute_id)
            .order_by(FinancialYear.start_date.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_financial_year_by_id(self, fy_id: uuid.UUID) -> Optional[FinancialYear]:
        stmt = select(FinancialYear).where(FinancialYear.id == fy_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_financial_year(self, fy: FinancialYear) -> FinancialYear:
        self.session.add(fy)
        await self.session.flush()
        return fy

    # ==================== Universal Number Generators ====================
    async def list_number_generators(self, institute_id: uuid.UUID) -> List[NumberGenerator]:
        stmt = (
            select(NumberGenerator)
            .options(selectinload(NumberGenerator.sequences))
            .where(NumberGenerator.institute_id == institute_id)
            .order_by(NumberGenerator.entity_type.asc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_number_generator(self, gen_id: uuid.UUID) -> Optional[NumberGenerator]:
        stmt = select(NumberGenerator).options(selectinload(NumberGenerator.sequences)).where(NumberGenerator.id == gen_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_generator_by_entity(self, entity_type: str, institute_id: uuid.UUID) -> Optional[NumberGenerator]:
        stmt = (
            select(NumberGenerator)
            .options(selectinload(NumberGenerator.sequences))
            .where(
                NumberGenerator.entity_type == entity_type,
                NumberGenerator.institute_id == institute_id,
                NumberGenerator.is_active.is_(True),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_number_generator(self, gen: NumberGenerator) -> NumberGenerator:
        self.session.add(gen)
        await self.session.flush()
        return gen

    # ==================== Holidays & Working Days ====================
    async def list_holidays(self, institute_id: uuid.UUID, branch_id: Optional[uuid.UUID] = None) -> List[Holiday]:
        stmt = select(Holiday).where(Holiday.institute_id == institute_id)
        if branch_id:
            stmt = stmt.where((Holiday.branch_id == branch_id) | (Holiday.branch_id.is_(None)))
        stmt = stmt.order_by(Holiday.holiday_date.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_holiday(self, holiday: Holiday) -> Holiday:
        self.session.add(holiday)
        await self.session.flush()
        return holiday

    async def list_working_days(self, institute_id: uuid.UUID, branch_id: Optional[uuid.UUID] = None) -> List[WorkingDay]:
        stmt = select(WorkingDay).where(WorkingDay.institute_id == institute_id)
        if branch_id:
            stmt = stmt.where(WorkingDay.branch_id == branch_id)
        stmt = stmt.order_by(WorkingDay.day_of_week.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Settings & Organization ====================
    async def get_org_settings(self, institute_id: uuid.UUID) -> Optional[OrganizationSetting]:
        stmt = select(OrganizationSetting).where(OrganizationSetting.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def save_org_settings(self, org_settings: OrganizationSetting) -> OrganizationSetting:
        self.session.add(org_settings)
        await self.session.flush()
        return org_settings

    async def list_settings_by_category(self, category: str, institute_id: Optional[uuid.UUID]) -> List[SystemSetting]:
        stmt = select(SystemSetting).where(SystemSetting.category == category)
        if institute_id:
            stmt = stmt.where(SystemSetting.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_setting(self, setting: SystemSetting) -> SystemSetting:
        self.session.add(setting)
        await self.session.flush()
        return setting
