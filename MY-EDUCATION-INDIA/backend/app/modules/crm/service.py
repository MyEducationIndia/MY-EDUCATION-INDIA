"""
Module 17: CRM Service Layer
"""
from app.modules.crm.repository import CrmRepository
from app.modules.crm.validators import CrmBusinessValidators
from app.modules.crm.lead_engine import LeadScoringAndDeduplicationEngine
from app.modules.crm.automation_engine import FollowupAutomationEngine
from datetime import datetime

class CrmManagementService:
    def __init__(self, repo: CrmRepository):
        self.repo = repo

    async def capture_new_lead(self, institute_id: str, data: dict):
        if not CrmBusinessValidators.validate_mobile(data.get("mobile", "")):
            raise ValueError("Invalid mobile number format")
        score = LeadScoringAndDeduplicationEngine.compute_lead_score(
            source=data.get("source", "WEBSITE"),
            priority=data.get("priority", "MEDIUM"),
            has_guardian=bool(data.get("guardian_name")),
            has_email=bool(data.get("email"))
        )
        data["score"] = score
        return await self.repo.create_lead(institute_id, data)

    async def convert_enquiry_to_lead(self, institute_id: str, enquiry_id: str):
        # Auto-converts incoming website enquiry to active CRM lead
        pass

    def schedule_followup_reminder(self, current_time: datetime, stage: str):
        return FollowupAutomationEngine.schedule_next_followup(current_time, stage)
