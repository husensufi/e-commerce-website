import uuid
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.products import ProductTable, ProductSchema, ProductCreateSchema, ProductUpdateSchema


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    """Retrieve all products."""
    result = await db.execute(select(ProductTable).order_by(ProductTable.created_at.desc()))
    products = result.scalars().all()
    return [ProductSchema.from_orm_str_id(p) for p in products]


@router.get("/{id}", response_model=ProductSchema)
async def get_product(id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve a single product by UUID."""
    try:
        product_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    result = await db.execute(
        select(ProductTable).where(ProductTable.id == product_uuid)
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    return ProductSchema.from_orm_str_id(product)


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED,
             response_description="Create a new product")
async def create_product(
    product: ProductCreateSchema = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new product."""
    new_product = ProductTable(
        name=product.name,
        description=product.description,
        price=product.price or 0.00,
    )
    db.add(new_product)
    await db.flush()  # assigns DB-generated values (id, timestamps)
    await db.refresh(new_product)
    return ProductSchema.from_orm_str_id(new_product)


@router.put("/{id}", response_model=ProductSchema)
async def update_product(
    id: str,
    product: ProductUpdateSchema = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing product by UUID."""
    try:
        product_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    result = await db.execute(
        select(ProductTable).where(ProductTable.id == product_uuid)
    )
    existing = result.scalar_one_or_none()
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    # Apply only provided fields
    update_data = product.dict(exclude_unset=True, exclude={"id", "created_at", "updated_at"})
    for field, value in update_data.items():
        if value is not None:
            setattr(existing, field, value)

    await db.flush()
    await db.refresh(existing)
    return ProductSchema.from_orm_str_id(existing)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str, db: AsyncSession = Depends(get_db)):
    """Delete a product by UUID."""
    try:
        product_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    result = await db.execute(
        select(ProductTable).where(ProductTable.id == product_uuid)
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    await db.delete(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)