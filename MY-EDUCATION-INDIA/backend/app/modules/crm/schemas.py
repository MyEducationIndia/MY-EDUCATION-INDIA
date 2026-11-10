"""
Module 17: CRM Schemas (Pydantic v2 / v1 compatible)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

class CrmLeadBase(BaseModel):
    full_name: str = Field(..., max_length=200)
    mobile: str = Field(..., max_length=30)
    email: Optional[str] = None
    guardian_name: Optional[str] = None
    course_interested_id: Optional[str] = None
    source_id: Optional[str] = None
    priority: str = "MEDIUM" # LOW, MEDIUM, HIGH, URGENT
    assigned_counsellor_id: Optional[str] = None
    stage: str = "NEW_LEAD"
    status: str = "ACTIVE"
    expected_admission_date: Optional[date] = None
    remarks: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class CrmLeadCreate(CrmLeadBase):
    pass

class CrmLeadResponse(CrmLeadBase):
    id: str
    institute_id: str
    lead_code: str
    score: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CrmEnquiryCreate(BaseModel):
    enquirer_name: str = Field(..., max_length=200)
    mobile: str = Field(..., max_length=30)
    email: Optional[str] = None
    source_type: str = "WEBSITE"
    course_id: Optional[str] = None
    message: Optional[str] = None

class CrmEnquiryResponse(CrmEnquiryCreate):
    id: str
    institute_id: str
    enquiry_code: str
    is_converted_to_lead: bool
    lead_id: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class CrmFollowupCreate(BaseModel):
    lead_id: str
    counsellor_id: str
    channel: str = "CALL"
    scheduled_at: datetime
    notes: Optional[str] = None
    outcome: Optional[str] = None
    next_followup_date: Optional[datetime] = None

class CrmFollowupResponse(CrmFollowupCreate):
    id: str
    institute_id: str
    completed_at: Optional[datetime] = None
    is_reminder_sent: bool
    created_at: datetime

    class Config:
        orm_mode = True

class CrmCampaignCreate(BaseModel):
    campaign_name: str = Field(..., max_length=200)
    channel: str # GOOGLE_ADS, FACEBOOK, INSTAGRAM, WHATSAPP, SMS, EMAIL, OFFLINE
    start_date: date
    end_date: Optional[date] = None
    allocated_budget: float = 0.0
    actual_spent: float = 0.0
    status: str = "ACTIVE"
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None

class CrmCampaignResponse(CrmCampaignCreate):
    id: str
    institute_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class CrmReferralCreate(BaseModel):
    referral_type: str = "STUDENT"
    referrer_name: str = Field(..., max_length=200)
    coupon_code: str = Field(..., max_length=50)
    commission_amount: float = 0.0

class CrmReferralResponse(CrmReferralCreate):
    id: str
    institute_id: str
    status: str
    referred_lead_id: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class CrmTaskCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    assigned_to_user_id: str
    related_lead_id: Optional[str] = None
    priority: str = "MEDIUM"
    due_date: datetime

class CrmTaskResponse(CrmTaskCreate):
    id: str
    institute_id: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class CrmOpportunityCreate(BaseModel):
    lead_id: str
    deal_value: float
    probability_percentage: float = 50.0
    expected_closing_date: date
    stage: str = "NEGOTIATION"
    remarks: Optional[str] = None

class CrmOpportunityResponse(CrmOpportunityCreate):
    id: str
    institute_id: str
    expected_revenue: float
    created_at: datetime

    class Config:
        orm_mode = True

class FranchiseCenterCreate(BaseModel):
    center_code: str = Field(..., max_length=50)
    center_name: str = Field(..., max_length=200)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    contact_email: str
    contact_phone: str
    royalty_percentage: float = 15.0

class FranchiseCenterResponse(FranchiseCenterCreate):
    id: str
    institute_id: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class CrmDashboardMetrics(BaseModel):
    total_new_leads: int
    todays_followups_count: int
    admissions_this_month: int
    conversion_rate_percentage: float
    revenue_forecast: float
    top_counsellor: str
    active_campaigns_count: int
    pending_tasks_count: int
