"""
SQLAlchemy Database Models.
Defines the logical structure and relationships for Users and Tasks.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from database import Base
from enum import Enum

class TaskStatus(str, Enum):
    """Enumeration for the possible states of a task."""
    pending = "pending"
    completed = "completed"

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default=TaskStatus.pending.value, nullable=False)
    due_date = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
