"""
API dependencies for authentication and authorization.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from core.security import decode_token
from apps.auth_service.services.auth_service import AuthService
from core.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token."""
    payload = decode_token(token)
    if not payload:
        raise UnauthorizedError("Invalid authentication credentials")
    
    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise UnauthorizedError("Invalid token payload")
    
    user = AuthService.get_user_by_id(db, user_id)
    if user is None:
        raise UnauthorizedError("User not found")
    
    if not user.is_active:
        raise UnauthorizedError("User account is inactive")
    
    return user


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """Get current active user."""
    if not current_user.is_active:
        raise UnauthorizedError("User account is inactive")
    return current_user


def get_admin_user(
    current_user = Depends(get_current_active_user)
):
    """Get current admin user."""
    from db.models.user import UserRole
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
