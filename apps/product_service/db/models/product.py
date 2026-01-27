"""
Product model for product service.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from apps.product_service.db.base import Base


class Product(Base):
    """
    Product model with automatic audit fields (created_at, updated_at).
    
    Inherits from TimestampBase which automatically provides:
    - id: Primary key
    - created_at: Timestamp when product was created (for audit logging)
    - updated_at: Timestamp when product was last updated (for audit logging)
    
    These fields are essential for timeseries algorithms to track product trends.
    """
    __tablename__ = "products"
    
    # Note: id, created_at, and updated_at are automatically included from TimestampBase
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    category = Column(String, nullable=True, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Reference to auth service
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
