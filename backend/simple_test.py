import json
import time

import requests

#!/usr/bin/env python3
"""
Simple test runner for basic functionality
"""


def test_backend_health():
    """Test backend health"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False


def test_services_health():
    """Test services health"""
    print("🔍 Testing Services Health...")
    try:
        response = requests.get("http://localhost:8000/api/v1/services/health")
        if response.status_code == 200:
            data = response.json()
            print(
                f"✅ Services health: {data['healthy_services']}/{data['total_services']} healthy"
            )
            return True
        else:
            print(f"❌ Services health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Services health check error: {e}")
        return False


def test_available_services():
    """Test available services"""
    print("🔍 Testing Available Services...")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/services/available-services"
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['services'])} available services")
            for service in data["services"]:
                print(f"   - {service['display_name']} ({service['name']})")
            return True
        else:
            print(f"❌ Available services check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Available services check error: {e}")
        return False


def test_user_registration():
    """Test user registration"""
    print("🔍 Testing User Registration...")
    try:
        user_data = {
            "email": f"test{int(time.time())}@example.com",
            "username": f"testuser{int(time.time())}",
            "full_name": "Test User",
            "password": "TestPass123",
        }

        response = requests.post(
            "http://localhost:8000/api/v1/auth/register", json=user_data
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ User registration successful")
            print(f"   - User ID: {data['user_id']}")
            print(f"   - Email: {data['email']}")
            return data["access_token"]
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   - Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return None


def test_user_login():
    """Test user login"""
    print("🔍 Testing User Login...")
    try:
        login_data = {"username": "test@example.com", "password": "TestPass123"}

        response = requests.post(
            "http://localhost:8000/api/v1/auth/login", data=login_data
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ User login successful")
            return data["access_token"]
        else:
            print(f"❌ User login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None


def test_get_current_user(token):
    """Test getting current user"""
    print("🔍 Testing Get Current User...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Get current user successful")
            print(f"   - User: {data['full_name']} ({data['email']})")
            print(f"   - SQL Level: {data['sql_level']}")
            print(f"   - Status: {data['status']}")
            return True
        else:
            print(f"❌ Get current user failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get current user error: {e}")
        return False


def test_dashboard_data():
    """Test dashboard data"""
    print("🔍 Testing Dashboard Data...")
    try:
        response = requests.get("http://localhost:8000/api/dashboard")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data successful")
            print(f"   - Users: {data['users']['total']}")
            print(f"   - Services: {data['services']['total']}")
            print(f"   - Transactions: {data['transactions']['total']}")
            return True
        else:
            print(f"❌ Dashboard data failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
        return False


def test_individual_services():
    """Test individual services"""
    print("🔍 Testing Individual Services...")
    services = [
        {"name": "PSS", "url": "http://localhost:4001"},
        {"name": "EMO", "url": "http://localhost:4003"},
        {"name": "EDR", "url": "http://localhost:4002"},
    ]

    for service in services:
        try:
            response = requests.get(f"{service['url']}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {service['name']} service is healthy")
            else:
                print(
                    f"❌ {service['name']} service health check failed: {response.status_code}"
                )
        except Exception as e:
            print(f"❌ {service['name']} service error: {e}")


def main():
    """Main test function"""
    print("🧪 EHB Simple Test Runner")
    print("=" * 50)

    # Test backend health
    if not test_backend_health():
        print("❌ Backend is not running. Please start the backend first.")
        return

    # Test services
    test_services_health()
    test_available_services()

    # Test authentication
    token = test_user_registration()
    if token:
        test_get_current_user(token)
    else:
        test_user_login()  # Try with existing user

    # Test dashboard
    test_dashboard_data()

    # Test individual services
    test_individual_services()

    print("\n" + "=" * 50)
    print("✅ Simple tests completed!")


if __name__ == "__main__":
    main()
