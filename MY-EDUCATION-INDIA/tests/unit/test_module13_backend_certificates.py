"""Unit and Integration Tests for Module 13: Enterprise Certificate, Document Generation & Digital Verification System
Verifies:
- AST compilation across all Module 13 backend files
- Pydantic v2 schemas validation for document types, certificate templates, and issue requests
- CertificatePDFCompiler dynamic placeholder interpolation ({{student_name}}, {{cgpa}}, etc.)
- DigitalVerificationEngine cryptographic HMAC SHA-256 token hashing & validation
- CertificateSequenceEngine universal numbering (DEG-2026-000001) & unique verification IDs
- CertificateQRGenerator & BarcodeGenerator payload validation
- CertificateBusinessValidators (issue date vs expiry date, template markup requirements)
- Zero browser LocalStorage/SessionStorage/IndexedDB in Module 13 frontend source
"""
import ast
from datetime import date
import os
from pathlib import Path
import re
import sys
import unittest
import uuid

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

os.environ.setdefault("SECRET_KEY", "test_secret_key_minimum_32_characters_long_for_security")
os.environ.setdefault("REFRESH_SECRET_KEY", "test_refresh_secret_key_minimum_32_characters_long")
os.environ.setdefault("CSRF_SECRET_KEY", "test_csrf_secret_key_minimum_32_characters_long_sec")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("SYNC_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")

from app.core.exceptions import ValidationException
from app.modules.certificates.barcode_generator import CertificateBarcodeGenerator
from app.modules.certificates.certificate_engine import CertificateSequenceEngine
from app.modules.certificates.pdf_generator import CertificatePDFCompiler
from app.modules.certificates.qr_generator import CertificateQRGenerator
from app.modules.certificates.schemas import (
    CertificateTemplateCreate,
    DocumentTypeCreate,
    IDCardGenerateRequest,
    SingleCertificateIssueRequest,
)
from app.modules.certificates.validators import CertificateBusinessValidators
from app.modules.certificates.verification_engine import DigitalVerificationEngine


