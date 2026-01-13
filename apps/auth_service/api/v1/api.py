"""
API v1 router aggregation.
"""
from fastapi import APIRouter
from apps.auth_service.api.v1.endpoints import auth, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
