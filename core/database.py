"""
Core database configuration and session management.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import create_engine, Column, DateTime, Integer, Boolean, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import expression
from core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Custom base class with common functionality
class CustomBase:
    """Base class with common attributes and methods for all models."""
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name automatically from class name."""
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        if name.endswith('y'):
            return name[:-1] + 'ies'
        elif name.endswith('s'):
            return name + 'es'
        return name + 's'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    def to_dict(self, exclude: Optional[list] = None) -> Dict[str, Any]:
        """Convert model instance to dictionary, excluding specified fields."""
        result = {}
        exclude = exclude or []
        
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                if isinstance(value, datetime):
                    result[column.name] = value.isoformat() if value else None
                else:
                    result[column.name] = value
        
        return result
    
    def update(self, db: Session, **kwargs) -> None:
        """Update model instance with given kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.commit()
        db.refresh(self)

# Audit/Timestamp mixin class for audit logging and timeseries support
class TimestampMixin:
    """
    Mixin class that adds created_at and updated_at timestamps.
    
    This mixin is essential for:
    - Audit logging: Track when records are created/modified
    - Timeseries algorithms: Rank and match users based on temporal data
    - Data analytics: Analyze trends over time
    
    All models should inherit from TimestampBase to automatically get these fields.
    """
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Timestamp when the record was created (for audit logging and timeseries)"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
        comment="Timestamp when the record was last updated (for audit logging and timeseries)"
    )
    
    @property
    def age_in_days(self) -> Optional[float]:
        """Return the age of the record in days (useful for timeseries algorithms)."""
        if self.created_at:
            delta = datetime.utcnow() - self.created_at
            return delta.total_seconds() / 86400  # seconds in a day
        return None
    
    @property
    def age_in_hours(self) -> Optional[float]:
        """Return the age of the record in hours (useful for timeseries algorithms)."""
        if self.created_at:
            delta = datetime.utcnow() - self.created_at
            return delta.total_seconds() / 3600  # seconds in an hour
        return None

# Soft delete mixin class
class SoftDeleteMixin:
    """Mixin for models that support soft deletion."""
    
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="Timestamp when the record was soft deleted (null if not deleted)"
    )
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        server_default=expression.true(),
        comment="Flag indicating if the record is active"
    )
    
    def soft_delete(self, db: Session) -> None:
        """Soft delete the record by setting deleted_at timestamp."""
        self.deleted_at = func.now()
        self.is_active = False
        db.commit()
        db.refresh(self)
    
    def restore(self, db: Session) -> None:
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.is_active = True
        db.commit()
        db.refresh(self)
    
    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None

# Create base class without timestamps (for special cases only)
Base = declarative_base(cls=CustomBase)

# Audit Base Class - RECOMMENDED for all models
# This combines CustomBase and TimestampMixin properly for SQLAlchemy
class AuditBase(CustomBase, TimestampMixin):
    """
    Base class for all models that need audit logging and timeseries support.
    
    Automatically includes:
    - id: Primary key
    - created_at: Timestamp when record was created (indexed, for audit logging)
    - updated_at: Timestamp when record was last updated (indexed, for audit logging)
    
    These fields are essential for:
    - Audit logging: Track when records are created/modified
    - Timeseries algorithms: Rank and match users based on temporal data
    - Data analytics: Analyze trends over time
    
    Usage:
        from apps.your_service.db.base import Base  # This is TimestampBase
        
        class MyModel(Base):
            __tablename__ = "my_table"
            name = Column(String, nullable=False)
            # created_at and updated_at are automatically included!
    """
    __abstract__ = True

# Create declarative base with audit fields - RECOMMENDED for all models
TimestampBase = declarative_base(cls=AuditBase)

# Soft delete with timestamps base (for models that need soft deletion)
class SoftDeleteAuditBase(CustomBase, TimestampMixin, SoftDeleteMixin):
    """
    Base class for models that need both audit logging and soft deletion.
    
    Automatically includes:
    - id: Primary key
    - created_at: Timestamp when record was created
    - updated_at: Timestamp when record was last updated
    - deleted_at: Timestamp when record was soft deleted (nullable)
    - is_active: Boolean flag for active status
    
    Usage:
        from core.database import SoftDeleteTimestampBase
        
        class MyModel(SoftDeleteTimestampBase):
            __tablename__ = "my_table"
            name = Column(String, nullable=False)
    """
    __abstract__ = True

SoftDeleteTimestampBase = declarative_base(cls=SoftDeleteAuditBase)


def get_db():
    """
    Dependency function to get database session.
    Use this in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper function for time-series queries
def get_time_series_query(model, db: Session, days: int = 30, date_column: str = "created_at"):
    """
    Get time-series data for a model.
    
    Args:
        model: SQLAlchemy model class
        db: Database session
        days: Number of days to look back
        date_column: Name of the timestamp column to use
    
    Returns:
        Query object filtered by time range
    """
    from datetime import datetime, timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    column = getattr(model, date_column)
    return db.query(model).filter(column >= cutoff_date)


__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "Base",
    "TimestampBase",  # Recommended: Use this for all models (includes audit fields)
    "SoftDeleteTimestampBase",  # Use this for models that need soft deletion
    "AuditBase",  # Abstract base class with audit fields
    "SoftDeleteAuditBase",  # Abstract base class with audit + soft delete
    "TimestampMixin",  # Mixin for adding timestamps to custom bases
    "SoftDeleteMixin",  # Mixin for adding soft delete functionality
    "CustomBase",  # Base class with common methods
    "get_time_series_query",  # Helper for timeseries queries
]