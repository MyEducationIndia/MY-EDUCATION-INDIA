"""
Module 15: Video Streaming & Telemetry Service
"""
import hashlib
import time

class VideoStreamingService:
    @staticmethod
    def generate_signed_streaming_url(raw_url: str, user_id: str, secret: str = "erp_video_secret", ttl_seconds: int = 3600) -> str:
        expiry = int(time.time()) + ttl_seconds
        token = hashlib.sha256(f"{raw_url}:{user_id}:{expiry}:{secret}".encode("utf-8")).hexdigest()
        return f"{raw_url}?token={token}&expires={expiry}"

    @staticmethod
    def calculate_watch_ratio(watch_seconds: int, total_duration_seconds: int) -> float:
        if total_duration_seconds <= 0:
            return 100.0
        return min(round((watch_seconds / total_duration_seconds) * 100.0, 2), 100.0)
