import uuid
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from pydantic import BaseModel
from typing import Optional


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""
    pass


class TimestampMixin:
    """Mixin that adds UUID primary key + timestamps to ORM models."""
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CommonSchema(BaseModel):
    """Pydantic base schema shared by all response models."""
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {uuid.UUID: str, datetime: lambda v: v.isoformat()}
