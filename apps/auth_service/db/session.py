"""
Database session management for auth service.
"""
from core.database import SessionLocal, get_db

__all__ = ["SessionLocal", "get_db"]
