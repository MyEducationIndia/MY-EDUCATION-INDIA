import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ------------------- Document Types & Templates -------------------
class DocumentTypeCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    category: str = "ACADEMIC" # ACADEMIC, ADMINISTRATIVE, IDENTIFICATION
    requires_approval: bool = True
    has_expiry: bool = False
    validity_months: int = Field(12, ge=1)


class DocumentTypeResponse(DocumentTypeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class CertificateTemplateCreate(BaseModel):
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    document_type_id: uuid.UUID
    template_code: str = Field(..., min_length=2, max_length=48)
    title: str = Field(..., min_length=3, max_length=180)
    page_orientation: str = "LANDSCAPE" # LANDSCAPE, PORTRAIT
    page_size: str = "A4" # A4, LETTER, LEGAL, ID_CARD_CR80
    background_image_url: Optional[str] = None
    html_markup: str = Field(..., min_length=10)
    css_styles: str = ""


class CertificateTemplateResponse(CertificateTemplateCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    version: int
    is_active: bool
    created_at: datetime


# ------------------- Certificate Generation & Issuance -------------------
class SingleCertificateIssueRequest(BaseModel):
    template_id: uuid.UUID
    recipient_type: str = "STUDENT" # STUDENT, FACULTY, STAFF, EXTERNAL
    recipient_user_id: uuid.UUID
    payload_data: Dict[str, Any] = Field(default_factory=dict)
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None


class BulkCertificateIssueRequest(BaseModel):
    template_id: uuid.UUID
    recipient_user_ids: List[uuid.UUID] = Field(..., min_items=1)
    shared_payload_data: Dict[str, Any] = Field(default_factory=dict)
    issue_date: Optional[date] = None


class IssuedCertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    certificate_number: str
    verification_id: str
    template_id: uuid.UUID
    institute_id: uuid.UUID
    recipient_type: str
    recipient_user_id: uuid.UUID
    issue_date: date
    expiry_date: Optional[date]
    status: str
    qr_code_payload: str
    barcode_data: str
    created_at: datetime


class CertificateRevokeRequest(BaseModel):
    certificate_id: uuid.UUID
    reason: str = Field(..., min_length=5)


# ------------------- ID Cards -------------------
class IDCardGenerateRequest(BaseModel):
    institute_id: uuid.UUID
    holder_type: str = "STUDENT" # STUDENT, FACULTY, STAFF, VISITOR
    holder_user_id: uuid.UUID
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    valid_until: date


class IDCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    card_number: str
    holder_type: str
    holder_user_id: uuid.UUID
    blood_group: Optional[str]
    emergency_contact: Optional[str]
    valid_until: date
    status: str
    qr_code_payload: str
    created_at: datetime


# ------------------- Public Verification -------------------
class PublicVerificationResult(BaseModel):
    is_valid: bool
    status: str # VALID, REVOKED, EXPIRED, NOT_FOUND
    certificate_number: Optional[str] = None
    document_type_name: Optional[str] = None
    recipient_name_masked: Optional[str] = None
    institute_name: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    digital_signature_verified: bool = False
    message: str


# ------------------- Dashboard & Analytics -------------------
class CertificateDashboardSummary(BaseModel):
    total_issued_certificates: int
    pending_approvals_count: int
    revoked_certificates_count: int
    public_verifications_count: int
    active_templates_count: int
    id_cards_active_count: int
    document_distribution: Dict[str, int]
    monthly_trend: List[Dict[str, Any]]
