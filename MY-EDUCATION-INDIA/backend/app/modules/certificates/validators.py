from datetime import date
from app.core.exceptions import ValidationException
from app.modules.certificates.schemas import CertificateTemplateCreate


class CertificateBusinessValidators:
    @staticmethod
    def validate_template_markup(payload: CertificateTemplateCreate) -> None:
        if not payload.html_markup or len(payload.html_markup.strip()) < 10:
            raise ValidationException("Certificate HTML markup must contain substantive layout structures.")
        if payload.page_orientation not in ["LANDSCAPE", "PORTRAIT"]:
            raise ValidationException("Page orientation must be either LANDSCAPE or PORTRAIT.")
        if payload.page_size not in ["A4", "LETTER", "LEGAL", "ID_CARD_CR80"]:
            raise ValidationException("Unsupported page format size specified.")

    @staticmethod
    def validate_certificate_dates(issue_date: date, expiry_date: date | None) -> None:
        if expiry_date and issue_date >= expiry_date:
            raise ValidationException("Certificate issue date must precede the expiry date.")
