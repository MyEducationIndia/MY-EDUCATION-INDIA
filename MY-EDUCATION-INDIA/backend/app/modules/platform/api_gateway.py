"""Module 20: Enterprise API Gateway"""
import time

class EnterpriseApiGateway:
    def __init__(self):
        self.request_counters = {}

    def check_rate_limit(self, client_id: str, limit_per_minute: int = 120) -> bool:
        now = time.time()
        timestamps = self.request_counters.get(client_id, [])
        valid_ts = [t for t in timestamps if now - t < 60.0]
        if len(valid_ts) >= limit_per_minute:
            return False
        valid_ts.append(now)
        self.request_counters[client_id] = valid_ts
        return True
