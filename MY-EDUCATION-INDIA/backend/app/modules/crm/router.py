"""
Module 17: Enterprise CRM, Sales, Marketing & Franchise Management Router
Mounted under /api/v1/crm
"""
import uuid
from datetime import datetime, timezone, date
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.modules.crm.schemas import (
    CrmLeadCreate, CrmLeadResponse,
    CrmEnquiryCreate, CrmEnquiryResponse,
    CrmFollowupCreate, CrmFollowupResponse,
    CrmCampaignCreate, CrmCampaignResponse,
    CrmReferralCreate, CrmReferralResponse,
    CrmTaskCreate, CrmTaskResponse,
    CrmOpportunityCreate, CrmOpportunityResponse,
    FranchiseCenterCreate, FranchiseCenterResponse,
    CrmDashboardMetrics
)

crm_router = APIRouter(prefix="/crm", tags=["Enterprise CRM, Sales, Marketing & Franchise"])

# In-memory mock store for dynamic CRUD in autonomous campus environment
_LEADS_STORE = [
    {
        "id": "lead_01",
        "institute_id": "inst_mei_hq",
        "lead_code": "LEAD-2026-081",
        "full_name": "Aarav Sharma",
        "mobile": "+91 98765 43210",
        "email": "aarav.sharma@example.com",
        "guardian_name": "Rajesh Sharma",
        "course_interested_id": "B.Tech Computer Science & Engineering",
        "source_id": "Website Admission Inquiry",
        "priority": "HIGH",
        "assigned_counsellor_id": "Dr. Anita Desai",
        "stage": "COUNSELLING",
        "status": "ACTIVE",
        "score": 88,
        "remarks": "JEE Main 96.4 percentile. Highly interested in AI/ML track.",
        "is_active": True,
        "created_at": "2026-11-02T10:00:00Z",
        "updated_at": "2026-11-09T14:30:00Z"
    },
    {
        "id": "lead_02",
        "institute_id": "inst_mei_hq",
        "lead_code": "LEAD-2026-082",
        "full_name": "Ananya Patel",
        "mobile": "+91 98765 43211",
        "email": "ananya.patel@example.com",
        "guardian_name": "Suresh Patel",
        "course_interested_id": "B.Tech Electronics & Communication",
        "source_id": "Google Ads Campaign",
        "priority": "URGENT",
        "assigned_counsellor_id": "Prof. Vikram Malhotra",
        "stage": "FEE_DISCUSSION",
        "status": "ACTIVE",
        "score": 94,
        "remarks": "Documents verified. Discussing merit scholarship concession.",
        "is_active": True,
        "created_at": "2026-11-03T11:30:00Z",
        "updated_at": "2026-11-09T15:00:00Z"
    },
    {
        "id": "lead_03",
        "institute_id": "inst_mei_hq",
        "lead_code": "LEAD-2026-083",
        "full_name": "Rohan Gupta",
        "mobile": "+91 98765 43222",
        "email": "rohan.gupta@example.com",
        "guardian_name": "Manoj Gupta",
        "course_interested_id": "MBA in Technology Management",
        "source_id": "Indore Education Expo",
        "priority": "MEDIUM",
        "assigned_counsellor_id": "Dr. Anita Desai",
        "stage": "NEW_LEAD",
        "status": "ACTIVE",
        "score": 65,
        "remarks": "CAT 84 percentile. Requested campus brochure and syllabus.",
        "is_active": True,
        "created_at": "2026-11-05T09:00:00Z",
        "updated_at": "2026-11-05T09:00:00Z"
    },
    {
        "id": "lead_04",
        "institute_id": "inst_mei_hq",
        "lead_code": "LEAD-2026-084",
        "full_name": "Siddharth Joshi",
        "mobile": "+91 98765 43233",
        "email": "siddharth.joshi@example.com",
        "guardian_name": "Deepak Joshi",
        "course_interested_id": "M.Tech in Cloud & AI",
        "source_id": "Direct Walk-in",
        "priority": "HIGH",
        "assigned_counsellor_id": "Prof. Vikram Malhotra",
        "stage": "ADMISSION_CONFIRMED",
        "status": "CONVERTED",
        "score": 98,
        "remarks": "Admission fee paid. Biometric student registration completed.",
        "is_active": True,
        "created_at": "2026-11-01T14:00:00Z",
        "updated_at": "2026-11-08T16:20:00Z"
    }
]

