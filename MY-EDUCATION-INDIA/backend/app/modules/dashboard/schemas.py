import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ==================== Dashboard Statistics ====================
class DashboardKPIStatistics(BaseModel):
    # Student & Academic
    total_students: int = 0
    active_students: int = 0
    admissions_today: int = 0
    admissions_this_month: int = 0
    total_faculty: int = 0
    total_courses: int = 0
    total_batches: int = 0
    total_branches: int = 0

    # Financial & Fees (INR)
    fee_collection_today: float = 0.0
    fee_collection_this_month: float = 0.0
    pending_fees_total: float = 0.0

    # Academic Performance & CBT
    overall_attendance_pct: float = 0.0
    examinations_conducted: int = 0
    certificates_issued: int = 0

    # Operational & Communication
    website_visitors_today: int = 0
    unread_notifications_count: int = 0
    sms_sent_count: int = 0
    whatsapp_sent_count: int = 0
    emails_sent_count: int = 0

    # System Status Indicators
    database_status: str = "ONLINE"
    server_status: str = "HEALTHY"
    api_status: str = "OPERATIONAL"
    storage_usage_mb: float = 0.0
    last_backup_at: Optional[datetime] = None


# ==================== Analytics Series ====================
class TimeSeriesDataPoint(BaseModel):
    timestamp: str # Date label e.g. "2026-11-01" or "09:00"
    label: str
    value: float
    secondary_value: Optional[float] = None
    category: Optional[str] = None


class ChartSeriesResponse(BaseModel):
    metric_name: str
    granularity: str # DAILY, WEEKLY, MONTHLY, YEARLY, CUSTOM
    start_date: str
    end_date: str
    data_points: List[TimeSeriesDataPoint]
    summary_total: float
    growth_rate_pct: Optional[float] = None


class CategoryDistributionItem(BaseModel):
    name: str
    count: int
    percentage: float
    color_hex: Optional[str] = None


class MultiChartAnalyticsResponse(BaseModel):
    admission_trends: List[TimeSeriesDataPoint]
    fee_collection: List[TimeSeriesDataPoint]
    attendance_trends: List[TimeSeriesDataPoint]
    student_growth: List[TimeSeriesDataPoint]
    course_popularity: List[CategoryDistributionItem]
    channel_statistics: Dict[str, int]
    branch_comparison: List[CategoryDistributionItem]


# ==================== Global Search ====================
class SearchResultItem(BaseModel):
    entity_type: str # student, faculty, course, fee_receipt, certificate, admission, user, setting
    title: str
    subtitle: Optional[str] = None
    identifier: str
    target_url: str
    status_badge: Optional[str] = None
    created_at: Optional[datetime] = None


class GlobalSearchResponse(BaseModel):
    query: str
    total_results: int
    grouped_results: Dict[str, List[SearchResultItem]]


# ==================== Activity Timeline ====================
class ActivityItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    actor_name: str
    action_type: str
    entity_type: str
    entity_id: Optional[str] = None
    summary: str
    detail_payload: Dict[str, Any]
    occurred_at: datetime


# ==================== Notification Center ====================
class NotificationItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    message: str
    category: str
    priority: str
    action_url: Optional[str] = None
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime


class NotificationCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=3)
    category: str = "SYSTEM"
    priority: str = "NORMAL"
    action_url: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    institute_id: Optional[uuid.UUID] = None
    meta_data: Dict[str, Any] = Field(default_factory=dict)


# ==================== Configurable Widgets ====================
class WidgetConfigItem(BaseModel):
    widget_key: str
    title: str
    category: str
    grid_position: int
    grid_width: int # 1 to 12
    grid_height: int
    is_visible: bool
    is_pinned: bool
    configuration: Dict[str, Any] = Field(default_factory=dict)


class UpdateWidgetsBatchRequest(BaseModel):
    widgets: List[WidgetConfigItem]


# ==================== System Health ====================
class SystemHealthResponse(BaseModel):
    database_status: str
    database_version: str
    api_status: str
    server_time: str
    uptime_seconds: float
    memory_usage_mb: float
    total_memory_mb: float
    cpu_percent: float
    storage_usage_mb: float
    active_db_connections: int
    last_backup_time: Optional[str] = None
    app_version: str = "2.0.0"
    environment: str = "production"
