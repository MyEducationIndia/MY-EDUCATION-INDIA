import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class StructuredJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_payload: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, "request_id"):
            log_payload["request_id"] = getattr(record, "request_id")
        if hasattr(record, "user_id"):
            log_payload["user_id"] = getattr(record, "user_id")
        if hasattr(record, "subdomain"):
            log_payload["subdomain"] = getattr(record, "subdomain")
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_payload, ensure_ascii=False)


def configure_logging(log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("my_education_india")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.handlers.clear()

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(StructuredJsonFormatter())
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


app_logger = configure_logging()
