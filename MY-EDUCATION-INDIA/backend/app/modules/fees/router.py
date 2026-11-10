from datetime import date
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.modules.auth.dependencies import get_current_user, require_permissions
from app.modules.fees.analytics import FeeAnalyticsEngine
from app.modules.fees.reports import FinancialReportEngine
from app.modules.fees.schemas import (
    ConcessionApplyRequest,
    ConcessionResponse,
    DiscountCreate,
    DiscountResponse,
    FeeAnalyticsSummary,
    FeeCategoryCreate,
    FeeCategoryResponse,
    FeeHeadCreate,
    FeeHeadResponse,
    FeeStructureCreate,
    FeeStructureResponse,
    LateFeeRuleCreate,
    LateFeeRuleResponse,
    PaymentCreate,
    PaymentResponse,
    ReceiptResponse,
    RefundRequest,
    RefundResponse,
    ScholarshipCreate,
    ScholarshipResponse,
    StudentFeeAssignmentCreate,
    StudentFeeAssignmentResponse,
)
from app.modules.fees.service import FeeManagementService

fee_router = APIRouter(prefix="/fees", tags=["Enterprise Fee & Finance Management"])


# Categories & Heads
@fee_router.get("/categories", response_model=List[FeeCategoryResponse])
async def list_fee_categories(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[FeeCategoryResponse]:
    service = FeeManagementService(db)
    items = await service.list_categories(institute_id)
    return [FeeCategoryResponse.model_validate(it) for it in items]


@fee_router.post("/categories", response_model=FeeCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_fee_category(
    payload: FeeCategoryCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> FeeCategoryResponse:
    service = FeeManagementService(db)
    cat = await service.create_fee_category(payload)
    return FeeCategoryResponse.model_validate(cat)


@fee_router.get("/heads", response_model=List[FeeHeadResponse])
async def list_fee_heads(
    institute_id: uuid.UUID = Query(...),
    category_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[FeeHeadResponse]:
    service = FeeManagementService(db)
    items = await service.list_fee_heads(institute_id, category_id)
    return [FeeHeadResponse.model_validate(it) for it in items]


@fee_router.post("/heads", response_model=FeeHeadResponse, status_code=status.HTTP_201_CREATED)
async def create_fee_head(
    payload: FeeHeadCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> FeeHeadResponse:
    service = FeeManagementService(db)
    head = await service.create_fee_head(payload)
    return FeeHeadResponse.model_validate(head)


# Fee Structures
@fee_router.get("/structures", response_model=List[FeeStructureResponse])
async def list_fee_structures(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[FeeStructureResponse]:
    service = FeeManagementService(db)
    items = await service.list_fee_structures(institute_id)
    return [FeeStructureResponse.model_validate(it) for it in items]


@fee_router.post("/structures", response_model=FeeStructureResponse, status_code=status.HTTP_201_CREATED)
async def create_fee_structure(
    payload: FeeStructureCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> FeeStructureResponse:
    service = FeeManagementService(db)
    struct = await service.create_fee_structure(payload)
    return FeeStructureResponse.model_validate(struct)


# Fee Assignments
@fee_router.post("/assignments", response_model=StudentFeeAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def assign_fee_to_student(
    payload: StudentFeeAssignmentCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> StudentFeeAssignmentResponse:
    service = FeeManagementService(db)
    assignment = await service.assign_fee_to_student(payload)
    return StudentFeeAssignmentResponse.model_validate(assignment)


# Collections & Payments
@fee_router.post("/collections", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def collect_fee_payment(
    payload: PaymentCreate,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("fees.collect")),
) -> PaymentResponse:
    service = FeeManagementService(db)
    user_id = getattr(user, "id", None)
    payment = await service.collect_payment(payload, user_id=user_id)
    return PaymentResponse.model_validate(payment)


# Receipts
@fee_router.get("/receipts/{payment_id}", response_model=ReceiptResponse)
async def get_payment_receipt(
    payment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ReceiptResponse:
    service = FeeManagementService(db)
    receipt = await service.repo.get_receipt_by_payment(payment_id)
    if not receipt:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Receipt not found for this payment.")
    return ReceiptResponse.model_validate(receipt)


# Concessions & Scholarships
@fee_router.post("/concessions/apply", response_model=ConcessionResponse, status_code=status.HTTP_201_CREATED)
async def apply_concession_or_scholarship(
    payload: ConcessionApplyRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> ConcessionResponse:
    service = FeeManagementService(db)
    concession = await service.apply_concession(payload)
    return ConcessionResponse.model_validate(concession)


@fee_router.get("/scholarships", response_model=List[ScholarshipResponse])
async def list_scholarships(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ScholarshipResponse]:
    service = FeeManagementService(db)
    items = await service.list_scholarships(institute_id)
    return [ScholarshipResponse.model_validate(it) for it in items]


@fee_router.post("/scholarships", response_model=ScholarshipResponse, status_code=status.HTTP_201_CREATED)
async def create_scholarship(
    payload: ScholarshipCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> ScholarshipResponse:
    service = FeeManagementService(db)
    item = await service.create_scholarship(payload)
    return ScholarshipResponse.model_validate(item)


@fee_router.get("/discounts", response_model=List[DiscountResponse])
async def list_discounts(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[DiscountResponse]:
    service = FeeManagementService(db)
    items = await service.list_discounts(institute_id)
    return [DiscountResponse.model_validate(it) for it in items]


@fee_router.post("/discounts", response_model=DiscountResponse, status_code=status.HTTP_201_CREATED)
async def create_discount(
    payload: DiscountCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> DiscountResponse:
    service = FeeManagementService(db)
    item = await service.create_discount(payload)
    return DiscountResponse.model_validate(item)


# Late Fee Rules
@fee_router.get("/late-fees", response_model=List[LateFeeRuleResponse])
async def list_late_fee_rules(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[LateFeeRuleResponse]:
    service = FeeManagementService(db)
    items = await service.list_late_fee_rules(institute_id)
    return [LateFeeRuleResponse.model_validate(it) for it in items]


@fee_router.post("/late-fees", response_model=LateFeeRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_late_fee_rule(
    payload: LateFeeRuleCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.manage")),
) -> LateFeeRuleResponse:
    service = FeeManagementService(db)
    item = await service.create_late_fee_rule(payload)
    return LateFeeRuleResponse.model_validate(item)


# Refunds
@fee_router.post("/refunds", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
async def process_refund(
    payload: RefundRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("fees.refund")),
) -> RefundResponse:
    service = FeeManagementService(db)
    user_id = getattr(user, "id", None)
    refund = await service.process_refund(payload, user_id=user_id)
    return RefundResponse.model_validate(refund)


# Financial Reports & Analytics
@fee_router.get("/reports/daily-collection")
async def get_daily_collection_report(
    institute_id: uuid.UUID = Query(...),
    report_date: date = Query(default=date.today()),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.reports")),
) -> Dict[str, Any]:
    return await FinancialReportEngine.get_daily_collection_report(db, institute_id, report_date)


@fee_router.get("/reports/outstanding")
async def get_outstanding_dues_report(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.reports")),
) -> Dict[str, Any]:
    return await FinancialReportEngine.get_outstanding_dues_report(db, institute_id)


@fee_router.get("/analytics", response_model=FeeAnalyticsSummary)
async def get_fee_analytics(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("fees.analytics")),
) -> FeeAnalyticsSummary:
    summary = await FeeAnalyticsEngine.get_dashboard_summary(db, institute_id)
    return FeeAnalyticsSummary.model_validate(summary)
