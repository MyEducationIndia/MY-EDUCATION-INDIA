"""
Module 18: BI Schemas (Pydantic v2 / v1 compatible)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

class ReportDefinitionBase(BaseModel):
    report_code: str = Field(..., max_length=50)
    report_name: str = Field(..., max_length=200)
    category: str = "ACADEMIC" # ACADEMIC, FINANCIAL, ADMISSION, ATTENDANCE, EXAM, LXP, CRM, SYSTEM
    description: Optional[str] = None
    source_tables: List[str]
    selected_fields: List[Dict[str, Any]]
    filter_config: Optional[List[Dict[str, Any]]] = None
    aggregation_config: Optional[List[Dict[str, Any]]] = None
    sort_config: Optional[List[Dict[str, Any]]] = None
    is_system_report: bool = False
    is_active: bool = True

class ReportDefinitionCreate(ReportDefinitionBase):
    pass

class ReportDefinitionResponse(ReportDefinitionBase):
    id: str
    institute_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReportScheduleCreate(BaseModel):
    report_id: str
    frequency: str = "WEEKLY" # DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY
    cron_expression: str
    export_format: str = "PDF" # PDF, EXCEL, CSV, DOCX
    delivery_channel: str = "EMAIL" # EMAIL, WHATSAPP, SYSTEM_NOTIFICATION
    recipient_list: List[str]
    is_active: bool = True

class ReportScheduleResponse(ReportScheduleCreate):
    id: str
    institute_id: str
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True

class KpiDefinitionCreate(BaseModel):
    kpi_key: str = Field(..., max_length=60)
    kpi_name: str = Field(..., max_length=150)
    category: str
    calculation_formula: str
    target_value: float
    warning_threshold: float
    critical_threshold: float
    unit: str = "%"

class KpiDefinitionResponse(KpiDefinitionCreate):
    id: str
    institute_id: str
    current_value: float
    trend_direction: str
    updated_at: datetime

    class Config:
        orm_mode = True

class ChartDefinitionCreate(BaseModel):
    chart_name: str = Field(..., max_length=150)
    chart_type: str = "BAR" # BAR, LINE, AREA, PIE, DONUT, STACKED, RADAR, SCATTER, HEATMAP, GAUGE, FUNNEL, TREEMAP
    config_options_json: Dict[str, Any]

class ChartDefinitionResponse(ChartDefinitionCreate):
    id: str
    institute_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class ExecutiveDashboardMetrics(BaseModel):
    admissions_count: int
    total_revenue_inr: float
    pending_fees_inr: float
    fee_collection_rate_percentage: float
    average_attendance_percentage: float
    exam_pass_percentage: float
    active_course_enrollments: int
    lead_conversion_rate_percentage: float
    institute_health_score: float # 0 - 100
