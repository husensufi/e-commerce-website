from typing import Optional
from sqlalchemy import String, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from models.common import Base, TimestampMixin, CommonSchema


# ── ORM Table Model ──────────────────────────────────────────────────────────

class ProductTable(Base, TimestampMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)


# ── Pydantic Schemas ─────────────────────────────────────────────────────────

class ProductSchema(CommonSchema):
    """Response schema — maps ORM → JSON."""
    name: str
    description: str
    price: float

    @classmethod
    def from_orm_str_id(cls, obj: ProductTable) -> "ProductSchema":
        return cls(
            id=str(obj.id),
            name=obj.name,
            description=obj.description,
            price=float(obj.price),
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class ProductCreateSchema(CommonSchema):
    """Request schema for creating a product."""
    id: Optional[str] = None
    name: str
    description: str = ""
    price: Optional[float] = 0.00

    class Config:
        schema_extra = {
            "example": {
                "name": "Wireless Headphones",
                "description": "Premium noise-cancelling headphones",
                "price": 99.99
            }
        }


class ProductUpdateSchema(CommonSchema):
    """Request schema for updating a product (all fields optional)."""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# Keep old names as aliases for backward compatibility
Product = ProductSchema
UpdateProduct = ProductUpdateSchema