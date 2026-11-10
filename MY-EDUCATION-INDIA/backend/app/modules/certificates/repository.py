from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.certificates.models import (
    CertificateNumber,
    CertificateTemplate,
    DocumentType,
    IDCard,
    IssuedCertificate,
    VerificationLog,
    VerificationToken,
)


class CertificateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Document Types & Templates
    async def create_document_type(self, dt: DocumentType) -> DocumentType:
        self.session.add(dt)
        await self.session.commit()
        await self.session.refresh(dt)
        return dt

    async def get_document_types(self, institute_id: uuid.UUID) -> List[DocumentType]:
        stmt = select(DocumentType).where(DocumentType.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_template(self, t: CertificateTemplate) -> CertificateTemplate:
        self.session.add(t)
        await self.session.commit()
        await self.session.refresh(t)
        return t

    async def get_templates(self, institute_id: uuid.UUID) -> List[CertificateTemplate]:
        stmt = select(CertificateTemplate).where(CertificateTemplate.institute_id == institute_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_template_by_id(self, template_id: uuid.UUID) -> Optional[CertificateTemplate]:
        stmt = (
            select(CertificateTemplate)
            .where(CertificateTemplate.id == template_id)
            .options(selectinload(CertificateTemplate.document_type))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # Number Generator Counter
    async def get_or_increment_counter(self, institute_id: uuid.UUID, prefix: str, year: int) -> int:
        stmt = select(CertificateNumber).where(
            CertificateNumber.institute_id == institute_id,
            CertificateNumber.prefix == prefix,
            CertificateNumber.year == year,
        )
        res = await self.session.execute(stmt)
        record = res.scalar_one_or_none()
        if not record:
            record = CertificateNumber(institute_id=institute_id, prefix=prefix, year=year, current_counter=1)
            self.session.add(record)
        else:
            record.current_counter += 1
        await self.session.commit()
        return record.current_counter

    # Issued Certificates
    async def save_issued_certificate(self, cert: IssuedCertificate) -> IssuedCertificate:
        self.session.add(cert)
        await self.session.commit()
        await self.session.refresh(cert)
        return cert

    async def get_certificate_by_number(self, cert_number: str) -> Optional[IssuedCertificate]:
        stmt = (
            select(IssuedCertificate)
            .where(IssuedCertificate.certificate_number == cert_number)
            .options(selectinload(IssuedCertificate.template).selectinload(CertificateTemplate.document_type))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_certificate_by_verification_id(self, vrf_id: str) -> Optional[IssuedCertificate]:
        stmt = (
            select(IssuedCertificate)
            .where(IssuedCertificate.verification_id == vrf_id)
            .options(selectinload(IssuedCertificate.template).selectinload(CertificateTemplate.document_type))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # Public Verification Log
    async def record_verification_log(self, log_entry: VerificationLog) -> VerificationLog:
        self.session.add(log_entry)
        await self.session.commit()
        return log_entry

    # ID Cards
    async def save_id_card(self, card: IDCard) -> IDCard:
        self.session.add(card)
        await self.session.commit()
        await self.session.refresh(card)
        return card
