"""
Core exception classes for the application.
"""
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Base exception class for API errors."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(BaseAPIException):
    """Resource not found exception."""
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {identifier} not found"
        )


class UnauthorizedError(BaseAPIException):
    """Unauthorized access exception."""
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class ForbiddenError(BaseAPIException):
    """Forbidden access exception."""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ValidationError(BaseAPIException):
    """Validation error exception."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
