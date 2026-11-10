import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import ast
import re
from datetime import datetime, date

from app.modules.crm.schemas import (
    CrmLeadCreate,
    CrmEnquiryCreate,
    CrmCampaignCreate,
    CrmOpportunityCreate,
    FranchiseCenterCreate
)
from app.modules.crm.validators import CrmBusinessValidators
from app.modules.crm.lead_engine import LeadScoringAndDeduplicationEngine
from app.modules.crm.automation_engine import FollowupAutomationEngine
from app.modules.crm.campaign_engine import CampaignROIEngine
from app.modules.crm.analytics import compute_conversion_metrics, calculate_expected_pipeline_revenue

class TestModule17CRMBackend(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.crm_backend_dir = os.path.join(self.base_dir, "backend/app/modules/crm")
        self.crm_frontend_dir = os.path.join(self.base_dir, "frontend/src/modules/crm")

    def test_crm_models_and_modules_ast(self):
        """Verify all Module 17 Python source files compile cleanly without syntax errors."""
        self.assertTrue(os.path.exists(self.crm_backend_dir), "CRM backend directory missing")
        py_files = [f for f in os.listdir(self.crm_backend_dir) if f.endswith(".py")]
        self.assertGreaterEqual(len(py_files), 12, "Expected at least 12 Python files in CRM module")
        for py_file in py_files:
            file_path = os.path.join(self.crm_backend_dir, py_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content, filename=py_file)
            except SyntaxError as e:
                self.fail(f"SyntaxError in {py_file}: {e}")

    def test_crm_schemas(self):
        """Test Pydantic schemas for leads, enquiries, campaigns, opportunities, and franchise centers."""
        lead = CrmLeadCreate(
            full_name="Aarav Sharma",
            mobile="+919876543210",
            email="aarav.sharma@example.com",
            priority="HIGH",
            stage="COUNSELLING"
        )
        self.assertEqual(lead.full_name, "Aarav Sharma")
        self.assertEqual(lead.priority, "HIGH")

        enquiry = CrmEnquiryCreate(
            enquirer_name="Rohan Gupta",
            mobile="+919876543222",
            source_type="WEBSITE",
            message="Inquiry about B.Tech CSE"
        )
        self.assertEqual(enquiry.source_type, "WEBSITE")

        campaign = CrmCampaignCreate(
            campaign_name="Engineering Admissions 2027",
            channel="GOOGLE_ADS",
            start_date=date(2026, 11, 1),
            allocated_budget=150000.0
        )
        self.assertEqual(campaign.allocated_budget, 150000.0)

        center = FranchiseCenterCreate(
            center_code="FC-IND-01",
            center_name="Indore Center",
            city="Indore",
            state="Madhya Pradesh",
            contact_email="indore@myeducation.in",
            contact_phone="+917312456789",
            royalty_percentage=15.0
        )
        self.assertEqual(center.city, "Indore")
        self.assertEqual(center.royalty_percentage, 15.0)

    def test_crm_business_validators(self):
        """Test mobile number, email, pipeline stage, and probability validators."""
        self.assertTrue(CrmBusinessValidators.validate_mobile("+919876543210"))
        self.assertTrue(CrmBusinessValidators.validate_mobile("9876543210"))
        self.assertFalse(CrmBusinessValidators.validate_mobile("123"))

        self.assertTrue(CrmBusinessValidators.validate_email("test@example.com"))
        self.assertTrue(CrmBusinessValidators.validate_email(None))
        self.assertFalse(CrmBusinessValidators.validate_email("invalid_email_string"))

        self.assertTrue(CrmBusinessValidators.validate_pipeline_stage("COUNSELLING"))
        self.assertTrue(CrmBusinessValidators.validate_pipeline_stage("ADMISSION_CONFIRMED"))
        self.assertFalse(CrmBusinessValidators.validate_pipeline_stage("INVALID_STAGE"))

        self.assertTrue(CrmBusinessValidators.validate_probability(75.0))
        self.assertFalse(CrmBusinessValidators.validate_probability(105.0))

    def test_lead_scoring_and_deduplication(self):
        """Test lead scoring algorithm and duplicate detection."""
        high_score = LeadScoringAndDeduplicationEngine.compute_lead_score(
            source="WALK_IN", priority="URGENT", has_guardian=True, has_email=True
        )
        self.assertEqual(high_score, 100) # 40 + 30 + 25 + 5 + 5 = 105 -> capped at 100

        low_score = LeadScoringAndDeduplicationEngine.compute_lead_score(
            source="WEBSITE", priority="LOW", has_guardian=False, has_email=False
        )
        self.assertEqual(low_score, 50) # 40 + 0 + 10 = 50

        # Deduplication
        self.assertTrue(LeadScoringAndDeduplicationEngine.is_duplicate_lead(
            "+919876543210", "aarav@test.com", "9876543210", "different@test.com"
        ))
        self.assertTrue(LeadScoringAndDeduplicationEngine.is_duplicate_lead(
            "+919876543210", "aarav@test.com", "+919999999999", "aarav@test.com"
        ))
        self.assertFalse(LeadScoringAndDeduplicationEngine.is_duplicate_lead(
            "+919876543210", "aarav@test.com", "+919999999999", "ananya@test.com"
        ))

    def test_followup_automation_and_reminders(self):
        """Test followup interval scheduling and notification alert payload."""
        now = datetime(2026, 11, 1, 10, 0, 0)
        next_dt = FollowupAutomationEngine.schedule_next_followup(now, "COUNSELLING")
        self.assertEqual(next_dt, datetime(2026, 11, 4, 10, 0, 0)) # +3 days

        alert = FollowupAutomationEngine.trigger_communication_alert("WHATSAPP", "+919876543210", "Reminder message")
        self.assertEqual(alert["dispatched_via"], "WHATSAPP")
        self.assertEqual(alert["status"], "DISPATCH_QUEUED")

    def test_campaign_roi_engine(self):
        """Test cost per lead and ROI calculations."""
        cpl = CampaignROIEngine.calculate_cost_per_lead(total_spent=50000.0, leads_generated=100)
        self.assertEqual(cpl, 500.0)

        roi = CampaignROIEngine.calculate_roi_percentage(revenue_generated=250000.0, total_spent=50000.0)
        self.assertEqual(roi, 400.0) # (250000 - 50000) / 50000 * 100 = 400%

    def test_analytics_and_pipeline_revenue(self):
        """Test conversion rate metrics and probability weighted revenue forecast."""
        conv = compute_conversion_metrics(total_leads=100, admissions_confirmed=32)
        self.assertEqual(conv["conversion_rate_percentage"], 32.0)

        opps = [
            {"deal_value": 100000.0, "probability_percentage": 50.0},
            {"deal_value": 200000.0, "probability_percentage": 75.0}
        ]
        weighted_rev = calculate_expected_pipeline_revenue(opps)
        self.assertEqual(weighted_rev, 200000.0) # 50,000 + 150,000 = 200,000

    def test_zero_browser_storage_crm(self):
        """Strictly enforce zero usage of localStorage, sessionStorage, or indexedDB in frontend."""
        storage_pattern = re.compile(r'\b(localStorage|sessionStorage|indexedDB)\b')
        violations = []
        for root, _, files in os.walk(self.crm_frontend_dir):
            for file in files:
                if file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        for line_idx, line in enumerate(f, 1):
                            if storage_pattern.search(line):
                                violations.append(f"{file}:{line_idx}")
        self.assertEqual(violations, [], f"Found forbidden browser storage usage: {violations}")

if __name__ == "__main__":
    unittest.main()
