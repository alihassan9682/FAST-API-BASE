"""
Auth service specific exceptions.
"""
from core.exceptions import BaseAPIException
from fastapi import status


class InvalidCredentialsError(BaseAPIException):
    """Invalid credentials exception."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


class UserAlreadyExistsError(BaseAPIException):
    """User already exists exception."""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {email} already exists"
        )


class TokenExpiredError(BaseAPIException):
    """Token expired exception."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )


class InvalidTokenError(BaseAPIException):
    """Invalid token exception."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
