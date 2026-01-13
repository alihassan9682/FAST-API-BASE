"""
Authentication endpoints.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from apps.auth_service.schemas.token import Token, LoginRequest, RefreshTokenRequest
from apps.auth_service.schemas.user import UserCreate, UserResponse
from apps.auth_service.services.auth_service import AuthService
from apps.auth_service.api.dependencies import get_current_active_user
from apps.auth_service.db.models.user import User
from apps.auth_service.core.exceptions import InvalidCredentialsError

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    user = AuthService.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    user = AuthService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise InvalidCredentialsError()
    
    tokens = AuthService.create_tokens(user)
    return tokens


@router.post("/refresh", response_model=dict)
async def refresh_token(
    token_data: RefreshTokenRequest
):
    """Refresh access token."""
    tokens = AuthService.refresh_access_token(token_data.refresh_token)
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    return current_user
