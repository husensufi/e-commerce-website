from typing import Optional, Union
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from models.common import Base, TimestampMixin, CommonSchema


# ── ORM Table Model ──────────────────────────────────────────────────────────

class UserTable(Base, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


# ── Pydantic Schemas ─────────────────────────────────────────────────────────

class UserSchema(CommonSchema):
    """Response schema — never exposes the password hash."""
    email: str
    full_name: Optional[str] = None
    disabled: bool = False

    @classmethod
    def from_orm_str_id(cls, obj: UserTable) -> "UserSchema":
        return cls(
            id=str(obj.id),
            email=obj.email,
            full_name=obj.full_name,
            disabled=obj.disabled,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


# Keep legacy names
class User(UserSchema):
    pass


class UserInDB(UserSchema):
    hashed_password: str
