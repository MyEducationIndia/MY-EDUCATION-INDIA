from functools import lru_cache
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "MY EDUCATION INDIA"
    APP_ENV: str = Field(default="production")
    DEBUG: bool = Field(default=False)
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = Field(..., min_length=32)
    REFRESH_SECRET_KEY: str = Field(..., min_length=32)
    CSRF_SECRET_KEY: str = Field(..., min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, ge=5, le=120)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=30)
    ALGORITHM: str = "HS256"

    # Strictly PostgreSQL (Neon PostgreSQL compatible)
    DATABASE_URL: str = Field(...)
    SYNC_DATABASE_URL: str = Field(...)
    DB_POOL_SIZE: int = Field(default=20, ge=5, le=100)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=50)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=5, le=120)

    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173")
    COOKIE_DOMAIN: str | None = Field(default=None)
    COOKIE_SECURE: bool = Field(default=True)

    SENTRY_DSN: str = Field(default="")
    LOG_LEVEL: str = Field(default="INFO")

    # External Providers
    CLOUDINARY_CLOUD_NAME: str = Field(default="")
    CLOUDINARY_API_KEY: str = Field(default="")
    CLOUDINARY_API_SECRET: str = Field(default="")

    SMTP_HOST: str = Field(default="")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_FROM_EMAIL: str = Field(default="noreply@myeducationindia.edu.in")
    SMTP_TLS: bool = Field(default=True)

    SMS_PROVIDER: str = Field(default="msg91")
    SMS_API_KEY: str = Field(default="")
    SMS_SENDER_ID: str = Field(default="MEIEDU")

    WHATSAPP_PROVIDER: str = Field(default="meta_cloud_api")
    WHATSAPP_ACCESS_TOKEN: str = Field(default="")
    WHATSAPP_PHONE_NUMBER_ID: str = Field(default="")

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_postgres_async_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError(
                "DATABASE_URL must strictly use PostgreSQL with asyncpg driver (postgresql+asyncpg://). "
                "SQLite, JSON, or in-memory databases are strictly prohibited."
            )
        return v

    @field_validator("SYNC_DATABASE_URL")
    @classmethod
    def validate_postgres_sync_url(cls, v: str) -> str:
        if not (v.startswith("postgresql://") or v.startswith("postgresql+psycopg://")):
            raise ValueError(
                "SYNC_DATABASE_URL must strictly use PostgreSQL (postgresql:// or postgresql+psycopg://)."
            )
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