class TestModule13BackendCertificates(unittest.TestCase):

    def test_all_module13_python_files_compile(self) -> None:
        cert_dir = PROJECT_ROOT / "backend/app/modules/certificates"
        self.assertTrue(cert_dir.exists(), "certificates backend directory must exist")
        for py_file in cert_dir.glob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                ast.parse(source, filename=str(py_file))
            except SyntaxError as exc:
                self.fail(f"Syntax error in {py_file}: {exc}")

    def test_certificate_schemas_validation(self) -> None:
        dummy_inst_id = uuid.uuid4()
        dummy_type_id = uuid.uuid4()
        dummy_user_id = uuid.uuid4()
        dummy_tmpl_id = uuid.uuid4()

        dt = DocumentTypeCreate(
            institute_id=dummy_inst_id,
            code="DEGREE",
            name="Bachelor Degree in Technology",
            category="ACADEMIC",
        )
        self.assertEqual(dt.code, "DEGREE")
        self.assertTrue(dt.requires_approval)

        tmpl = CertificateTemplateCreate(
            institute_id=dummy_inst_id,
            document_type_id=dummy_type_id,
            template_code="DEGREE-BTECH-2026",
            title="B.Tech Degree in Computer Science",
            page_orientation="LANDSCAPE",
            page_size="A4",
            html_markup="<div class='cert'><h1>{{student_name}}</h1></div>",
        )
        self.assertEqual(tmpl.page_orientation, "LANDSCAPE")

        issue_req = SingleCertificateIssueRequest(
            template_id=dummy_tmpl_id,
            recipient_user_id=dummy_user_id,
            payload_data={"student_name": "Aarav Sharma", "cgpa": 9.72},
        )
        self.assertEqual(issue_req.recipient_type, "STUDENT")

        card_req = IDCardGenerateRequest(
            institute_id=dummy_inst_id,
            holder_user_id=dummy_user_id,
            blood_group="O+",
            valid_until=date(2030, 6, 30),
        )
        self.assertEqual(card_req.blood_group, "O+")

    def test_pdf_placeholder_interpolation(self) -> None:
        template = "<div>This certifies that {{student_name}} completed {{course_name}} with CGPA {{cgpa}}.</div>"
        data = {
            "student_name": "Ananya Iyer",
            "course_name": "B.Tech Computer Science & AI",
            "cgpa": 9.85,
        }
        interpolated = CertificatePDFCompiler.interpolate_placeholders(template, data)
        self.assertIn("Ananya Iyer", interpolated)
        self.assertIn("B.Tech Computer Science & AI", interpolated)
        self.assertIn("9.85", interpolated)
        self.assertNotIn("{{student_name}}", interpolated)

        wrapped = CertificatePDFCompiler.inject_print_css(interpolated, "h1 { color: #0d9488; }", "LANDSCAPE")
        self.assertIn("@page { size: landscape; margin: 0; }", wrapped)
        self.assertIn("h1 { color: #0d9488; }", wrapped)

    def test_digital_verification_engine(self) -> None:
        vrf_id = "VRF-98F12A09B42C"
        cert_no = "DEG-2026-000042"
        recipient_id = str(uuid.uuid4())

        token_hash = DigitalVerificationEngine.generate_token_hash(vrf_id, cert_no, recipient_id)
        self.assertEqual(len(token_hash), 64) # SHA-256

        # Valid hash check
        self.assertTrue(DigitalVerificationEngine.verify_token(vrf_id, cert_no, recipient_id, token_hash))

        # Tampered hash check
        self.assertFalse(DigitalVerificationEngine.verify_token(vrf_id, cert_no, recipient_id, "tampered_token_hash_000000000000000000000000000000000000000000000"))

    def test_certificate_sequence_engine_and_qr(self) -> None:
        cert_num = CertificateSequenceEngine.format_certificate_number("CERT", 2026, 42)
        self.assertEqual(cert_num, "CERT-2026-000042")

        vrf_id = CertificateSequenceEngine.generate_unique_verification_id()
        self.assertTrue(vrf_id.startswith("VRF-"))

        qr = CertificateQRGenerator.generate_verification_qr_payload(
            verification_id=vrf_id,
            cert_number=cert_num,
            institute_id="inst-1",
            public_url="https://myeducationindia.com/verify?id=" + vrf_id,
        )
        self.assertIn("OFFICIAL_DIGITAL_CREDENTIAL", qr)
        self.assertIn(cert_num, qr)

        barcode = CertificateBarcodeGenerator.generate_barcode_token(cert_num)
        self.assertEqual(barcode, "CERT2026000042")

    def test_certificate_business_validators(self) -> None:
        # Invalid date range
        with self.assertRaises(ValidationException):
            CertificateBusinessValidators.validate_certificate_dates(date(2027, 1, 1), date(2026, 1, 1))

        # Invalid orientation
        with self.assertRaises(ValidationException):
            CertificateBusinessValidators.validate_template_markup(
                CertificateTemplateCreate(
                    institute_id=uuid.uuid4(),
                    document_type_id=uuid.uuid4(),
                    template_code="INVALID",
                    title="Invalid",
                    page_orientation="DIAGONAL",
                    html_markup="<div>This is valid markup length</div>",
                )
            )

    def test_zero_browser_storage_in_certificates_frontend(self) -> None:
        cert_fe_dir = PROJECT_ROOT / "frontend/src/modules/certificates"
        self.assertTrue(cert_fe_dir.exists(), "Certificates frontend directory must exist")
        forbidden = [r"\blocalStorage\b", r"\bsessionStorage\b", r"\bindexedDB\b"]

        for ts_file in cert_fe_dir.rglob("*.ts*"):
            content = ts_file.read_text(encoding="utf-8")
            for pattern in forbidden:
                matches = re.findall(pattern, content, re.IGNORECASE)
                self.assertEqual(
                    matches,
                    [],
                    f"Forbidden storage API found in {ts_file.name}: {matches}",
                )


if __name__ == "__main__":
    unittest.main()
