"""
Module 17: Campaign ROI Engine
"""
class CampaignROIEngine:
    @staticmethod
    def calculate_cost_per_lead(total_spent: float, leads_generated: int) -> float:
        if leads_generated <= 0:
            return 0.0
        return round(total_spent / leads_generated, 2)

    @staticmethod
    def calculate_roi_percentage(revenue_generated: float, total_spent: float) -> float:
        if total_spent <= 0:
            return 0.0
        net_profit = revenue_generated - total_spent
        return round((net_profit / total_spent) * 100.0, 2)
