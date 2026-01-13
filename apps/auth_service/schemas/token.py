"""
Token schemas for authentication.
"""
from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""
    email: str | None = None
    user_id: int | None = None


class LoginRequest(BaseModel):
    """Login request schema."""
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str
