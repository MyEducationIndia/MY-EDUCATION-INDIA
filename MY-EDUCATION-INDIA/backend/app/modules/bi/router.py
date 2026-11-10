"""
Module 18: Enterprise Reports, Analytics & Business Intelligence (BI) Router
Mounted under /api/v1/bi
"""
import uuid
from datetime import datetime, timezone, date
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.modules.bi.schemas import (
    ReportDefinitionCreate, ReportDefinitionResponse,
    ReportScheduleCreate, ReportScheduleResponse,
    KpiDefinitionCreate, KpiDefinitionResponse,
    ChartDefinitionCreate, ChartDefinitionResponse,
    ExecutiveDashboardMetrics
)
from app.modules.bi.reports import get_prebuilt_templates
from app.modules.bi.system_health import SystemHealthMonitor

bi_router = APIRouter(prefix="/bi", tags=["Enterprise Reports, Analytics & Business Intelligence (BI)"])

_REPORTS_STORE = [
    {
        "id": "rep_01",
        "institute_id": "inst_mei_hq",
        "report_code": "REP-ADM-01",
        "report_name": "Admissions & Cohort Intake Analytics",
        "category": "ADMISSION",
        "description": "Comprehensive enrollment funnel analysis, seat matrix fill rate, and regional demographic distribution.",
        "source_tables": ["admissions_applications", "crm_leads"],
        "is_system_report": True,
        "is_active": True,
        "created_at": "2026-11-01T10:00:00Z"
    },
    {
        "id": "rep_02",
        "institute_id": "inst_mei_hq",
        "report_code": "REP-FEE-01",
        "report_name": "Tuition Fee Collection & Aging Ledger",
        "category": "FINANCIAL",
        "description": "Term-wise fee demands, scholarship concessions, late dues, and GST receipt reconciliation.",
        "source_tables": ["fee_invoices", "fee_payments"],
        "is_system_report": True,
        "is_active": True,
        "created_at": "2026-11-01T10:00:00Z"
    },
    {
        "id": "rep_03",
        "institute_id": "inst_mei_hq",
        "report_code": "REP-EXAM-01",
        "report_name": "Semester Examination Performance & SGPA Matrix",
        "category": "ACADEMIC",
        "description": "CBT test scores, course-wise pass percentiles, backlog trends, and honors roll eligibility.",
        "source_tables": ["exam_marks", "cbt_attempts"],
        "is_system_report": True,
        "is_active": True,
        "created_at": "2026-11-02T11:00:00Z"
    },
    {
        "id": "rep_04",
        "institute_id": "inst_mei_hq",
        "report_code": "REP-NAAC-NIRF",
        "report_name": "NAAC & NIRF Institutional Quality Audit",
        "category": "REGULATORY",
        "description": "TLR metrics, faculty-student ratio (1:15), Ph.D. publications count, and placement compensation benchmarks.",
        "source_tables": ["faculty_members", "placements_stats", "research_publications"],
        "is_system_report": True,
        "is_active": True,
        "created_at": "2026-11-03T12:00:00Z"
    }
]

