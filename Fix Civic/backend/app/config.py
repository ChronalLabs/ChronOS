"""
CivicFix Backend Configuration
Reads from environment variables / .env file
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./civicfix.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # S3 / MinIO
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "civicfix"
    S3_REGION: str = "us-east-1"

    # Google Maps
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    # X / Twitter
    X_API_KEY: Optional[str] = None
    X_API_SECRET: Optional[str] = None
    X_ACCESS_TOKEN: Optional[str] = None
    X_ACCESS_TOKEN_SECRET: Optional[str] = None
    X_BEARER_TOKEN: Optional[str] = None
    X_AUTO_POST_ENABLED: bool = False

    # Firebase
    FIREBASE_PROJECT_ID: Optional[str] = None

    # JWT
    JWT_SECRET: str = "supersecretkey-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440

    # SMTP Settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # App
    MOCK_MODE: bool = True
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    MAX_UPLOAD_SIZE_MB: int = 10
    RATE_LIMIT_MAX_REQUESTS: int = 5
    RATE_LIMIT_WINDOW_SECONDS: int = 3600

    # Admin
    ADMIN_EMAIL: str = "admin@civicfix.com"
    ADMIN_PASSWORD: str = "admin123"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
