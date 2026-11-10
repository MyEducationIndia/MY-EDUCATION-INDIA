import hashlib
import json
from datetime import date


class TranscriptGenerator:
    @staticmethod
    def generate_transcript_number(institute_code: str = "MEI") -> str:
        year_str = date.today().strftime("%Y")
        unique_suffix = hashlib.sha256(str(date.today()).encode("utf-8")).hexdigest()[:6].upper()
        return f"TRN-{institute_code}-{year_str}-{unique_suffix}"

    @staticmethod
    def sign_transcript(transcript_number: str, student_id: str, cgpa: float) -> str:
        raw = f"{transcript_number}:{student_id}:{cgpa:.2f}:MEI_EXAM_CONTROLLER_SECRET_2026"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
