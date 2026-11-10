"""
Module 17: CRM Analytics & Telemetry Engine
"""
def compute_conversion_metrics(total_leads: int, admissions_confirmed: int) -> dict:
    if total_leads <= 0:
        return {"conversion_rate_percentage": 0.0, "total_leads": 0, "admissions": 0}
    rate = round((admissions_confirmed / total_leads) * 100.0, 2)
    return {
        "conversion_rate_percentage": rate,
        "total_leads": total_leads,
        "admissions": admissions_confirmed
    }

def calculate_expected_pipeline_revenue(opportunities: list) -> float:
    total = 0.0
    for opp in opportunities:
        val = opp.get("deal_value", 0.0)
        prob = opp.get("probability_percentage", 50.0) / 100.0
        total += (val * prob)
    return round(total, 2)
