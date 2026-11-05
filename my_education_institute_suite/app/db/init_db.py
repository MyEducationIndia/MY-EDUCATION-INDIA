from app.core.database import Base, engine
from app.core.logging_config import get_logger, setup_logging
import app.models.entities  # noqa: F401 - register all SQLAlchemy ORM models

logger = get_logger(__name__)


def init_database(fresh: bool = False) -> None:
    """
    Initializes PostgreSQL database tables using SQLAlchemy 2.x metadata.
    """
    if fresh:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("PostgreSQL database tables initialized successfully via SQLAlchemy ORM.")


init_db = init_database

if __name__ == "__main__":
    setup_logging()
    init_database()
