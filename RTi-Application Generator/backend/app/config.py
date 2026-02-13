"""
Application Configuration
Production-grade settings loaded from environment variables.
All sensitive values must come from environment, not hardcoded.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional, List, Union
from functools import lru_cache
import json


class Settings(BaseSettings):
    """
    Application settings loaded from environment.
    
    Usage:
        from app.config import get_settings
        settings = get_settings()
    """
    
    # ===================
    # Server Configuration
    # ===================
    APP_NAME: str = "RTI & Complaint Generator API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="development, staging, production")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    BACKEND_HOST: str = Field(default="0.0.0.0", description="Server host")
    BACKEND_PORT: int = Field(default=8000, description="Server port")
    
    # ===================
    # CORS Configuration
    # ===================
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default='["http://localhost:3000","http://127.0.0.1:3000","https://*.vercel.app"]',
        description="Allowed CORS origins - JSON array or comma-separated string"
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS_ORIGINS from JSON string or comma-separated values"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Remove whitespace
            v = v.strip()
            if not v:
                return ["http://localhost:3000"]
            # Try parsing as JSON array (handles both proper JSON and escaped quotes)
            if v.startswith('[') or v.startswith('[\\"'):
                try:
                    # Handle escaped quotes from environment variables
                    cleaned = v.replace('\\"', '"')
                    parsed = json.loads(cleaned)
                    return parsed if isinstance(parsed, list) else [str(parsed)]
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated values (only if no brackets)
            if '[' not in v:
                return [origin.strip() for origin in v.split(",") if origin.strip()]
            # Last resort: return as single item
            return [v]
        return ["http://localhost:3000"]
    
    # ===================
    # NLP Configuration
    # ===================
    SPACY_MODEL: str = Field(default="en_core_web_sm", description="spaCy model to use")
    ENABLE_DISTILBERT: bool = Field(default=False, description="Enable DistilBERT for semantic analysis (memory intensive)")
    DISTILBERT_MODEL: str = Field(default="distilbert-base-uncased", description="DistilBERT model")
    
    # ===================
    # Confidence Thresholds
    # ===================
    CONFIDENCE_HIGH: float = Field(default=0.9, description="High confidence threshold - auto proceed")
    CONFIDENCE_MEDIUM: float = Field(default=0.7, description="Medium confidence - suggest with highlight")
    CONFIDENCE_LOW: float = Field(default=0.5, description="Low confidence - show alternatives")
    
    # ===================
    # Rate Limiting
    # ===================
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Max requests per window")
    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60, description="Rate limit window in seconds")
    
    # ===================
    # Logging
    # ===================
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        description="Log format"
    )
    LOG_TO_FILE: bool = Field(default=False, description="Also log to file")
    LOG_FILE_PATH: str = Field(default="logs/app.log", description="Log file path")
    
    # ===================
    # Document Generation
    # ===================
    MAX_DOCUMENT_SIZE_MB: int = Field(default=10, description="Max generated document size in MB")
    PDF_FONT: str = Field(default="Helvetica", description="PDF font family")
    PDF_FONT_SIZE: int = Field(default=11, description="PDF base font size")
    
    # ===================
    # Security
    # ===================
    API_KEY_ENABLED: bool = Field(default=False, description="Require API key for requests")
    API_KEY_HEADER: str = Field(default="X-API-Key", description="API key header name")
    API_KEYS: Union[str, List[str]] = Field(default="[]", description="Valid API keys - JSON array or comma-separated")
    
    @field_validator("API_KEYS", mode="after")
    @classmethod
    def parse_api_keys(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse API_KEYS from JSON string or comma-separated values"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            if not v or v == "[]":
                return []
            if v.startswith('['):
                try:
                    parsed = json.loads(v)
                    return parsed if isinstance(parsed, list) else [str(parsed)]
                except json.JSONDecodeError:
                    pass
            return [key.strip() for key in v.split(",") if key.strip()]
        return []
    
    # ===================
    # OpenAI Configuration (LLM Assistant - NOT Authority)
    # ===================
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key for LLM enhancement")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", description="OpenAI model to use")
    OPENAI_MAX_TOKENS: int = Field(default=1500, description="Max tokens for LLM response")
    OPENAI_TEMPERATURE: float = Field(default=0.3, description="Low temperature for consistent legal language")
    ENABLE_LLM_ENHANCEMENT: bool = Field(default=True, description="Enable LLM text enhancement")
    LLM_ENHANCEMENT_MODE: str = Field(default="polish", description="polish, translate, clarify")
    
    # ===================
    # Feature Flags
    # ===================
    FEATURE_HINDI_SUPPORT: bool = Field(default=True, description="Enable Hindi language support")
    FEATURE_XLSX_EXPORT: bool = Field(default=True, description="Enable XLSX export")
    FEATURE_AUDIT_LOG: bool = Field(default=True, description="Enable audit logging")
    FEATURE_LLM_ASSIST: bool = Field(default=True, description="Enable LLM assistance for text improvement")
    
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        # This tells pydantic-settings to parse JSON strings for complex types
        json_schema_extra={"env_parse_none_str": "null"},
    )
        
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid re-reading env vars on every call.
    """
    return Settings()


# For backward compatibility
settings = get_settings()
