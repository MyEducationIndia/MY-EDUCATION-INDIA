import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.modules.admissions.models import Application, Lead
from app.modules.admissions.schemas import (
    AdmissionApproveRequest,
    AdmissionDashboardMetrics,
    AdmissionFeeCollectRequest,
    AdmissionRejectRequest,
    ApplicationCreateRequest,
    ApplicationResponse,
    DocumentVerifyRequest,
    LeadCreateRequest,
    LeadFollowupRequest,
    LeadResponse,
)
from app.modules.admissions.service import AdmissionService
from app.modules.admissions.workflow import AdmissionWorkflowEngine
from app.modules.auth.dependencies import enforce_csrf, get_current_user, require_permissions
from app.modules.auth.models import User

router = admission_router = APIRouter(prefix="/admissions", tags=["Enterprise Admission & CRM System"])


@admission_router.get("/dashboard", response_model=AdmissionDashboardMetrics)
async def get_admission_dashboard(
    current_user: User = Depends(require_permissions("admission.view")),
    db: AsyncSession = Depends(get_db_session),
) -> AdmissionDashboardMetrics:
    if not current_user.institute_id:
        return AdmissionDashboardMetrics(today_enquiries=0, admissions_today=0, pending_applications=0, verification_pending=0, waiting_list=0, total_leads=0, conversions_count=0, conversion_rate_pct=0.0, total_revenue_collected=0.0)
    service = AdmissionService(db)
    return await service.get_dashboard_metrics(current_user.institute_id)


# ==================== Leads CRM ====================
@admission_router.get("/leads", response_model=Dict[str, Any])
async def list_leads(
    priority: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(require_permissions("admission.view")),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    if not current_user.institute_id:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}
    service = AdmissionService(db)
    leads, total = await service.repo.list_leads_paginated(
        current_user.institute_id, priority, status, search, page, page_size
    )
    return {
        "items": [LeadResponse.model_validate(l).model_dump() for l in leads],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@admission_router.post("/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_lead(
    payload: LeadCreateRequest,
    current_user: User = Depends(require_permissions("admission.create")),
    db: AsyncSession = Depends(get_db_session),
) -> LeadResponse:
    service = AdmissionService(db)
    lead = await service.create_lead(payload)
    return LeadResponse.model_validate(lead)


@admission_router.post("/leads/{lead_id}/followups", dependencies=[Depends(enforce_csrf)])
async def add_lead_followup(
    lead_id: uuid.UUID,
    payload: LeadFollowupRequest,
    current_user: User = Depends(require_permissions("admission.edit")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AdmissionService(db)
    followup = await service.add_lead_followup(lead_id, payload, counsellor_id=current_user.id)
    return {"success": True, "followup_id": str(followup.id)}


# ==================== Applications ====================
@admission_router.get("/applications", response_model=Dict[str, Any])
async def list_applications(
    status: Optional[str] = Query(default=None),
    course_name: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(require_permissions("admission.view")),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    if not current_user.institute_id:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}
    service = AdmissionService(db)
    apps, total = await service.repo.list_applications_paginated(
        current_user.institute_id, status, course_name, search, page, page_size
    )
    return {
        "items": [ApplicationResponse.model_validate(a).model_dump() for a in apps],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@admission_router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    payload: ApplicationCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> ApplicationResponse:
    service = AdmissionService(db)
    app = await service.submit_application(payload)
    return ApplicationResponse.model_validate(app)


@admission_router.post("/applications/approve", dependencies=[Depends(enforce_csrf)])
async def approve_and_convert_admission(
    payload: AdmissionApproveRequest,
    current_user: User = Depends(require_permissions("admission.approve")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AdmissionService(db)
    app = await service.repo.get_application_by_id(payload.application_id)
    if not app:
        raise ValueError("Application not found.")

    actor_label = f"{current_user.first_name} {current_user.last_name}"
    student = await AdmissionWorkflowEngine.convert_application_to_student(
        session=db,
        application=app,
        allocated_batch=payload.allocated_batch,
        actor_name=actor_label,
    )
    return {
        "success": True,
        "message": "Admission approved. Student successfully enrolled in SIMS Module 6.",
        "student_id": str(student.id),
        "registration_number": student.registration_number,
    }


@admission_router.post("/applications/reject", dependencies=[Depends(enforce_csrf)])
async def reject_admission(
    payload: AdmissionRejectRequest,
    current_user: User = Depends(require_permissions("admission.approve")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AdmissionService(db)
    app = await service.repo.get_application_by_id(payload.application_id)
    if not app:
        raise ValueError("Application not found.")

    app.status = "REJECTED"
    app.rejection_reason = payload.rejection_reason
    actor_label = f"{current_user.first_name} {current_user.last_name}"
    await AdmissionWorkflowEngine.record_timeline(
        session=db,
        application_id=app.id,
        stage="REJECTION",
        title="Application Rejected",
        description=f"Admission rejected by {actor_label}. Reason: {payload.rejection_reason}",
        actor_name=actor_label,
    )
    await db.commit()
    return {"success": True, "message": "Application rejected."}


@admission_router.post("/documents/verify", dependencies=[Depends(enforce_csrf)])
async def verify_document(
    payload: DocumentVerifyRequest,
    current_user: User = Depends(require_permissions("admission.verify")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AdmissionService(db)
    doc = await service.verify_document(payload, current_user.id)
    return {"success": True, "document_id": str(doc.id), "status": doc.verification_status}


@admission_router.post("/fees/collect", dependencies=[Depends(enforce_csrf)])
async def collect_fee(
    payload: AdmissionFeeCollectRequest,
    current_user: User = Depends(require_permissions("fees.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AdmissionService(db)
    actor_label = f"{current_user.first_name} {current_user.last_name}"
    receipt = await service.collect_admission_fee(payload, actor_name=actor_label)
    return {
        "success": True,
        "receipt_number": receipt.receipt_number,
        "amount_paid": receipt.amount_paid,
    }
