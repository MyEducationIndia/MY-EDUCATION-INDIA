"""
API Telemetry & Analytics Engine
"""
def compute_provider_metrics(logs: list) -> dict:
    total = len(logs)
    if total == 0:
        return {"total_calls": 0, "success_rate": 100.0, "avg_latency_ms": 0.0, "circuit_trips": 0}
    successes = sum(1 for l in logs if l.get("is_success"))
    total_lat = sum(l.get("latency_ms", 0.0) for l in logs)
    circuit_trips = sum(1 for l in logs if l.get("circuit_broken"))
    return {
        "total_calls": total,
        "success_rate": round((successes / total) * 100.0, 2),
        "avg_latency_ms": round(total_lat / total, 2),
        "circuit_trips": circuit_trips
    }
