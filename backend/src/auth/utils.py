from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from auth import SECRET_KEY, ALGORITHM, pwd_context
from auth.models import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain-text password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(email: str, expires_delta: Union[timedelta, None] = None) -> str:
    """Create a signed JWT token encoding the user's email."""
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    payload = {
        "sub": email,  # standard JWT subject claim
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Decode and validate a JWT token, returning the user email."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data.email


def authenticate_user(db_user, password: str) -> bool:
    """Verify a user's password against the stored hash."""
    if not db_user:
        return False
    return verify_password(password, db_user.password)