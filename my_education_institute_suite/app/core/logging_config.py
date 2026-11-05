import logging
import sys
from typing import Optional


def setup_logging(level: Optional[str] = "INFO") -> None:
    if not level:
        level = "INFO"
    log_level = getattr(logging, str(level).upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
