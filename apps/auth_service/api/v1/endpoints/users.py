"""
User management endpoints.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from apps.auth_service.schemas.user import UserResponse, UserUpdate
from apps.auth_service.services.auth_service import AuthService
from apps.auth_service.api.dependencies import get_current_active_user, get_admin_user
from apps.auth_service.db.models.user import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Get all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID."""
    # Users can only view their own profile unless they're admin
    if current_user.id != user_id and current_user.role.value != "admin":
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        from core.exceptions import NotFoundError
        raise NotFoundError("User", str(user_id))
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user information."""
    # Users can only update their own profile unless they're admin
    if current_user.id != user_id and current_user.role.value != "admin":
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = AuthService.update_user(db, user_id, user_data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Delete a user (admin only)."""
    AuthService.delete_user(db, user_id)
    return None
