import json
from typing import List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MY EDUCATION INSTITUTE"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Security & JWT Configuration (loaded strictly via BaseSettings from environment / .env)
    SECRET_KEY: str = "render-production-secret-key-change-in-env-9f8e7d6c5b4a3f2e1d0c"
    JWT_SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    INACTIVITY_TIMEOUT_MINUTES: int = 10

    # PostgreSQL Database Configuration
    DATABASE_URL: str = "postgresql+psycopg2://my_education_user:my_education_secure_pass@localhost:5432/my_education"

    # SQLAlchemy Production Connection Pool Parameters
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # Server Host, Port, CORS & Rate Limiting
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: Union[List[str], str] = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 240

    # SMTP Email Delivery Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@myeducation.edu.in"
    SMTP_TLS: bool = True

    # S3 / Cloudflare R2 / Backblaze B2 Object Storage Configuration
    S3_BUCKET: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None
    S3_REGION_NAME: str = "us-east-1"
    S3_PUBLIC_URL: Optional[str] = None

    # Redis Cache / Session Broker Configuration
    REDIS_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        v = self.CORS_ORIGINS
        if isinstance(v, str):
            v_str = v.strip()
            if v_str.startswith("[") and v_str.endswith("]"):
                try:
                    parsed = json.loads(v_str)
                    if isinstance(parsed, list):
                        return [str(x).strip() for x in parsed if str(x).strip()]
                except Exception:
                    pass
            return [i.strip() for i in v_str.split(",") if i.strip()]
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        return ["*"]

    @property
    def effective_jwt_secret(self) -> str:
        return self.JWT_SECRET_KEY or self.SECRET_KEY

    @property
    def get_database_url(self) -> str:
        """
        Ensures compatibility with Render PostgreSQL connection string format.
        Replaces legacy 'postgres://' or 'postgresql://' prefix with SQLAlchemy 2.x 'postgresql+psycopg2://'.
        """
        url = (self.DATABASE_URL or "").strip()
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url


settings = Settings()
