"""
Database base configuration for product service.
"""
from core.database import TimestampBase, get_db

# Use TimestampBase for automatic timestamps
Base = TimestampBase

# Import all models here so Alembic can discover them
# from apps.product_service.db.models.product import Product  # noqa: F401

__all__ = ["Base", "get_db"]