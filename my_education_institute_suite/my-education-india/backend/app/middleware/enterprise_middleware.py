import time
import uuid
from collections import defaultdict, deque
from typing import Deque, Dict
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logs.logger import app_logger

SUPPORTED_SUBDOMAINS = {
    "admin",
    "website",
    "student",
    "teacher",
    "parent",
    "exam",
    "cbt",
    "fees",
    "attendance",
    "certificate",
    "library",
    "lms",
    "communication",
    "api",
}


class EnterpriseContextAndSecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests_per_minute: int = 120) -> None:
        super().__init__(app)
        self.max_requests_per_minute = max_requests_per_minute
        self._rate_buckets: Dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        # Extract subdomain for multi-portal routing awareness
        host = request.headers.get("host", "localhost").split(":")[0].lower()
        parts = host.split(".")
        subdomain = parts[0] if len(parts) > 2 and parts[0] in SUPPORTED_SUBDOMAINS else "api"
        request.state.subdomain = subdomain

        # Client IP & Sliding Window Rate Limiting
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or (request.client.host if request.client else "127.0.0.1")
        )
        request.state.client_ip = client_ip

        now = time.monotonic()
        bucket = self._rate_buckets[client_ip]
        while bucket and now - bucket[0] > 60.0:
            bucket.popleft()
        if len(bucket) >= self.max_requests_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests from this IP address. Please retry after a minute.",
                        "details": {"limit_per_minute": self.max_requests_per_minute},
                        "request_id": request_id,
                    },
                },
            )
        bucket.append(now)

        start_time = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Enterprise Security Headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Subdomain-Context"] = subdomain
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

        app_logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)",
            extra={"request_id": request_id, "subdomain": subdomain},
        )
        return response
