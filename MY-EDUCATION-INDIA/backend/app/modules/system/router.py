import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.modules.auth.dependencies import enforce_csrf, get_current_user, require_permissions
from app.modules.auth.models import User
from app.modules.system.number_generator import UniversalNumberGeneratorService
from app.modules.system.schemas import (
    AcademicYearCreate,
    AcademicYearResponse,
    AcademicYearUpdate,
    BranchCreate,
    BranchResponse,
    BranchUpdate,
    FinancialYearCreate,
    FinancialYearResponse,
    FinancialYearUpdate,
    HolidayCreate,
    HolidayResponse,
    NumberGenerateRequest,
    NumberGeneratorCreate,
    NumberGeneratorResponse,
    NumberGeneratorUpdate,
    NumberPreviewRequest,
    OrganizationSettingsResponse,
    OrganizationSettingsUpdate,
    SettingResponse,
    SettingSaveRequest,
    WorkingDayResponse,
    WorkingDaysBatchUpdate,
)
from app.modules.system.service import CoreSystemService
from app.schemas.institute import InstituteResponse

system_router = APIRouter(prefix="/system", tags=["Core System Engine"])


# ==================== Institutes & Branches ====================
@system_router.get("/institutes", response_model=List[InstituteResponse])
async def list_institutes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[InstituteResponse]:
    service = CoreSystemService(db)
    institutes = await service.repo.list_institutes()
    return [InstituteResponse.model_validate(i) for i in institutes]


