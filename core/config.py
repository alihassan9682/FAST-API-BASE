"""
Core configuration module for shared settings across all microservices.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project Info
    PROJECT_NAME: str = "ATB Backend"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Redis (for caching/sessions)
    REDIS_URL: Optional[str] = None
    
    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    # Service URLs (for inter-service communication)
    AUTH_SERVICE_URL: str = "http://auth_service:8000"
    PRODUCT_SERVICE_URL: str = "http://product_service:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow extra environment variables that are not explicitly defined
        # on the Settings model (e.g. POSTGRES_USER, SMTP_HOST, etc.).
        # Without this, Pydantic raises `extra_forbidden` errors and the
        # application fails to start when such variables are present.
        extra = "ignore"


settings = Settings()