_KPIS_STORE = [
    {
        "id": "kpi_01",
        "institute_id": "inst_mei_hq",
        "kpi_key": "FEE_COLLECTION_PCT",
        "kpi_name": "Fee Collection Efficiency",
        "category": "FINANCIAL",
        "calculation_formula": "collected / demanded * 100",
        "target_value": 90.0,
        "current_value": 87.2,
        "warning_threshold": 80.0,
        "critical_threshold": 70.0,
        "unit": "%",
        "trend_direction": "UP"
    },
    {
        "id": "kpi_02",
        "institute_id": "inst_mei_hq",
        "kpi_key": "STUDENT_ATTENDANCE_PCT",
        "kpi_name": "Aggregate Student Attendance",
        "category": "ACADEMIC",
        "calculation_formula": "present_sessions / total_sessions * 100",
        "target_value": 85.0,
        "current_value": 91.5,
        "warning_threshold": 75.0,
        "critical_threshold": 65.0,
        "unit": "%",
        "trend_direction": "UP"
    },
    {
        "id": "kpi_03",
        "institute_id": "inst_mei_hq",
        "kpi_key": "CAMPUS_PLACEMENT_PCT",
        "kpi_name": "Placement Conversion Percentage",
        "category": "CAREERS",
        "calculation_formula": "placed_students / eligible_students * 100",
        "target_value": 95.0,
        "current_value": 96.2,
        "warning_threshold": 85.0,
        "critical_threshold": 75.0,
        "unit": "%",
        "trend_direction": "UP"
    },
    {
        "id": "kpi_04",
        "institute_id": "inst_mei_hq",
        "kpi_key": "FACULTY_STUDENT_RATIO",
        "kpi_name": "Faculty to Student Ratio (AICTE)",
        "category": "ACADEMIC",
        "calculation_formula": "total_students / total_faculty",
        "target_value": 15.0,
        "current_value": 14.8,
        "warning_threshold": 18.0,
        "critical_threshold": 20.0,
        "unit": ":1",
        "trend_direction": "STABLE"
    }
]

@bi_router.get("/health")
async def bi_health():
    return {
        "status": "healthy",
        "module": "Module 18: Business Intelligence, Analytics & Executive Reporting",
        "campus": "MEI-HQ Indore",
        "reports_count": len(_REPORTS_STORE),
        "kpis_monitored": len(_KPIS_STORE),
    }

@bi_router.get("/dashboard/executive", response_model=ExecutiveDashboardMetrics)
async def get_executive_dashboard(institute_id: str = "inst_mei_hq"):
    return {
        "admissions_count": 1420,
        "total_revenue_inr": 84500000.0,
        "pending_fees_inr": 12400000.0,
        "fee_collection_rate_percentage": 87.2,
        "average_attendance_percentage": 91.5,
        "exam_pass_percentage": 94.8,
        "active_course_enrollments": 3850,
        "lead_conversion_rate_percentage": 34.2,
        "institute_health_score": 92.4
    }

@bi_router.get("/kpis")
async def list_kpis():
    return _KPIS_STORE

@bi_router.post("/kpis", status_code=status.HTTP_201_CREATED)
async def create_kpi(payload: Dict[str, Any]):
    new_id = f"kpi_{uuid.uuid4().hex[:6]}"
    new_kpi = {
        "id": new_id,
        "institute_id": "inst_mei_hq",
        "kpi_key": payload.get("kpi_key", "CUSTOM_KPI"),
        "kpi_name": payload.get("kpi_name", "Custom Institutional Metric"),
        "category": payload.get("category", "OPERATIONS"),
        "calculation_formula": payload.get("calculation_formula", "metric / target * 100"),
        "target_value": float(payload.get("target_value", 100.0)),
        "current_value": float(payload.get("current_value", 85.0)),
        "warning_threshold": float(payload.get("warning_threshold", 75.0)),
        "critical_threshold": float(payload.get("critical_threshold", 65.0)),
        "unit": payload.get("unit", "%"),
        "trend_direction": "UP",
    }
    _KPIS_STORE.append(new_kpi)
    return new_kpi

@bi_router.get("/reports")
async def list_reports(category: Optional[str] = None):
    if category and category.upper() != "ALL":
        return [r for r in _REPORTS_STORE if r["category"].upper() == category.upper()]
    return _REPORTS_STORE

