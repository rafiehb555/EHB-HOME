#!/usr/bin/env python3
"""
Test API Endpoints
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:8000"

    print("🧪 Testing EHB API Endpoints")
    print("=" * 50)

    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"📊 Database: {data['database']}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")

    # Test 2: Root Endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root: {data['message']}")
        else:
            print(f"❌ Root failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root error: {e}")

    # Test 3: API Info
    print("\n3. Testing API Info...")
    try:
        response = requests.get(f"{base_url}/api")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Info: {data['name']} v{data['version']}")
            print(f"📋 Available endpoints: {len(data['endpoints'])}")
        else:
            print(f"❌ API Info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API Info error: {e}")

    # Test 4: Services Endpoint
    print("\n4. Testing Services Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/services")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Services: {len(data)} services found")
            for service in data:
                print(f"  - {service['name']} (${service['price_per_month']})")
        else:
            print(f"❌ Services failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Services error: {e}")

    # Test 5: Featured Services
    print("\n5. Testing Featured Services...")
    try:
        response = requests.get(f"{base_url}/api/services/featured")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Featured Services: {len(data)} services found")
        else:
            print(f"❌ Featured Services failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Featured Services error: {e}")

    # Test 6: Stats Overview
    print("\n6. Testing Stats Overview...")
    try:
        response = requests.get(f"{base_url}/api/stats/overview")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats Overview:")
            print(f"  - Users: {data['users']['total']}")
            print(f"  - Services: {data['services']['total']}")
            print(f"  - Transactions: {data['transactions']['total']}")
        else:
            print(f"❌ Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {e}")

    # Test 7: Search Endpoint
    print("\n7. Testing Search Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/search?q=PSS")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search: {data['total_results']} results found")
        else:
            print(f"❌ Search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search error: {e}")

    print("\n" + "=" * 50)
    print("🎯 API Testing Complete!")


def test_database_connection():
    """Test database connection directly"""
    print("\n🔍 Testing Database Connection...")

    try:
        from sqlalchemy import create_engine, text

        # Create engine with the correct URL
        engine = create_engine(
            "postgresql://ehb_user:postgres@localhost:5433/ehb_database",
            echo=False
        )

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")

            # Test services table
            result = conn.execute(text("SELECT COUNT(*) FROM services"))
            service_count = result.fetchone()[0]
            print(f"📊 Services in database: {service_count}")

            # Test users table
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"👥 Users in database: {user_count}")

        return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def main():
    """Main test function"""
    print("🚀 EHB API Testing Suite")
    print("=" * 50)

    # Test database connection
    db_success = test_database_connection()

    # Test API endpoints
    test_api_endpoints()

    if db_success:
        print("\n✅ Database is connected and working!")
    else:
        print("\n❌ Database connection issues detected!")

    print("\n📋 Next Steps:")
    print("1. Check backend logs for errors")
    print("2. Verify database schema is created")
    print("3. Test frontend integration")
    print("4. Deploy to production")


if __name__ == "__main__":
    main()
