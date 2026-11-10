"""
Module 17: Enterprise CRM, Sales, Marketing & Franchise Management System - Models
Provisions 16 enterprise tables for leads, enquiries, follow-ups, pipeline stages,
campaigns, referrals, tasks, opportunities, and franchise management.
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class CrmLead(Base):
    __tablename__ = "crm_leads"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    lead_code = Column(String(50), nullable=False, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    mobile = Column(String(30), nullable=False, index=True)
    email = Column(String(150), nullable=True, index=True)
    guardian_name = Column(String(200), nullable=True)
    course_interested_id = Column(String(36), nullable=True)
    source_id = Column(String(36), ForeignKey("crm_lead_sources.id"), nullable=True)
    priority = Column(String(20), default="MEDIUM", nullable=False) # LOW, MEDIUM, HIGH, URGENT
    assigned_counsellor_id = Column(String(36), nullable=True, index=True)
    stage = Column(String(50), default="NEW_LEAD", nullable=False, index=True)
    # NEW_LEAD, CONTACTED, COUNSELLING, DEMO_GIVEN, INTERESTED, DOCUMENTS_PENDING, FEE_DISCUSSION, ADMISSION_CONFIRMED, LOST
    status = Column(String(30), default="ACTIVE", nullable=False) # ACTIVE, CONVERTED, DROPPED
    expected_admission_date = Column(Date, nullable=True)
    score = Column(Integer, default=50, nullable=False)
    remarks = Column(Text, nullable=True)
    custom_fields = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    source = relationship("CrmLeadSource", back_populates="leads")
    followups = relationship("CrmFollowup", back_populates="lead", cascade="all, delete-orphan")
    opportunities = relationship("CrmOpportunity", back_populates="lead", cascade="all, delete-orphan")
    activities = relationship("CrmActivityLog", back_populates="lead", cascade="all, delete-orphan")

class CrmEnquiry(Base):
    __tablename__ = "crm_enquiries"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    enquiry_code = Column(String(50), nullable=False, index=True)
    enquirer_name = Column(String(200), nullable=False)
    mobile = Column(String(30), nullable=False, index=True)
    email = Column(String(150), nullable=True)
    source_type = Column(String(50), default="WEBSITE", nullable=False)
    # WEBSITE, WALK_IN, PHONE, WHATSAPP, FACEBOOK, INSTAGRAM, GOOGLE_ADS, REFERRAL, EDUCATION_FAIR, MANUAL
    course_id = Column(String(36), nullable=True)
    message = Column(Text, nullable=True)
    is_converted_to_lead = Column(Boolean, default=False, nullable=False)
    lead_id = Column(String(36), ForeignKey("crm_leads.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CrmFollowup(Base):
    __tablename__ = "crm_followups"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    lead_id = Column(String(36), ForeignKey("crm_leads.id"), nullable=False, index=True)
    counsellor_id = Column(String(36), nullable=False, index=True)
    channel = Column(String(30), default="CALL", nullable=False) # CALL, WHATSAPP, SMS, EMAIL, MEETING, VISIT, VIDEO_CALL
    scheduled_at = Column(DateTime, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    outcome = Column(String(50), nullable=True) # INTERESTED, BUSY_CALLBACK, NOT_REACHABLE, NOT_INTERESTED, ADMISSION_PROMISED
    next_followup_date = Column(DateTime, nullable=True)
    is_reminder_sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    lead = relationship("CrmLead", back_populates="followups")

class CrmPipeline(Base):
    __tablename__ = "crm_pipeline"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    stage_key = Column(String(50), nullable=False, index=True)
    stage_name = Column(String(100), nullable=False)
    order_index = Column(Integer, default=1, nullable=False)
    probability_percentage = Column(Float, default=10.0, nullable=False)
    is_won_stage = Column(Boolean, default=False, nullable=False)
    is_lost_stage = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CrmCampaign(Base):
    __tablename__ = "crm_campaigns"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    campaign_name = Column(String(200), nullable=False)
    channel = Column(String(50), nullable=False) # GOOGLE_ADS, FACEBOOK, INSTAGRAM, WHATSAPP, SMS, EMAIL, OFFLINE
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    allocated_budget = Column(Float, default=0.0, nullable=False)
    actual_spent = Column(Float, default=0.0, nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False) # DRAFT, ACTIVE, PAUSED, COMPLETED
    utm_source = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    results = relationship("CrmCampaignResult", back_populates="campaign", cascade="all, delete-orphan")

class CrmCampaignResult(Base):
    __tablename__ = "crm_campaign_results"
    id = Column(String(36), primary_key=True)
    campaign_id = Column(String(36), ForeignKey("crm_campaigns.id"), nullable=False, index=True)
    leads_generated = Column(Integer, default=0, nullable=False)
    admissions_converted = Column(Integer, default=0, nullable=False)
    revenue_generated = Column(Float, default=0.0, nullable=False)
    cost_per_lead = Column(Float, default=0.0, nullable=False)
    roi_percentage = Column(Float, default=0.0, nullable=False)
    recorded_date = Column(Date, default=date.today, nullable=False)

    campaign = relationship("CrmCampaign", back_populates="results")

class CrmLeadSource(Base):
    __tablename__ = "crm_lead_sources"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    source_name = Column(String(100), nullable=False)
    source_code = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    leads = relationship("CrmLead", back_populates="source")

class CrmReferral(Base):
    __tablename__ = "crm_referrals"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    referral_type = Column(String(30), default="STUDENT", nullable=False) # STUDENT, STAFF, PARTNER
    referrer_user_id = Column(String(36), nullable=True)
    referrer_name = Column(String(200), nullable=False)
    coupon_code = Column(String(50), unique=True, nullable=False, index=True)
    referred_lead_id = Column(String(36), ForeignKey("crm_leads.id"), nullable=True)
    commission_amount = Column(Float, default=0.0, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False) # PENDING, APPROVED, PAID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CrmTask(Base):
    __tablename__ = "crm_tasks"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to_user_id = Column(String(36), nullable=False, index=True)
    related_lead_id = Column(String(36), ForeignKey("crm_leads.id"), nullable=True)
    priority = Column(String(20), default="MEDIUM", nullable=False) # LOW, MEDIUM, HIGH, URGENT
    due_date = Column(DateTime, nullable=False, index=True)
    status = Column(String(30), default="PENDING", nullable=False) # PENDING, IN_PROGRESS, COMPLETED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CrmOpportunity(Base):
    __tablename__ = "crm_opportunities"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    lead_id = Column(String(36), ForeignKey("crm_leads.id"), nullable=False, index=True)
    deal_value = Column(Float, default=0.0, nullable=False)
    expected_revenue = Column(Float, default=0.0, nullable=False)
    probability_percentage = Column(Float, default=50.0, nullable=False)
    expected_closing_date = Column(Date, nullable=False)
    stage = Column(String(50), default="NEGOTIATION", nullable=False)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    lead = relationship("CrmLead", back_populates="opportunities")

class CrmActivityLog(Base):
    __tablename__ = "crm_activity_logs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    lead_id = Column(String(36), ForeignKey("crm_leads.id"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False)
    action_type = Column(String(50), nullable=False) # STAGE_CHANGED, CALL_LOGGED, EMAIL_SENT, TASK_CREATED
    description = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    lead = relationship("CrmLead", back_populates="activities")

class CrmReport(Base):
    __tablename__ = "crm_reports"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_name = Column(String(150), nullable=False)
    report_type = Column(String(50), nullable=False) # LEAD_SUMMARY, CONVERSION_AUDIT, CAMPAIGN_ROI, COUNSELLOR_PERF
    filters = Column(JSON, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CrmAnalytics(Base):
    __tablename__ = "crm_analytics"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    date_key = Column(Date, nullable=False, index=True)
    new_leads_count = Column(Integer, default=0, nullable=False)
    conversions_count = Column(Integer, default=0, nullable=False)
    total_pipeline_value = Column(Float, default=0.0, nullable=False)
    won_revenue = Column(Float, default=0.0, nullable=False)

class FranchiseCenter(Base):
    __tablename__ = "franchise_centers"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    center_code = Column(String(50), unique=True, nullable=False, index=True)
    center_name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    contact_email = Column(String(150), nullable=False)
    contact_phone = Column(String(30), nullable=False)
    royalty_percentage = Column(Float, default=15.0, nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False) # ACTIVE, SUSPENDED, PENDING
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    users = relationship("FranchiseUser", back_populates="center", cascade="all, delete-orphan")
    settings = relationship("FranchiseSetting", back_populates="center", cascade="all, delete-orphan")

class FranchiseUser(Base):
    __tablename__ = "franchise_users"
    id = Column(String(36), primary_key=True)
    center_id = Column(String(36), ForeignKey("franchise_centers.id"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    role = Column(String(50), default="COUNSELLOR", nullable=False) # CENTER_HEAD, COUNSELLOR, OPERATIONS
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    center = relationship("FranchiseCenter", back_populates="users")

class FranchiseSetting(Base):
    __tablename__ = "franchise_settings"
    id = Column(String(36), primary_key=True)
    center_id = Column(String(36), ForeignKey("franchise_centers.id"), nullable=False, index=True)
    setting_key = Column(String(100), nullable=False)
    setting_value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    center = relationship("FranchiseCenter", back_populates="settings")
