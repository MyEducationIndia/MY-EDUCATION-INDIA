import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.modules.system.models import (
    AcademicYear,
    Branch,
    FinancialYear,
    Holiday,
    NumberGenerator,
    OrganizationSetting,
    SystemSetting,
    WorkingDay,
)
from app.modules.system.number_generator import UniversalNumberGeneratorService
from app.modules.system.repository import SystemRepository
from app.modules.system.schemas import (
    AcademicYearCreate,
    AcademicYearUpdate,
    BranchCreate,
    BranchUpdate,
    FinancialYearCreate,
    FinancialYearUpdate,
    HolidayCreate,
    NumberGenerateRequest,
    NumberGeneratorCreate,
    NumberGeneratorUpdate,
    NumberPreviewRequest,
    OrganizationSettingsUpdate,
    SettingSaveRequest,
    WorkingDaysBatchUpdate,
)
from app.modules.system.validators import validate_date_range, validate_format_template


class CoreSystemService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = SystemRepository(session)

    # ==================== Branch Management ====================
    async def create_branch(self, payload: BranchCreate) -> Branch:
        institute = await self.repo.get_institute_by_id(payload.institute_id)
        if not institute:
            raise ResourceNotFoundException("Institute", payload.institute_id)

        branch = Branch(**payload.model_dump())
        created = await self.repo.create_branch(branch)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update_branch(self, branch_id: uuid.UUID, payload: BranchUpdate) -> Branch:
        branch = await self.repo.get_branch_by_id(branch_id)
        if not branch:
            raise ResourceNotFoundException("Branch", branch_id)

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(branch, k, v)

        await self.session.commit()
        await self.session.refresh(branch)
        return branch

    # ==================== Academic & Financial Years ====================
    async def create_academic_year(self, payload: AcademicYearCreate) -> AcademicYear:
        validate_date_range(payload.start_date, payload.end_date)
        if payload.is_current:
            # Unset existing current year for this institute
            existing = await self.repo.list_academic_years(payload.institute_id)
            for y in existing:
                if y.is_current:
                    y.is_current = False

        ay = AcademicYear(**payload.model_dump())
        created = await self.repo.create_academic_year(ay)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def switch_current_academic_year(self, ay_id: uuid.UUID) -> AcademicYear:
        target = await self.repo.get_academic_year_by_id(ay_id)
        if not target:
            raise ResourceNotFoundException("AcademicYear", ay_id)

        existing = await self.repo.list_academic_years(target.institute_id)
        for y in existing:
            y.is_current = (y.id == target.id)

        await self.session.commit()
        await self.session.refresh(target)
        return target

    async def create_financial_year(self, payload: FinancialYearCreate) -> FinancialYear:
        validate_date_range(payload.start_date, payload.end_date)
        if payload.is_current:
            existing = await self.repo.list_financial_years(payload.institute_id)
            for y in existing:
                if y.is_current:
                    y.is_current = False

        fy = FinancialYear(**payload.model_dump())
        created = await self.repo.create_financial_year(fy)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def switch_current_financial_year(self, fy_id: uuid.UUID) -> FinancialYear:
        target = await self.repo.get_financial_year_by_id(fy_id)
        if not target:
            raise ResourceNotFoundException("FinancialYear", fy_id)

        existing = await self.repo.list_financial_years(target.institute_id)
        for y in existing:
            y.is_current = (y.id == target.id)

        await self.session.commit()
        await self.session.refresh(target)
        return target

    # ==================== Universal Number Generator ====================
    async def create_number_generator(self, payload: NumberGeneratorCreate) -> NumberGenerator:
        validate_format_template(payload.format_template)
        existing = await self.repo.get_generator_by_entity(payload.entity_type, payload.institute_id)
        if existing:
            raise ConflictException(f"Number generator for '{payload.entity_type}' already exists in this institute.")

        gen = NumberGenerator(**payload.model_dump())
        created = await self.repo.create_number_generator(gen)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update_number_generator(self, gen_id: uuid.UUID, payload: NumberGeneratorUpdate) -> NumberGenerator:
        gen = await self.repo.get_number_generator(gen_id)
        if not gen:
            raise ResourceNotFoundException("NumberGenerator", gen_id)

        if payload.format_template:
            validate_format_template(payload.format_template)

        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(gen, k, v)

        await self.session.commit()
        await self.session.refresh(gen)
        return gen

    async def generate_next_number(self, payload: NumberGenerateRequest) -> str:
        gen = await self.repo.get_generator_by_entity(payload.entity_type, payload.institute_id)
        if not gen:
            raise ResourceNotFoundException("Active NumberGenerator", f"{payload.entity_type}:{payload.institute_id}")

        inst = await self.repo.get_institute_by_id(payload.institute_id)
        institute_code = inst.code if inst else "MEI"

        number = await UniversalNumberGeneratorService.generate_next_number(
            session=self.session,
            generator=gen,
            institute_code=institute_code,
            branch_code=payload.branch_code,
            course_code=payload.course_code,
            dept_code=payload.dept_code,
            academic_year_code=payload.academic_year_code,
            financial_year_code=payload.financial_year_code,
        )
        await self.session.commit()
        return number

    # ==================== Holidays & Working Days ====================
    async def create_holiday(self, payload: HolidayCreate) -> Holiday:
        holiday = Holiday(**payload.model_dump())
        created = await self.repo.create_holiday(holiday)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def configure_working_days(self, payload: WorkingDaysBatchUpdate) -> List[WorkingDay]:
        existing = await self.repo.list_working_days(payload.institute_id, payload.branch_id)
        existing_map = {d.day_of_week: d for d in existing}

        result_days = []
        for item in payload.days:
            if item.day_of_week in existing_map:
                record = existing_map[item.day_of_week]
                record.is_working_day = item.is_working_day
                record.start_time = item.start_time
                record.end_time = item.end_time
            else:
                record = WorkingDay(
                    institute_id=payload.institute_id,
                    branch_id=payload.branch_id,
                    day_of_week=item.day_of_week,
                    day_name=item.day_name,
                    is_working_day=item.is_working_day,
                    start_time=item.start_time,
                    end_time=item.end_time,
                )
                self.session.add(record)
            result_days.append(record)

        await self.session.commit()
        return result_days

    # ==================== Dynamic Settings ====================
    async def save_system_setting(self, payload: SettingSaveRequest) -> SystemSetting:
        stmt = (
            SystemSetting.category == payload.category,
            SystemSetting.key == payload.key,
            SystemSetting.institute_id == payload.institute_id,
        )
        existing_list = await self.repo.list_settings_by_category(payload.category, payload.institute_id)
        matched = next((s for s in existing_list if s.key == payload.key), None)

        if matched:
            matched.value = payload.value
            matched.description = payload.description
            matched.is_public = payload.is_public
            setting = matched
        else:
            setting = SystemSetting(**payload.model_dump())
            await self.repo.save_setting(setting)

        await self.session.commit()
        await self.session.refresh(setting)
        return setting

    async def update_org_settings(self, institute_id: uuid.UUID, payload: OrganizationSettingsUpdate) -> OrganizationSetting:
        org = await self.repo.get_org_settings(institute_id)
        if not org:
            org = OrganizationSetting(institute_id=institute_id, **payload.model_dump(exclude_unset=True))
            await self.repo.save_org_settings(org)
        else:
            for k, v in payload.model_dump(exclude_unset=True).items():
                setattr(org, k, v)

        await self.session.commit()
        await self.session.refresh(org)
        return org