_CAMPAIGNS_STORE = [
    {
        "id": "cmp_01",
        "institute_id": "inst_mei_hq",
        "campaign_name": "Engineering Admissions 2026-27 - Google Ads",
        "channel": "GOOGLE_ADS",
        "start_date": "2026-11-01",
        "end_date": "2026-12-31",
        "allocated_budget": 250000.0,
        "actual_spent": 84500.0,
        "status": "ACTIVE",
        "utm_source": "google",
        "utm_campaign": "btech_2026_indore",
        "leads_generated": 142,
        "conversions": 28,
        "created_at": "2026-11-01T08:00:00Z"
    },
    {
        "id": "cmp_02",
        "institute_id": "inst_mei_hq",
        "campaign_name": "Meta Instagram & Facebook Reels Campaign",
        "channel": "META_ADS",
        "start_date": "2026-11-05",
        "end_date": "2026-12-15",
        "allocated_budget": 120000.0,
        "actual_spent": 38200.0,
        "status": "ACTIVE",
        "utm_source": "instagram",
        "utm_campaign": "campus_tour_reels",
        "leads_generated": 86,
        "conversions": 14,
        "created_at": "2026-11-05T10:00:00Z"
    },
    {
        "id": "cmp_03",
        "institute_id": "inst_mei_hq",
        "campaign_name": "Central India Scholarship Awareness Drive",
        "channel": "OFFLINE_EVENTS",
        "start_date": "2026-10-15",
        "end_date": "2026-11-30",
        "allocated_budget": 180000.0,
        "actual_spent": 145000.0,
        "status": "ACTIVE",
        "utm_source": "regional_fairs",
        "utm_campaign": "scholarship_drive",
        "leads_generated": 210,
        "conversions": 45,
        "created_at": "2026-10-15T09:00:00Z"
    }
]

_FRANCHISE_CENTERS_STORE = [
    {
        "id": "fc_01",
        "institute_id": "inst_mei_hq",
        "center_code": "FC-IND-01",
        "center_name": "Indore Vijay Nagar Learning & Counseling Center",
        "city": "Indore",
        "state": "Madhya Pradesh",
        "contact_email": "vijaynagar@mei-centers.in",
        "contact_phone": "+91 731 299 1101",
        "royalty_percentage": 15.0,
        "active_students": 140,
        "revenue_generated": 3850000.0,
        "status": "ACTIVE",
        "created_at": "2026-10-01T10:00:00Z"
    },
    {
        "id": "fc_02",
        "institute_id": "inst_mei_hq",
        "center_code": "FC-BHO-02",
        "center_name": "Bhopal MP Nagar Regional Outreach Center",
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "contact_email": "bhopal@mei-centers.in",
        "contact_phone": "+91 755 288 2202",
        "royalty_percentage": 15.0,
        "active_students": 95,
        "revenue_generated": 2600000.0,
        "status": "ACTIVE",
        "created_at": "2026-10-15T10:00:00Z"
    },
    {
        "id": "fc_03",
        "institute_id": "inst_mei_hq",
        "center_code": "FC-JAB-03",
        "center_name": "Jabalpur Mahakaushal Academic Center",
        "city": "Jabalpur",
        "state": "Madhya Pradesh",
        "contact_email": "jabalpur@mei-centers.in",
        "contact_phone": "+91 761 277 3303",
        "royalty_percentage": 12.5,
        "active_students": 62,
        "revenue_generated": 1750000.0,
        "status": "ACTIVE",
        "created_at": "2026-11-01T10:00:00Z"
    }
]

_FOLLOWUPS_STORE = [
    {
        "id": "fol_01",
        "lead_id": "lead_01",
        "counsellor_name": "Dr. Anita Desai",
        "channel": "CALL",
        "scheduled_at": "2026-11-10T10:30:00Z",
        "notes": "Discussed CSE syllabus and lab facilities. Parent asked for fee installment options.",
        "outcome": "INTERESTED",
        "next_followup_date": "2026-11-12T11:00:00Z",
    },
    {
        "id": "fol_02",
        "lead_id": "lead_02",
        "counsellor_name": "Prof. Vikram Malhotra",
        "channel": "WHATSAPP",
        "scheduled_at": "2026-11-09T16:00:00Z",
        "notes": "Sent digital scholarship concession letter and hostel brochure.",
        "outcome": "ADMISSION_PROMISED",
        "next_followup_date": "2026-11-11T14:00:00Z",
    }
]

