"""
Auth service specific configuration.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class AuthServiceSettings(BaseSettings):
    """Auth service specific settings."""
    
    SERVICE_NAME: str = "auth_service"
    SERVICE_PORT: int = 8000
    
    # Email settings (for password reset, etc.)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # OAuth settings (if needed)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


auth_settings = AuthServiceSettings()
