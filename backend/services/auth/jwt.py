from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.env'))

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Token data structure
class TokenData:
    def __init__(self, user_id: int, email: str, is_admin: bool = False):
        self.user_id = user_id
        self.email = email
        self.is_admin = is_admin


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        is_admin: bool = payload.get("is_admin", False)

        if user_id is None or email is None:
            return None

        return TokenData(user_id=user_id, email=email, is_admin=is_admin)

    except JWTError:
        return None


def create_user_token(user_id: int, email: str, is_admin: bool = False) -> str:
    """Create token for user"""
    data = {
        "user_id": user_id,
        "email": email,
        "is_admin": is_admin,
        "sub": email
    }
    return create_access_token(data)


def get_token_expiration() -> datetime:
    """Get token expiration time"""
    return datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
