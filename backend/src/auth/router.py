from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.models import UserLoginSchema, UserSignupSchema
from auth.utils import hash_password, verify_password, create_access_token
# pyrefly: ignore [missing-import] 
from models.users import UserTable, UserSchema
# pyrefly: ignore [missing-import]
from database import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", tags=["Auth"])
async def login(
    user: UserLoginSchema = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate a user and return a JWT access token."""
    result = await db.execute(
        select(UserTable).where(UserTable.email == user.email)
    )
    registered = result.scalar_one_or_none()

    if registered is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist."
        )

    if not verify_password(user.password, registered.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password."
        )

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", tags=["Auth"], response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def signup(
    user: UserSignupSchema = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Register a new user account."""
    # Check if email is already taken
    result = await db.execute(
        select(UserTable).where(UserTable.email == user.email)
    )
    already_exists = result.scalar_one_or_none()

    if already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )

    if user.password != user.password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match."
        )

    new_user = UserTable(
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    return UserSchema.from_orm_str_id(new_user)