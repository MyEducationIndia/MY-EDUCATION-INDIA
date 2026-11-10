from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.modules.auth.dependencies import get_current_user, require_permissions
from app.modules.certificates.analytics import CertificateAnalyticsEngine
from app.modules.certificates.reports import CertificateReportEngine
from app.modules.certificates.schemas import (
    CertificateDashboardSummary,
    CertificateRevokeRequest,
    CertificateTemplateCreate,
    CertificateTemplateResponse,
    DocumentTypeCreate,
    DocumentTypeResponse,
    IDCardGenerateRequest,
    IDCardResponse,
    IssuedCertificateResponse,
    PublicVerificationResult,
    SingleCertificateIssueRequest,
)
from app.modules.certificates.service import CertificateManagementService

certificate_router = APIRouter(prefix="/certificates", tags=["Enterprise Certificate & Document Management"])
public_verify_router = APIRouter(prefix="/public/verify", tags=["Public Digital Verification Portal"])


# 1. Dashboard & Analytics
@certificate_router.get("/dashboard", response_model=CertificateDashboardSummary)
async def get_certificate_dashboard(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("certificates.view")),
) -> CertificateDashboardSummary:
    summary = await CertificateAnalyticsEngine.get_dashboard_kpis(db, institute_id)
    return CertificateDashboardSummary.model_validate(summary)


# 2. Document Types & Templates
@certificate_router.get("/types", response_model=List[DocumentTypeResponse])
async def list_document_types(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[DocumentTypeResponse]:
    service = CertificateManagementService(db)
    items = await service.repo.get_document_types(institute_id)
    return [DocumentTypeResponse.model_validate(it) for it in items]


@certificate_router.post("/types", response_model=DocumentTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_document_type(
    payload: DocumentTypeCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("certificates.manage")),
) -> DocumentTypeResponse:
    service = CertificateManagementService(db)
    item = await service.create_document_type(payload)
    return DocumentTypeResponse.model_validate(item)


@certificate_router.get("/templates", response_model=List[CertificateTemplateResponse])
async def list_templates(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CertificateTemplateResponse]:
    service = CertificateManagementService(db)
    items = await service.repo.get_templates(institute_id)
    return [CertificateTemplateResponse.model_validate(it) for it in items]


@certificate_router.post("/templates", response_model=CertificateTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    payload: CertificateTemplateCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("certificates.manage")),
) -> CertificateTemplateResponse:
    service = CertificateManagementService(db)
    t = await service.create_template(payload)
    return CertificateTemplateResponse.model_validate(t)


# 3. Issuance & Revocation
@certificate_router.post("/issue", response_model=IssuedCertificateResponse, status_code=status.HTTP_201_CREATED)
async def issue_certificate(
    payload: SingleCertificateIssueRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("certificates.issue")),
) -> IssuedCertificateResponse:
    service = CertificateManagementService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    cert = await service.issue_single_certificate(payload, issued_by_user_id=user_id)
    return IssuedCertificateResponse.model_validate(cert)


@certificate_router.post("/revoke", response_model=IssuedCertificateResponse)
async def revoke_certificate(
    payload: CertificateRevokeRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("certificates.revoke")),
) -> IssuedCertificateResponse:
    service = CertificateManagementService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    cert = await service.revoke_certificate(payload, revoked_by_user_id=user_id)
    return IssuedCertificateResponse.model_validate(cert)


# 4. ID Cards
@certificate_router.post("/id-cards", response_model=IDCardResponse, status_code=status.HTTP_201_CREATED)
async def issue_id_card(
    payload: IDCardGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("certificates.issue")),
) -> IDCardResponse:
    service = CertificateManagementService(db)
    card = await service.issue_id_card(payload)
    return IDCardResponse.model_validate(card)


# 5. Reports
@certificate_router.get("/reports/register")
async def get_issuance_register(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("certificates.view")),
) -> List[Dict[str, Any]]:
    return await CertificateReportEngine.get_issuance_register(db, institute_id)


# 6. Public Verification Portal (Unauthenticated)
@public_verify_router.get("/{identifier}", response_model=PublicVerificationResult)
async def verify_credential_public(
    identifier: str,
    db: AsyncSession = Depends(get_db_session),
) -> PublicVerificationResult:
    service = CertificateManagementService(db)
    return await service.verify_credential_public(identifier)
