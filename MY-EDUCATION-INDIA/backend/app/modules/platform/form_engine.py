"""Module 20: Dynamic Form Engine"""
import uuid
from datetime import datetime

class DynamicFormEngine:
    @staticmethod
    def generate_form_reference(form_key: str) -> str:
        ts = datetime.utcnow().strftime('%Y%m%d%H%M')
        u = str(uuid.uuid4())[:4].upper()
        return f'{form_key.upper()[:6]}-{ts}-{u}'

    @staticmethod
    def validate_submission_payload(schema_fields: list, payload: dict) -> list:
        errors = []
        for field in schema_fields:
            name = field.get('name')
            is_req = field.get('required', False)
            if is_req and (name not in payload or payload[name] is None or payload[name] == ''):
                errors.append(f"Field '{field.get('label', name)}' is required.")
        return errors
