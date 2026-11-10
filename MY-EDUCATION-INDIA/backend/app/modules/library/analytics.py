"""
Module 14: Library Analytics & KPIs
"""
def get_circulation_kpis(metrics: dict) -> dict:
    total_books = metrics.get("total_physical_copies", 0)
    active_issued = metrics.get("active_issued_copies", 0)
    utilization_rate = round((active_issued / total_books * 100), 2) if total_books > 0 else 0.0
    return {
        "utilization_rate_percentage": utilization_rate,
        "active_issued": active_issued,
        "available": metrics.get("available_copies", 0),
        "total_books": total_books
    }

def get_popular_books(circulation_stats: list, limit: int = 5) -> list:
    sorted_stats = sorted(circulation_stats, key=lambda x: x.get("borrow_count", 0), reverse=True)
    return sorted_stats[:limit]