PIPELINE_STAGES = [
    {"stage_key": "NEW_LEAD", "stage_name": "New Inquiries", "order_index": 1, "probability": 10},
    {"stage_key": "CONTACTED", "stage_name": "First Contact", "order_index": 2, "probability": 25},
    {"stage_key": "COUNSELLING", "stage_name": "Academic Counselling", "order_index": 3, "probability": 50},
    {"stage_key": "FEE_DISCUSSION", "stage_name": "Fee & Concession", "order_index": 4, "probability": 75},
    {"stage_key": "ADMISSION_CONFIRMED", "stage_name": "Confirmed Admission", "order_index": 5, "probability": 100},
    {"stage_key": "LOST", "stage_name": "Dropped / Ineligible", "order_index": 6, "probability": 0},
]

@crm_router.get("/health")
async def crm_health():
    return {
        "status": "healthy",
        "module": "Module 17: Enterprise CRM, Marketing Automation & Franchise Management",
        "campus": "MEI-HQ Indore",
        "pipeline_stages_count": len(PIPELINE_STAGES),
        "total_active_leads": len(_LEADS_STORE),
        "active_franchise_centers": len(_FRANCHISE_CENTERS_STORE),
    }

@crm_router.get("/dashboard")
async def get_crm_dashboard(institute_id: str = "inst_mei_hq"):
    return {
        "total_new_leads": len(_LEADS_STORE),
        "todays_followups_count": len(_FOLLOWUPS_STORE),
        "admissions_this_month": len([l for l in _LEADS_STORE if l["stage"] == "ADMISSION_CONFIRMED"]),
        "conversion_rate_percentage": 34.2,
        "revenue_forecast": 8200000.0,
        "top_counsellor": "Dr. Anita Desai (22 Conversions)",
        "active_campaigns_count": len(_CAMPAIGNS_STORE),
        "pending_tasks_count": 8,
    }

@crm_router.get("/pipeline/stages")
async def get_pipeline_stages():
    return PIPELINE_STAGES

# Leads Endpoints
@crm_router.get("/leads")
async def list_leads(stage: Optional[str] = None, q: Optional[str] = None):
    res = _LEADS_STORE
    if stage and stage.upper() != "ALL":
        res = [l for l in res if l["stage"].upper() == stage.upper()]
    if q and q.strip():
        q_clean = q.strip().lower()
        res = [
            l for l in res
            if q_clean in l["full_name"].lower()
            or q_clean in l["mobile"]
            or q_clean in (l.get("email") or "").lower()
            or q_clean in l.get("lead_code", "").lower()
        ]
    return res

@crm_router.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(payload: Dict[str, Any]):
    new_id = f"lead_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    new_lead = {
        "id": new_id,
        "institute_id": "inst_mei_hq",
        "lead_code": f"LEAD-2026-{len(_LEADS_STORE) + 85}",
        "full_name": payload.get("full_name", "Prospective Student"),
        "mobile": payload.get("mobile", ""),
        "email": payload.get("email"),
        "guardian_name": payload.get("guardian_name"),
        "course_interested_id": payload.get("course_interested_id", "B.Tech Computer Science"),
        "source_id": payload.get("source_id", "Website Form"),
        "priority": payload.get("priority", "MEDIUM"),
        "assigned_counsellor_id": payload.get("assigned_counsellor_id", "Dr. Anita Desai"),
        "stage": payload.get("stage", "NEW_LEAD"),
        "status": "ACTIVE",
        "score": payload.get("score", 70),
        "remarks": payload.get("remarks"),
        "is_active": True,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    _LEADS_STORE.insert(0, new_lead)
    return new_lead

@crm_router.patch("/leads/{lead_id}")
async def update_lead(lead_id: str, payload: Dict[str, Any]):
    for lead in _LEADS_STORE:
        if lead["id"] == lead_id:
            for k, v in payload.items():
                if v is not None:
                    lead[k] = v
            lead["updated_at"] = datetime.now(timezone.utc).isoformat()
            return lead
    raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")

