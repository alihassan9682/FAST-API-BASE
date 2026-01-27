"""
User model for authentication service.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from apps.auth_service.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(Base):
    """
    User model with automatic audit fields (created_at, updated_at).
    
    Inherits from TimestampBase which automatically provides:
    - id: Primary key
    - created_at: Timestamp when user was created (for audit logging)
    - updated_at: Timestamp when user was last updated (for audit logging)
    
    These fields are essential for timeseries algorithms to rank/match users.
    """
    __tablename__ = "users"
    
    # Note: id, created_at, and updated_at are automatically included from TimestampBase
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
