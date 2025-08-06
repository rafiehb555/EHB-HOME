from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from models.database.connection import get_db
from services.auth.auth import auth_service, get_current_user, get_current_active_user
from services.auth.jwt import create_tokens, refresh_access_token
from models.database.user import User


router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


# Pydantic models
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    is_verified: bool
    is_active: bool
    is_admin: bool
    sql_level: Optional[str]
    avatar_url: Optional[str]
    company: Optional[str]
    position: Optional[str]
    email_verified: bool
    phone_verified: bool
    kyc_verified: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Validate email
    if not auth_service.validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
        )

    # Validate username
    if not auth_service.validate_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-20 characters, alphanumeric and underscore only",
        )

    # Validate password
    if not auth_service.validate_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters with uppercase, lowercase, and digit",
        )

    # Check if user exists
    existing_user = auth_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    existing_username = auth_service.get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create user
    try:
        user = auth_service.create_user(db, user_data.dict())

        # Create tokens
        tokens = create_tokens(
            user_id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
        )

        return tokens

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = auth_service.authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Account is deactivated"
        )

    # Create tokens
    tokens = create_tokens(
        user_id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
    )

    return tokens


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    """Refresh access token"""
    new_access_token = refresh_access_token(refresh_token)

    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800,  # 30 minutes
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_info(
    user_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update current user information"""
    # Remove sensitive fields
    user_data.pop("password", None)
    user_data.pop("is_admin", None)
    user_data.pop("is_active", None)

    updated_user = auth_service.update_user(db, current_user.id, user_data)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user


@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Change user password"""
    # Validate new password
    if not auth_service.validate_password(password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters with uppercase, lowercase, and digit",
        )

    success = auth_service.change_password(
        db, current_user.id, password_data.old_password, password_data.new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password"
        )

    return {"message": "Password changed successfully"}


@router.post("/logout")
def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Logged out successfully"}
