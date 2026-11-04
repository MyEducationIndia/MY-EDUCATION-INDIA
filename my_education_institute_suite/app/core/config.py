import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MY EDUCATION INSTITUTE"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Mandatory security and database environment variables
    # Must be supplied via Render environment variables or .env file
    SECRET_KEY: str = os.getenv("SECRET_KEY", ...)
    DATABASE_URL: str = os.getenv("DATABASE_URL", ...)

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    INACTIVITY_TIMEOUT_MINUTES: int = 10

    # SQLAlchemy Production Connection Pool Parameters
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # Optional S3-compatible persistent object storage for file uploads
    # If not set, uploads use PostgreSQL BYTEA storage (persistent across Render restarts)
    S3_BUCKET: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None
    S3_REGION_NAME: Optional[str] = "us-east-1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Pydantic v1 backwards compatibility
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def get_database_url(self) -> str:
        """
        Ensures compatibility with Render PostgreSQL connection string format.
        Replaces legacy 'postgres://' prefix with SQLAlchemy 2.x standard 'postgresql+psycopg2://'.
        """
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

# Instantiate settings - reads from environment variables and .env
settings = Settings()
