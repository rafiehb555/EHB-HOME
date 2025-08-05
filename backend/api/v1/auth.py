from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from utils.database.connection import get_db
from models.database.user import User
from services.auth.auth import authenticate_user, create_user, get_current_user
from services.auth.jwt import create_user_token

router = APIRouter(prefix="/auth", tags=["authentication"])


# Pydantic models for request/response
class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    is_admin: bool


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    sql_level: str
    sql_points: int
    sql_rank: str
    status: str
    is_admin: bool
    verification_progress: float

    class Config:
        from_attributes = True


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        # Create user
        user = create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            username=user_data.username
        )

        # Create access token
        access_token = create_user_token(
            user_id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user"""
    try:
        # Authenticate user
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user is active
        if user.status.value != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is not active"
            )

        # Create access token
        access_token = create_user_token(
            user_id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        sql_level=current_user.sql_level.value,
        sql_points=current_user.sql_points,
        sql_rank=current_user.sql_rank,
        status=current_user.status.value,
        is_admin=current_user.is_admin,
        verification_progress=current_user.verification_progress
    )


@router.post("/logout")
async def logout():
    """Logout user (client should discard token)"""
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token"""
    access_token = create_user_token(
        user_id=current_user.id,
        email=current_user.email,
        is_admin=current_user.is_admin
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=current_user.id,
        email=current_user.email,
        is_admin=current_user.is_admin
    )
