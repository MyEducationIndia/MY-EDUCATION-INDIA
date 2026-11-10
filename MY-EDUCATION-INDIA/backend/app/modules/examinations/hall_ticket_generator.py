import hashlib
import json
import uuid


class HallTicketGenerator:
    @staticmethod
    def generate_hall_ticket_number(session_code: str, roll_number: str) -> str:
        clean_roll = roll_number.replace("-", "").upper()
        return f"HT-{session_code}-{clean_roll}"

    @staticmethod
    def generate_qr_payload(hall_ticket_no: str, student_id: str, session_id: str) -> str:
        payload = {
            "entity": "MY EDUCATION INDIA ERP",
            "document": "OFFICIAL_EXAM_HALL_TICKET",
            "ht_no": hall_ticket_no,
            "student_id": student_id,
            "session_id": session_id,
            "verified": True,
        }
        return json.dumps(payload)
