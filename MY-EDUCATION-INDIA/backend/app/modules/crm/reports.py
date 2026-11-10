"""
Module 17: CRM Reports
"""
def generate_lead_conversion_report(leads: list) -> dict:
    total = len(leads)
    converted = sum(1 for l in leads if l.get("stage") == "ADMISSION_CONFIRMED")
    return {
        "report_type": "LEAD_CONVERSION_AUDIT",
        "total_leads": total,
        "converted_count": converted,
        "conversion_percentage": round((converted / total * 100.0), 2) if total > 0 else 0.0,
        "leads": leads
    }
