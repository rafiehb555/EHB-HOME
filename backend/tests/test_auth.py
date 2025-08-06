import pytest
from app.main import app
from fastapi.testclient import TestClient
from models.database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from utils.database.connection import get_db

# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAuth:
    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "TestPass123",
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["email"] == user_data["email"]
        assert data["is_admin"] is False

    def test_register_user_invalid_email(self):
        """Test user registration with invalid email"""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "full_name": "Test User",
            "password": "TestPass123",
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400

    def test_register_user_weak_password(self):
        """Test user registration with weak password"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "weak",
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400

    def test_login_user(self):
        """Test user login"""
        # First register a user
        user_data = {
            "email": "login@example.com",
            "username": "loginuser",
            "full_name": "Login User",
            "password": "TestPass123",
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Then login
        login_data = {"username": "login@example.com", "password": "TestPass123"}

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["email"] == user_data["email"]

    def test_login_user_invalid_credentials(self):
        """Test user login with invalid credentials"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword",
        }

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401

    def test_get_current_user(self):
        """Test getting current user info"""
        # First register and login
        user_data = {
            "email": "current@example.com",
            "username": "currentuser",
            "full_name": "Current User",
            "password": "TestPass123",
        }
        register_response = client.post("/api/v1/auth/register", json=user_data)
        token = register_response.json()["access_token"]

        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]

    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401


class TestServices:
    def test_get_available_services(self):
        """Test getting available services"""
        response = client.get("/api/v1/services/available-services")
        assert response.status_code == 200

        data = response.json()
        assert "services" in data
        assert len(data["services"]) > 0

    def test_get_services_health(self):
        """Test getting services health"""
        response = client.get("/api/v1/services/health")
        assert response.status_code == 200

        data = response.json()
        assert "total_services" in data
        assert "healthy_services" in data
        assert "unhealthy_services" in data


class TestDashboard:
    def test_get_dashboard_data(self):
        """Test getting dashboard data"""
        response = client.get("/api/dashboard")
        assert response.status_code == 200

        data = response.json()
        assert "users" in data
        assert "services" in data
        assert "transactions" in data
        assert "system" in data

    def test_get_sql_level(self):
        """Test getting SQL level"""
        response = client.get("/api/sql/1")
        assert response.status_code == 200

        data = response.json()
        assert "user_id" in data
        assert "sql_level" in data
        assert "sql_points" in data


if __name__ == "__main__":
    pytest.main([__file__])
