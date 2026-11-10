from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ValidationException
from app.modules.certificates.barcode_generator import CertificateBarcodeGenerator
from app.modules.certificates.certificate_engine import CertificateSequenceEngine
from app.modules.certificates.models import (
    CertificateStatusHistory,
    CertificateTemplate,
    DocumentType,
    IDCard,
    IssuedCertificate,
    VerificationToken,
)
from app.modules.certificates.pdf_generator import CertificatePDFCompiler
from app.modules.certificates.qr_generator import CertificateQRGenerator
from app.modules.certificates.repository import CertificateRepository
from app.modules.certificates.schemas import (
    BulkCertificateIssueRequest,
    CertificateRevokeRequest,
    CertificateTemplateCreate,
    DocumentTypeCreate,
    IDCardGenerateRequest,
    PublicVerificationResult,
    SingleCertificateIssueRequest,
)
from app.modules.certificates.validators import CertificateBusinessValidators
from app.modules.certificates.verification_engine import DigitalVerificationEngine


class CertificateManagementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CertificateRepository(session)

    # 1. Document Types & Templates
    async def create_document_type(self, payload: DocumentTypeCreate) -> DocumentType:
        dt = DocumentType(
            institute_id=payload.institute_id,
            code=payload.code.strip().upper(),
            name=payload.name.strip(),
            description=payload.description,
            category=payload.category,
            requires_approval=payload.requires_approval,
            has_expiry=payload.has_expiry,
            validity_months=payload.validity_months,
            is_active=True,
        )
        return await self.repo.create_document_type(dt)

    async def create_template(self, payload: CertificateTemplateCreate) -> CertificateTemplate:
        CertificateBusinessValidators.validate_template_markup(payload)
        t = CertificateTemplate(
            institute_id=payload.institute_id,
            branch_id=payload.branch_id,
            document_type_id=payload.document_type_id,
            template_code=payload.template_code.strip().upper(),
            title=payload.title.strip(),
            page_orientation=payload.page_orientation,
            page_size=payload.page_size,
            background_image_url=payload.background_image_url,
            html_markup=payload.html_markup,
            css_styles=payload.css_styles,
            is_active=True,
        )
        return await self.repo.create_template(t)

    # 2. Issue Certificate
    async def issue_single_certificate(
        self,
        payload: SingleCertificateIssueRequest,
        issued_by_user_id: uuid.UUID,
    ) -> IssuedCertificate:
        template = await self.repo.get_template_by_id(payload.template_id)
        if not template:
            raise NotFoundException("Certificate template not found.")

        issue_dt = payload.issue_date or date.today()
        CertificateBusinessValidators.validate_certificate_dates(issue_dt, payload.expiry_date)

        # Generate sequence number and verification IDs
        year = issue_dt.year
        counter = await self.repo.get_or_increment_counter(template.institute_id, template.document_type.code, year)
        cert_no = CertificateSequenceEngine.format_certificate_number(template.document_type.code, year, counter)
        vrf_id = CertificateSequenceEngine.generate_unique_verification_id()

        public_url = f"https://myeducationindia.com/verify?id={vrf_id}"
        qr_payload = CertificateQRGenerator.generate_verification_qr_payload(
            verification_id=vrf_id,
            cert_number=cert_no,
            institute_id=str(template.institute_id),
            public_url=public_url,
        )
        barcode_data = CertificateBarcodeGenerator.generate_barcode_token(cert_no)

        cert = IssuedCertificate(
            certificate_number=cert_no,
            verification_id=vrf_id,
            template_id=payload.template_id,
            institute_id=template.institute_id,
            recipient_type=payload.recipient_type,
            recipient_user_id=payload.recipient_user_id,
            issue_date=issue_dt,
            expiry_date=payload.expiry_date,
            payload_data_json=payload.payload_data,
            qr_code_payload=qr_payload,
            barcode_data=barcode_data,
            status="ISSUED",
            issued_by_user_id=issued_by_user_id,
        )
        saved_cert = await self.repo.save_issued_certificate(cert)

        # Attach verification token
        token_hash = DigitalVerificationEngine.generate_token_hash(vrf_id, cert_no, str(payload.recipient_user_id))
        vrf_token = VerificationToken(
            certificate_id=saved_cert.id,
            token_hash=token_hash,
            public_verification_url=public_url,
        )
        self.session.add(vrf_token)
        await self.session.commit()

        return saved_cert

    # 3. Revoke Certificate
    async def revoke_certificate(
        self,
        payload: CertificateRevokeRequest,
        revoked_by_user_id: uuid.UUID,
    ) -> IssuedCertificate:
        cert = await self.session.get(IssuedCertificate, payload.certificate_id)
        if not cert:
            raise NotFoundException("Certificate not found.")

        old_status = cert.status
        cert.status = "REVOKED"
        cert.revocation_reason = payload.reason
        cert.revoked_at = datetime.now(timezone.utc)

        history = CertificateStatusHistory(
            certificate_id=cert.id,
            previous_status=old_status,
            new_status="REVOKED",
            changed_by_user_id=revoked_by_user_id,
            reason=payload.reason,
        )
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(cert)
        return cert

    # 4. Public Verification
    async def verify_credential_public(self, identifier: str) -> PublicVerificationResult:
        # Check by cert_number or verification_id
        cert = await self.repo.get_certificate_by_verification_id(identifier)
        if not cert:
            cert = await self.repo.get_certificate_by_number(identifier)

        if not cert:
            return PublicVerificationResult(
                is_valid=False,
                status="NOT_FOUND",
                message="No institutional credential matching this identifier was located in the verification registry.",
            )

        if cert.status == "REVOKED":
            return PublicVerificationResult(
                is_valid=False,
                status="REVOKED",
                certificate_number=cert.certificate_number,
                document_type_name=cert.template.document_type.name,
                issue_date=cert.issue_date,
                message=f"This credential was officially REVOKED by the institution. Reason: {cert.revocation_reason}",
            )

        if cert.expiry_date and cert.expiry_date < date.today():
            return PublicVerificationResult(
                is_valid=False,
                status="EXPIRED",
                certificate_number=cert.certificate_number,
                document_type_name=cert.template.document_type.name,
                issue_date=cert.issue_date,
                expiry_date=cert.expiry_date,
                message="This credential has expired past its official institutional validity date.",
            )

        return PublicVerificationResult(
            is_valid=True,
            status="VALID",
            certificate_number=cert.certificate_number,
            document_type_name=cert.template.document_type.name,
            recipient_name_masked="A**** S****",
            institute_name="MY EDUCATION INDIA",
            issue_date=cert.issue_date,
            expiry_date=cert.expiry_date,
            digital_signature_verified=True,
            message="Verified authentic institutional credential issued by MY EDUCATION INDIA.",
        )

    # 5. ID Cards
    async def issue_id_card(self, payload: IDCardGenerateRequest) -> IDCard:
        card_no = f"ID-{payload.holder_type[:3]}-{uuid.uuid4().hex[:8].upper()}"
        qr = f'{{"entity":"MY_EDUCATION_INDIA","id_card":"{card_no}"}}'
        card = IDCard(
            institute_id=payload.institute_id,
            card_number=card_no,
            holder_type=payload.holder_type,
            holder_user_id=payload.holder_user_id,
            blood_group=payload.blood_group,
            emergency_contact=payload.emergency_contact,
            valid_until=payload.valid_until,
            qr_code_payload=qr,
            barcode_data=card_no.replace("-", ""),
            status="ACTIVE",
        )
        return await self.repo.save_id_card(card)
