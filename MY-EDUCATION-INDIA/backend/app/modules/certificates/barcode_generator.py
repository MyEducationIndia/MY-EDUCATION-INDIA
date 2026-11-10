import re


class CertificateBarcodeGenerator:
    @staticmethod
    def generate_barcode_token(cert_number: str) -> str:
        clean = re.sub(r"[^A-Za-z0-9]", "", cert_number)
        return clean.upper()
