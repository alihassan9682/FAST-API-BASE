from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression

# Create a base class that can be used across all services
class CustomBase:
    """Base class with common attributes and methods for all models."""
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name automatically from class name."""
        # Convert CamelCase to snake_case for table names
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

# Create base class with timestamps
class TimestampMixin:
    """Mixin class that adds created_at and updated_at timestamps."""
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # Uses database server time
        nullable=False,
        index=True,  # Added index for better query performance
        comment="Timestamp when the record was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Automatically updates on record modification
        nullable=False,
        index=True,  # Added index for better query performance
        comment="Timestamp when the record was last updated"
    )
    
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="Timestamp when the record was soft deleted (null if not deleted)"
    )
    
    def soft_delete(self, db: Session) -> None:
        """Soft delete the record by setting deleted_at timestamp."""
        self.deleted_at = func.now()
        db.commit()
        db.refresh(self)
    
    def restore(self, db: Session) -> None:
        """Restore a soft-deleted record."""
        self.deleted_at = None
        db.commit()
        db.refresh(self)
    
    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None

# Create base class for models that should be soft deletable
class SoftDeleteMixin:
    """Mixin for models that support soft deletion."""
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        server_default=expression.true(),
        comment="Flag indicating if the record is active (not soft deleted)"
    )

# Create different base classes for different needs
Base = declarative_base(cls=CustomBase)
TimestampBase = declarative_base(cls=CustomBase)
TimestampBase.__bases__ = (TimestampMixin, CustomBase)

# For soft deletable models with timestamps
SoftDeleteTimestampBase = declarative_base(cls=CustomBase)
SoftDeleteTimestampBase.__bases__ = (TimestampMixin, SoftDeleteMixin, CustomBase)