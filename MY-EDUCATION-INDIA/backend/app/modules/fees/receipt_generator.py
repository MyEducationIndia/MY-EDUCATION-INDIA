import hashlib
import json
import uuid
from datetime import datetime


def number_to_indian_currency_words(amount: float) -> str:
    """Converts a numeric amount to Indian Currency Words (Lakhs, Crores, Thousands)."""
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def convert_upto_thousand(n: int) -> str:
        words = []
        if n >= 100:
            words.append(units[n // 100] + " Hundred")
            n %= 100
        if 10 <= n <= 19:
            words.append(teens[n - 10])
        elif n >= 20:
            words.append(tens[n // 10])
            if n % 10:
                words.append(units[n % 10])
        elif n > 0:
            words.append(units[n])
        return " ".join(words)

    int_part = int(round(amount))
    if int_part == 0:
        return "Zero Rupees Only"

    crores = int_part // 10000000
    int_part %= 10000000
    lakhs = int_part // 100000
    int_part %= 100000
    thousands = int_part // 1000
    int_part %= 1000
    remainder = int_part

    parts = []
    if crores > 0:
        parts.append(convert_upto_thousand(crores) + " Crore")
    if lakhs > 0:
        parts.append(convert_upto_thousand(lakhs) + " Lakh")
    if thousands > 0:
        parts.append(convert_upto_thousand(thousands) + " Thousand")
    if remainder > 0:
        parts.append(convert_upto_thousand(remainder))

    return " ".join(parts).strip() + " Rupees Only"


class ReceiptGenerator:
    @staticmethod
    def generate_receipt_number(institute_code: str = "MEI") -> str:
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_suffix = uuid.uuid4().hex[:6].upper()
        return f"REC-{institute_code}-{timestamp_str}-{unique_suffix}"

    @staticmethod
    def generate_digital_signature(receipt_number: str, amount: float, student_id: str) -> str:
        payload = f"{receipt_number}:{amount:.2f}:{student_id}:MEI_SECURE_TOKEN_2026"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_qr_payload(receipt_number: str, amount: float, student_id: str, payment_date: str) -> str:
        data = {
            "entity": "MY EDUCATION INDIA ERP",
            "receipt_no": receipt_number,
            "amount": amount,
            "student_id": student_id,
            "date": payment_date,
            "verified": True,
        }
        return json.dumps(data)