@crm_router.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(lead_id: str):
    global _LEADS_STORE
    _LEADS_STORE = [l for l in _LEADS_STORE if l["id"] != lead_id]
    return None

# Followups
@crm_router.get("/followups")
async def list_followups(lead_id: Optional[str] = None):
    if lead_id:
        return [f for f in _FOLLOWUPS_STORE if f.get("lead_id") == lead_id]
    return _FOLLOWUPS_STORE

@crm_router.post("/followups", status_code=status.HTTP_201_CREATED)
async def create_followup(payload: Dict[str, Any]):
    new_id = f"fol_{uuid.uuid4().hex[:6]}"
    new_fol = {
        "id": new_id,
        "lead_id": payload.get("lead_id"),
        "counsellor_name": payload.get("counsellor_name", "Academic Counsellor"),
        "channel": payload.get("channel", "CALL"),
        "scheduled_at": payload.get("scheduled_at", datetime.now(timezone.utc).isoformat()),
        "notes": payload.get("notes"),
        "outcome": payload.get("outcome", "INTERESTED"),
        "next_followup_date": payload.get("next_followup_date"),
    }
    _FOLLOWUPS_STORE.insert(0, new_fol)
    return new_fol

# Campaigns Endpoints
@crm_router.get("/campaigns")
async def list_campaigns():
    return _CAMPAIGNS_STORE

@crm_router.post("/campaigns", status_code=status.HTTP_201_CREATED)
async def create_campaign(payload: Dict[str, Any]):
    new_id = f"cmp_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    new_cmp = {
        "id": new_id,
        "institute_id": "inst_mei_hq",
        "campaign_name": payload.get("campaign_name", "Admission Campaign"),
        "channel": payload.get("channel", "GOOGLE_ADS"),
        "start_date": payload.get("start_date", str(date.today())),
        "end_date": payload.get("end_date"),
        "allocated_budget": float(payload.get("allocated_budget", 50000.0)),
        "actual_spent": 0.0,
        "status": "ACTIVE",
        "utm_source": payload.get("utm_source", "admissions"),
        "utm_campaign": payload.get("utm_campaign", "campaign_2026"),
        "leads_generated": 0,
        "conversions": 0,
        "created_at": now_iso,
    }
    _CAMPAIGNS_STORE.insert(0, new_cmp)
    return new_cmp

@crm_router.delete("/campaigns/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(campaign_id: str):
    global _CAMPAIGNS_STORE
    _CAMPAIGNS_STORE = [c for c in _CAMPAIGNS_STORE if c["id"] != campaign_id]
    return None

# Franchise Centers Endpoints
@crm_router.get("/franchise/centers")
async def list_franchise_centers():
    return _FRANCHISE_CENTERS_STORE

@crm_router.post("/franchise/centers", status_code=status.HTTP_201_CREATED)
async def create_franchise_center(payload: Dict[str, Any]):
    new_id = f"fc_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    new_fc = {
        "id": new_id,
        "institute_id": "inst_mei_hq",
        "center_code": payload.get("center_code", f"FC-CTR-{len(_FRANCHISE_CENTERS_STORE) + 1}"),
        "center_name": payload.get("center_name", "Regional Counseling Center"),
        "city": payload.get("city", "Indore"),
        "state": payload.get("state", "Madhya Pradesh"),
        "contact_email": payload.get("contact_email", "center@mei-centers.in"),
        "contact_phone": payload.get("contact_phone", "+91 731 200 0000"),
        "royalty_percentage": float(payload.get("royalty_percentage", 15.0)),
        "active_students": 0,
        "revenue_generated": 0.0,
        "status": "ACTIVE",
        "created_at": now_iso,
    }
    _FRANCHISE_CENTERS_STORE.append(new_fc)
    return new_fc

@crm_router.delete("/franchise/centers/{center_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_franchise_center(center_id: str):
    global _FRANCHISE_CENTERS_STORE
    _FRANCHISE_CENTERS_STORE = [fc for fc in _FRANCHISE_CENTERS_STORE if fc["id"] != center_id]
    return None
