"""
Core configuration module for shared settings across all microservices.
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
import sys


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
    
    # Security - REQUIRED: Must be set in .env file
    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="Required secret key for JWT token signing. Must be at least 32 characters."
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """
        Validate SECRET_KEY is set, has minimum length, and is not a weak/default value.
        This validator runs after Pydantic's field validation.
        """
        if not v:
            print("\n" + "=" * 80)
            print("❌ CRITICAL ERROR: SECRET_KEY is required!")
            print("=" * 80)
            print("   The SECRET_KEY must be set in your .env file.")
            print("   The application CANNOT run without a valid SECRET_KEY.")
            print("   This is a security requirement for JWT token signing.\n")
            print("   Please add SECRET_KEY to your .env file with at least 32 characters.")
            print("=" * 80 + "\n")
            sys.exit(1)
        
        v_stripped = v.strip()
        
        # Check minimum length
        if len(v_stripped) < 32:
            print("\n" + "=" * 80)
            print("❌ CRITICAL ERROR: SECRET_KEY is too short!")
            print("=" * 80)
            print(f"   Current length: {len(v_stripped)} characters")
            print("   Required length: At least 32 characters")
            print("   The application CANNOT run with an invalid SECRET_KEY.")
            print("   This is a security requirement for JWT token signing.\n")
            print("   Please update SECRET_KEY in your .env file with at least 32 characters.")
            print("=" * 80 + "\n")
            sys.exit(1)
        
        # Check for weak/common secret keys
        weak_keys = [
            "your-secret-key-here-change-this-in-production",
            "change-this-secret-key-in-production",
            "secret-key-change-this-in-production",
            "default-secret-key-change-me",
            "please-change-this-secret-key",
            "changeme" * 10,  # Repeated patterns
            "a" * 32,  # All same character
            "1234567890" * 4,  # Sequential numbers
            "abcdefghijklmnopqrstuvwxyz123456",  # Sequential letters
            "false",  # Common invalid value
            "true",  # Common invalid value
            "none",  # Common invalid value
            "null",  # Common invalid value
            "secret",  # Too common
            "password",  # Too common
        ]
        
        # Check for boolean-like or common invalid values (case-insensitive)
        invalid_values = ["false", "true", "none", "null", "secret", "password", "test", "demo"]
        if v_stripped.lower() in invalid_values:
            print("\n" + "=" * 80)
            print("❌ CRITICAL ERROR: SECRET_KEY appears to be an invalid value!")
            print("=" * 80)
            print(f"   Detected value: '{v_stripped}'")
            print("   The SECRET_KEY must be a secure, randomly generated string.")
            print("   The application CANNOT run with an invalid SECRET_KEY.")
            print("   This is a security requirement for JWT token signing.\n")
            print("   Please generate a secure SECRET_KEY and update it in your .env file.")
            print("=" * 80 + "\n")
            sys.exit(1)
        
        # Check if it's a weak key
        v_lower = v_stripped.lower()
        for weak_key in weak_keys:
            if weak_key in v_lower or v_lower in weak_key:
                print("\n" + "=" * 80)
                print("❌ CRITICAL ERROR: SECRET_KEY is too weak or appears to be a default value!")
                print("=" * 80)
                print("   The SECRET_KEY must be a secure, randomly generated string.")
                print("   The application CANNOT run with a weak or default SECRET_KEY.")
                print("   This is a security requirement for JWT token signing.\n")
                print("   Security requirements:")
                print("   - Must be at least 32 characters long")
                print("   - Must be randomly generated (not sequential or repeated)")
                print("   - Must not be a common/default value")
                print("   - Should contain a mix of letters, numbers, and special characters\n")
                print("   Please generate a secure SECRET_KEY and update it in your .env file.")
                print("=" * 80 + "\n")
                sys.exit(1)
        
        # Check for low entropy (too many repeated characters)
        if len(set(v_stripped)) < 8:  # Less than 8 unique characters
            print("\n" + "=" * 80)
            print("❌ CRITICAL ERROR: SECRET_KEY has low entropy (too many repeated characters)!")
            print("=" * 80)
            print("   The SECRET_KEY must be a secure, randomly generated string.")
            print("   The application CANNOT run with a weak SECRET_KEY.\n")
            print("   Please generate a secure SECRET_KEY with high entropy and update it in your .env file.")
            print("=" * 80 + "\n")
            sys.exit(1)
        
        return v_stripped
    
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


# Initialize settings - this will fail if SECRET_KEY is missing or invalid
try:
    settings = Settings()
except Exception as e:
    error_str = str(e).lower()
    # Check if it's a SECRET_KEY related error
    if "secret_key" in error_str or "secret" in error_str or "string_too_short" in error_str:
        print("\n" + "=" * 80)
        print("❌ CRITICAL ERROR: SECRET_KEY validation failed!")
        print("=" * 80)
        print("   The SECRET_KEY must be set in your .env file.")
        print("   The application CANNOT run without a valid SECRET_KEY.")
        print("   This is a security requirement for JWT token signing.\n")
        print("   Requirements:")
        print("   - SECRET_KEY must be present in .env file")
        print("   - SECRET_KEY must be at least 32 characters long")
        print("   - SECRET_KEY should be a secure random string\n")
        print("   Please add or update SECRET_KEY in your .env file.")
        print("=" * 80 + "\n")
        sys.exit(1)
    else:
        # Re-raise other exceptions
        raise
