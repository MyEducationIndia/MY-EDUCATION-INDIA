import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MY EDUCATION INSTITUTE"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "prod_super_secret_key_8492019482716301")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    INACTIVITY_TIMEOUT_MINUTES: int = 10
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./data/my_education.db")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

settings = Settings()
