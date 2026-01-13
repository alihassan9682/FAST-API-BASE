"""
Product service specific configuration.
"""
from pydantic_settings import BaseSettings


class ProductServiceSettings(BaseSettings):
    """Product service specific settings."""
    
    SERVICE_NAME: str = "product_service"
    SERVICE_PORT: int = 8001
    
    class Config:
        env_file = ".env"
        case_sensitive = True


product_settings = ProductServiceSettings()
