"""
Module 18: Enterprise Reports, Analytics & BI - Models
Provisions 14 enterprise tables for centralized reporting, KPIs, charts,
dashboard layouts, schedules, system health, and exports.
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class ReportDefinition(Base):
    __tablename__ = "report_definitions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_code = Column(String(50), nullable=False, index=True)
    report_name = Column(String(200), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True) # ACADEMIC, FINANCIAL, ADMISSION, ATTENDANCE, EXAM, LXP, CRM, SYSTEM
    description = Column(Text, nullable=True)
    source_tables = Column(JSON, nullable=False) # ["crm_leads", "admissions_applications"]
    selected_fields = Column(JSON, nullable=False) # [{"table": "crm_leads", "field": "full_name", "alias": "Name"}]
    filter_config = Column(JSON, nullable=True) # [{"field": "stage", "op": "==", "value": "ADMISSION_CONFIRMED"}]
    aggregation_config = Column(JSON, nullable=True) # [{"field": "fee_amount", "func": "SUM"}]
    sort_config = Column(JSON, nullable=True) # [{"field": "created_at", "dir": "DESC"}]
    is_system_report = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    schedules = relationship("ReportSchedule", back_populates="report", cascade="all, delete-orphan")
    saved_instances = relationship("SavedReport", back_populates="report", cascade="all, delete-orphan")

class ReportTemplate(Base):
    __tablename__ = "report_templates"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    template_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    layout_type = Column(String(30), default="TABULAR", nullable=False) # TABULAR, PIVOT, SUMMARY, EXECUTIVE_BRIEF
    definition_json = Column(JSON, nullable=False)
    is_prebuilt = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_id = Column(String(36), ForeignKey("report_definitions.id"), nullable=False, index=True)
    frequency = Column(String(30), default="WEEKLY", nullable=False) # DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY
    cron_expression = Column(String(50), nullable=False)
    export_format = Column(String(20), default="PDF", nullable=False) # PDF, EXCEL, CSV, DOCX
    delivery_channel = Column(String(30), default="EMAIL", nullable=False) # EMAIL, WHATSAPP, SYSTEM_NOTIFICATION
    recipient_list = Column(JSON, nullable=False) # ["principal@myeducation.in", "director@myeducation.in"]
    is_active = Column(Boolean, default=True, nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    report = relationship("ReportDefinition", back_populates="schedules")

class SavedReport(Base):
    __tablename__ = "saved_reports"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_id = Column(String(36), ForeignKey("report_definitions.id"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False)
    name = Column(String(200), nullable=False)
    snapshot_data_json = Column(JSON, nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    report = relationship("ReportDefinition", back_populates="saved_instances")

class DashboardWidget(Base):
    __tablename__ = "dashboard_widgets"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    widget_key = Column(String(60), nullable=False, index=True)
    widget_name = Column(String(150), nullable=False)
    widget_type = Column(String(30), default="METRIC_CARD", nullable=False) # METRIC_CARD, CHART, DATA_TABLE, KPI_GAUGE, HEALTH_MONITOR
    data_source_query = Column(String(100), nullable=False)
    refresh_interval_seconds = Column(Integer, default=60, nullable=False)
    config_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class DashboardLayout(Base):
    __tablename__ = "dashboard_layouts"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    dashboard_type = Column(String(50), default="EXECUTIVE", nullable=False) # EXECUTIVE, ACADEMIC, FINANCIAL, OPERATIONS
    layout_grid_json = Column(JSON, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class KpiDefinition(Base):
    __tablename__ = "kpi_definitions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    kpi_key = Column(String(60), nullable=False, index=True)
    kpi_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    calculation_formula = Column(String(255), nullable=False) # e.g. "admissions_confirmed / total_leads * 100"
    target_value = Column(Float, nullable=False)
    warning_threshold = Column(Float, nullable=False)
    critical_threshold = Column(Float, nullable=False)
    unit = Column(String(30), default="%", nullable=False) # %, INR, COUNT, DAYS
    current_value = Column(Float, default=0.0, nullable=False)
    trend_direction = Column(String(10), default="UP", nullable=False) # UP, DOWN, STABLE
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    snapshot_date = Column(Date, nullable=False, index=True)
    domain = Column(String(50), nullable=False) # ENROLLMENT, REVENUE, ATTENDANCE, PERFORMANCE
    metrics_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class SystemHealthLog(Base):
    __tablename__ = "system_health_logs"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    component_name = Column(String(50), nullable=False, index=True) # API_GATEWAY, DATABASE, BACKGROUND_WORKER, CACHE, STORAGE, EMAIL_QUEUE
    status = Column(String(20), default="HEALTHY", nullable=False) # HEALTHY, DEGRADED, DOWN
    latency_ms = Column(Float, default=0.0, nullable=False)
    error_rate_percentage = Column(Float, default=0.0, nullable=False)
    details_json = Column(JSON, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class AuditReport(Base):
    __tablename__ = "audit_reports"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_id = Column(String(36), nullable=False, index=True)
    action_type = Column(String(30), nullable=False) # VIEWED, EXPORTED, SCHEDULED, DELETED
    user_id = Column(String(36), nullable=False)
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

class ExportHistory(Base):
    __tablename__ = "export_history"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False)
    export_format = Column(String(20), nullable=False) # PDF, EXCEL, CSV, DOCX, JSON
    file_url = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0, nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    is_password_protected = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class ChartDefinition(Base):
    __tablename__ = "chart_definitions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    chart_name = Column(String(150), nullable=False)
    chart_type = Column(String(30), default="BAR", nullable=False) # BAR, LINE, AREA, PIE, DONUT, STACKED, RADAR, SCATTER, HEATMAP, GAUGE, FUNNEL, TREEMAP
    config_options_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class WidgetSetting(Base):
    __tablename__ = "widget_settings"
    id = Column(String(36), primary_key=True)
    widget_id = Column(String(36), ForeignKey("dashboard_widgets.id"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    position_x = Column(Integer, default=0, nullable=False)
    position_y = Column(Integer, default=0, nullable=False)
    width = Column(Integer, default=4, nullable=False)
    height = Column(Integer, default=3, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BiSetting(Base):
    __tablename__ = "bi_settings"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    setting_key = Column(String(100), nullable=False)
    setting_value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
