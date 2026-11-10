"""
Module 18: BI Service Layer
"""
from app.modules.bi.repository import BiRepository
from app.modules.bi.validators import BiBusinessValidators
from app.modules.bi.report_engine import UniversalReportQueryEngine
from app.modules.bi.analytics_engine import PredictiveAnalyticsEngine
from app.modules.bi.chart_engine import EChartsOptionBuilder
from app.modules.bi.system_health import SystemHealthMonitor

class BiManagementService:
    def __init__(self, repo: BiRepository):
        self.repo = repo

    def calculate_health_score(self, attendance: float, fees: float, exam: float, crm: float) -> float:
        return PredictiveAnalyticsEngine.compute_institute_health_score(attendance, fees, exam, crm)

    def generate_chart_config(self, chart_type: str, title: str, categories: list, data: list):
        if chart_type == "BAR":
            return EChartsOptionBuilder.build_bar_chart(title, categories, data)
        return {}

    def get_system_health(self):
        return SystemHealthMonitor.get_cluster_health_overview()
