"""
Module 14: Library Reports
"""
def generate_active_issues_register(issues: list) -> dict:
    return {
        "report_type": "ACTIVE_ISSUES_REGISTER",
        "total_records": len(issues),
        "issues": issues
    }

def generate_overdue_fines_report(fines: list) -> dict:
    total_unpaid = sum(f.get("balance_amount", 0.0) for f in fines)
    return {
        "report_type": "OVERDUE_FINES_AUDIT",
        "total_unpaid_amount": round(total_unpaid, 2),
        "fines": fines
    }