@system_router.get("/branches", response_model=List[BranchResponse])
async def list_branches(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[BranchResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        return []
    branches = await service.repo.list_branches(eff_inst)
    return [BranchResponse.model_validate(b) for b in branches]


@system_router.post("/branches", response_model=BranchResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_branch(
    payload: BranchCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> BranchResponse:
    service = CoreSystemService(db)
    branch = await service.create_branch(payload)
    return BranchResponse.model_validate(branch)


@system_router.patch("/branches/{branch_id}", response_model=BranchResponse, dependencies=[Depends(enforce_csrf)])
async def update_branch(
    branch_id: uuid.UUID,
    payload: BranchUpdate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> BranchResponse:
    service = CoreSystemService(db)
    branch = await service.update_branch(branch_id, payload)
    return BranchResponse.model_validate(branch)


# ==================== Academic Years ====================
@system_router.get("/academic-years", response_model=List[AcademicYearResponse])
async def list_academic_years(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[AcademicYearResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        return []
    years = await service.repo.list_academic_years(eff_inst)
    return [AcademicYearResponse.model_validate(y) for y in years]


@system_router.post("/academic-years", response_model=AcademicYearResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_academic_year(
    payload: AcademicYearCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> AcademicYearResponse:
    service = CoreSystemService(db)
    ay = await service.create_academic_year(payload)
    return AcademicYearResponse.model_validate(ay)


@system_router.post("/academic-years/{ay_id}/set-current", response_model=AcademicYearResponse, dependencies=[Depends(enforce_csrf)])
async def switch_academic_year(
    ay_id: uuid.UUID,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> AcademicYearResponse:
    service = CoreSystemService(db)
    ay = await service.switch_current_academic_year(ay_id)
    return AcademicYearResponse.model_validate(ay)


# ==================== Financial Years ====================
@system_router.get("/financial-years", response_model=List[FinancialYearResponse])
async def list_financial_years(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[FinancialYearResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        return []
    years = await service.repo.list_financial_years(eff_inst)
    return [FinancialYearResponse.model_validate(y) for y in years]


@system_router.post("/financial-years", response_model=FinancialYearResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_financial_year(
    payload: FinancialYearCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> FinancialYearResponse:
    service = CoreSystemService(db)
    fy = await service.create_financial_year(payload)
    return FinancialYearResponse.model_validate(fy)


@system_router.post("/financial-years/{fy_id}/set-current", response_model=FinancialYearResponse, dependencies=[Depends(enforce_csrf)])
async def switch_financial_year(
    fy_id: uuid.UUID,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> FinancialYearResponse:
    service = CoreSystemService(db)
    fy = await service.switch_current_financial_year(fy_id)
    return FinancialYearResponse.model_validate(fy)


# ==================== Universal Number Generator ====================
@system_router.get("/number-generator", response_model=List[NumberGeneratorResponse])
async def list_number_generators(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[NumberGeneratorResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        return []
    gens = await service.repo.list_number_generators(eff_inst)
    return [NumberGeneratorResponse.model_validate(g) for g in gens]


@system_router.post("/number-generator", response_model=NumberGeneratorResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_number_generator(
    payload: NumberGeneratorCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> NumberGeneratorResponse:
    service = CoreSystemService(db)
    gen = await service.create_number_generator(payload)
    return NumberGeneratorResponse.model_validate(gen)


@system_router.patch("/number-generator/{gen_id}", response_model=NumberGeneratorResponse, dependencies=[Depends(enforce_csrf)])
async def update_number_generator(
    gen_id: uuid.UUID,
    payload: NumberGeneratorUpdate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> NumberGeneratorResponse:
    service = CoreSystemService(db)
    gen = await service.update_number_generator(gen_id, payload)
    return NumberGeneratorResponse.model_validate(gen)


@system_router.post("/number-generator/preview", response_model=Dict[str, str])
async def preview_number_generation(payload: NumberPreviewRequest) -> Dict[str, str]:
    preview = UniversalNumberGeneratorService.render_preview(
        format_template=payload.format_template,
        prefix=payload.prefix,
        suffix=payload.suffix,
        separator=payload.separator,
        padding_length=payload.padding_length,
        sample_number=payload.sample_number,
        institute_code=payload.institute_code or "MEI",
        branch_code=payload.branch_code or "BPL",
        course_code=payload.course_code or "BTECH",
        dept_code=payload.dept_code or "CSE",
        year=payload.year or 2027,
        month=payload.month or 6,
    )
    return {"preview": preview}


@system_router.post("/number-generator/next", response_model=Dict[str, str], dependencies=[Depends(enforce_csrf)])
async def generate_next_number(
    payload: NumberGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, str]:
    service = CoreSystemService(db)
    number = await service.generate_next_number(payload)
    return {"number": number}


# ==================== Holidays & Working Days ====================
@system_router.get("/holidays", response_model=List[HolidayResponse])
async def list_holidays(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    branch_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[HolidayResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        return []
    holidays = await service.repo.list_holidays(eff_inst, branch_id)
    return [HolidayResponse.model_validate(h) for h in holidays]


@system_router.post("/holidays", response_model=HolidayResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_holiday(
    payload: HolidayCreate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> HolidayResponse:
    service = CoreSystemService(db)
    h = await service.create_holiday(payload)
    return HolidayResponse.model_validate(h)


@system_router.get("/working-days", response_model=List[WorkingDayResponse])
async def list_working_days(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    branch_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[WorkingDayResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        return []
    days = await service.repo.list_working_days(eff_inst, branch_id)
    return [WorkingDayResponse.model_validate(d) for d in days]


@system_router.put("/working-days", response_model=List[WorkingDayResponse], dependencies=[Depends(enforce_csrf)])
async def update_working_days(
    payload: WorkingDaysBatchUpdate,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> List[WorkingDayResponse]:
    service = CoreSystemService(db)
    days = await service.configure_working_days(payload)
    return [WorkingDayResponse.model_validate(d) for d in days]


# ==================== Dynamic Settings & Organization ====================
@system_router.get("/settings", response_model=List[SettingResponse])
async def get_system_settings_by_category(
    category: str = Query(..., min_length=2, max_length=64),
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[SettingResponse]:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    settings = await service.repo.list_settings_by_category(category, eff_inst)
    return [SettingResponse.model_validate(s) for s in settings]


@system_router.post("/settings", response_model=SettingResponse, dependencies=[Depends(enforce_csrf)])
async def save_system_setting(
    payload: SettingSaveRequest,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> SettingResponse:
    service = CoreSystemService(db)
    setting = await service.save_system_setting(payload)
    return SettingResponse.model_validate(setting)


@system_router.get("/organization", response_model=OrganizationSettingsResponse)
async def get_organization_settings(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> OrganizationSettingsResponse:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        raise ValueError("Institute ID required.")
    org = await service.repo.get_org_settings(eff_inst)
    if not org:
        org = await service.update_org_settings(eff_inst, OrganizationSettingsUpdate())
    return OrganizationSettingsResponse.model_validate(org)


@system_router.patch("/organization", response_model=OrganizationSettingsResponse, dependencies=[Depends(enforce_csrf)])
async def update_organization_settings(
    payload: OrganizationSettingsUpdate,
    institute_id: Optional[uuid.UUID] = Query(default=None),
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> OrganizationSettingsResponse:
    service = CoreSystemService(db)
    eff_inst = institute_id or current_user.institute_id
    if not eff_inst:
        raise ValueError("Institute ID required.")
    org = await service.update_org_settings(eff_inst, payload)
    return OrganizationSettingsResponse.model_validate(org)
