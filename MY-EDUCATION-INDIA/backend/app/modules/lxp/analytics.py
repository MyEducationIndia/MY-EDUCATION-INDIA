"""
Module 15: LXP Analytics & Telemetry
"""
def compute_completion_kpis(enrollments: list) -> dict:
    total = len(enrollments)
    if total == 0:
        return {"total_enrollments": 0, "completed_count": 0, "completion_rate": 0.0}
    completed = sum(1 for e in enrollments if e.get("enrollment_status") == "COMPLETED")
    return {
        "total_enrollments": total,
        "completed_count": completed,
        "completion_rate": round((completed / total) * 100.0, 2)
    }

def compute_dropoff_by_module(module_progress_data: list) -> list:
    return sorted(module_progress_data, key=lambda x: x.get("dropoff_count", 0), reverse=True)
