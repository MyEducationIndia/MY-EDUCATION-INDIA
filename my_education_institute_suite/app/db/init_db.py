from app.core.database import engine, Base
import app.models.entities  # Ensure all SQLAlchemy ORM models are registered

def init_database(fresh: bool = False):
    """
    Initializes PostgreSQL database tables using SQLAlchemy 2.x metadata.
    """
    if fresh:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL database tables initialized successfully via SQLAlchemy ORM.")

init_db = init_database

if __name__ == "__main__":
    init_database()
