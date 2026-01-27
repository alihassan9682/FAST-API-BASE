"""
Database base configuration for auth service.
"""
from core.database import TimestampBase, get_db

# Use TimestampBase for automatic timestamps
Base = TimestampBase

# Import all models here so Alembic can discover them
# from apps.auth_service.db.models.user import User  # noqa: F401

__all__ = ["Base", "get_db"]