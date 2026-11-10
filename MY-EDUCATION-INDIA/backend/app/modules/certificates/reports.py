from typing import Any, Dict, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.certificates.models import IssuedCertificate


class CertificateReportEngine:
    @staticmethod
    async def get_issuance_register(
        session: AsyncSession,
        institute_id: uuid.UUID,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        stmt = (
            select(IssuedCertificate)
            .where(IssuedCertificate.institute_id == institute_id)
            .order_by(IssuedCertificate.issue_date.desc())
            .limit(limit)
        )
        res = await session.execute(stmt)
        records = res.scalars().all()

        return [
            {
                "id": str(r.id),
                "certificate_number": r.certificate_number,
                "verification_id": r.verification_id,
                "recipient_type": r.recipient_type,
                "recipient_user_id": str(r.recipient_user_id),
                "issue_date": str(r.issue_date),
                "status": r.status,
            }
            for r in records
        ]
