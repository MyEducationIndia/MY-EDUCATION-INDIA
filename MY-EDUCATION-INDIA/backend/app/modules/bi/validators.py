"""
Module 18: BI Business Validators
"""
import re

class BiBusinessValidators:
    @staticmethod
    def validate_chart_type(chart_type: str) -> bool:
        valid_types = {
            "BAR", "LINE", "AREA", "PIE", "DONUT", "STACKED",
            "RADAR", "SCATTER", "HEATMAP", "GAUGE", "FUNNEL", "TREEMAP"
        }
        return chart_type.upper() in valid_types

    @staticmethod
    def validate_export_format(fmt: str) -> bool:
        valid_formats = {"PDF", "EXCEL", "CSV", "DOCX", "JSON"}
        return fmt.upper() in valid_formats

    @staticmethod
    def validate_cron_format(cron: str) -> bool:
        parts = cron.strip().split()
        return len(parts) == 5

    @staticmethod
    def validate_kpi_thresholds(warning: float, critical: float, target: float) -> bool:
        return True # Flexible bounds for both ascending and descending KPIs
