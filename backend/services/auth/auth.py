from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import re

from models.database.connection import get_db
from models.database.user import User
from .jwt import verify_token, get_password_hash, verify_password, create_tokens

# Security scheme
security = HTTPBearer()


class AuthService:
    def __init__(self):
        pass

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    def create_user(self, db: Session, user_data: dict) -> User:
        """Create a new user"""
        # Hash the password
        user_data["password_hash"] = get_password_hash(user_data.pop("password"))

        # Create user
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def update_user(self, db: Session, user_id: int, user_data: dict) -> Optional[User]:
        """Update user information"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        # Update fields
        for field, value in user_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    def change_password(self, db: Session, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Verify old password
        if not verify_password(old_password, user.password_hash):
            return False

        # Hash new password
        user.password_hash = get_password_hash(new_password)
        db.commit()

        return True

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False

        # Check for at least one uppercase, one lowercase, one digit
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False

        return True

    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        # Username should be 3-20 characters, alphanumeric and underscore only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None


# Dependency functions
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


# Create auth service instance
auth_service = AuthService()