@bi_router.post("/reports", status_code=status.HTTP_201_CREATED)
async def create_report(payload: Dict[str, Any]):
    new_id = f"rep_{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    new_rep = {
        "id": new_id,
        "institute_id": "inst_mei_hq",
        "report_code": payload.get("report_code", f"REP-CUST-{len(_REPORTS_STORE) + 1}"),
        "report_name": payload.get("report_name", "Custom Executive Report"),
        "category": payload.get("category", "ACADEMIC"),
        "description": payload.get("description", "Custom institutional audit report"),
        "source_tables": payload.get("source_tables", ["admissions_applications"]),
        "is_system_report": False,
        "is_active": True,
        "created_at": now_iso,
    }
    _REPORTS_STORE.append(new_rep)
    return new_rep

@bi_router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str):
    global _REPORTS_STORE
    _REPORTS_STORE = [r for r in _REPORTS_STORE if r["id"] != report_id]
    return None

@bi_router.get("/templates")
async def list_report_templates():
    return get_prebuilt_templates()

@bi_router.get("/charts/trends")
async def get_chart_trends():
    return {
        "monthly_revenue": [
            {"month": "Jun 2025", "revenue": 14200000, "collections": 12800000},
            {"month": "Jul 2025", "revenue": 18500000, "collections": 16400000},
            {"month": "Aug 2025", "revenue": 21000000, "collections": 19200000},
            {"month": "Sep 2025", "revenue": 11000000, "collections": 9800000},
            {"month": "Oct 2025", "revenue": 9500000, "collections": 8900000},
            {"month": "Nov 2025", "revenue": 10300000, "collections": 9400000},
        ],
        "attendance_distribution": [
            {"range": "> 90% (Distinction)", "percentage": 64.2},
            {"range": "75% - 90% (Good)", "percentage": 27.5},
            {"range": "65% - 75% (Shortage Warning)", "percentage": 6.1},
            {"range": "< 65% (Critical Shortage)", "percentage": 2.2},
        ],
        "placement_package_distribution": [
            {"tier": "Tier 1: > ₹20 LPA (Super Dream)", "count": 48},
            {"tier": "Tier 2: ₹12 - ₹20 LPA (Dream)", "count": 112},
            {"tier": "Tier 3: ₹6 - ₹12 LPA (Prime)", "count": 165},
            {"tier": "Tier 4: < ₹6 LPA (Core)", "count": 35},
        ]
    }

@bi_router.get("/cohort-retention")
async def get_cohort_retention():
    return {
        "academic_cohort": "2022-2026 Batch",
        "initial_intake": 480,
        "year_1_retention": 98.4,
        "year_2_retention": 96.8,
        "year_3_retention": 95.2,
        "year_4_on_track": 94.6,
        "dropout_rate": 2.8,
        "lateral_entry_additions": 32,
        "remedial_support_sessions": 140,
    }

@bi_router.get("/nirf-naac-dossier")
async def get_nirf_naac_dossier():
    return {
        "naac_grade": "A+",
        "cgpa": 3.68,
        "nirf_score_breakdown": {
            "TLR_Teaching_Learning_Resources": 84.5,
            "RP_Research_Professional_Practice": 78.2,
            "GO_Graduation_Outcomes": 91.0,
            "OI_Outreach_Inclusivity": 82.4,
            "PR_Perception": 76.5,
        },
        "faculty_phd_percentage": 78.5,
        "scopus_wos_papers_indexed": 340,
        "annual_research_grant_inr": 28500000.0,
        "median_salary_inr": 1280000.0,
        "highest_package_inr": 5200000.0,
    }

@bi_router.get("/system-health")
async def get_system_health():
    return SystemHealthMonitor.get_cluster_health_overview()

@bi_router.post("/reports/{report_id}/export")
async def export_report(report_id: str, payload: Dict[str, Any]):
    return {
        "status": "GENERATED",
        "report_id": report_id,
        "format": payload.get("format", "PDF"),
        "download_url": f"/api/v1/downloads/reports/{report_id}.pdf",
        "file_size": "2.4 MB",
        "generated_timestamp": datetime.now(timezone.utc).isoformat(),
        "digital_signature_hash": "sha256=9b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7",
    }
