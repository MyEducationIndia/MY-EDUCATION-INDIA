"""
Module 17: CRM Business Validators
"""
import re

class CrmBusinessValidators:
    @staticmethod
    def validate_mobile(mobile: str) -> bool:
        clean = re.sub(r'[^\d+]', '', mobile)
        return len(clean) >= 10 and len(clean) <= 15

    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return True
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    @staticmethod
    def validate_pipeline_stage(stage: str) -> bool:
        valid_stages = {
            "NEW_LEAD", "CONTACTED", "COUNSELLING", "DEMO_GIVEN",
            "INTERESTED", "DOCUMENTS_PENDING", "FEE_DISCUSSION",
            "ADMISSION_CONFIRMED", "LOST"
        }
        return stage.upper() in valid_stages

    @staticmethod
    def validate_probability(probability: float) -> bool:
        return 0.0 <= probability <= 100.0
