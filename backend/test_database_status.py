#!/usr/bin/env python3
"""
Database Status Check Script
Tests all database components and connections
"""

import sys
import os
from datetime import datetime

def test_database_connection():
    """Test database connection"""
    try:
        from utils.database.connection import test_connection, engine
        from sqlalchemy import text

        print("🔍 Testing database connection...")

        # Test basic connection
        if test_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
            return False

        # Test table creation
        try:
            from utils.database.connection import create_tables
            create_tables()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False

        # Test basic queries
        try:
            with engine.connect() as conn:
                # Test users table
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.scalar()
                print(f"✅ Users table accessible: {user_count} users")

                # Test services table
                result = conn.execute(text("SELECT COUNT(*) FROM services"))
                service_count = result.scalar()
                print(f"✅ Services table accessible: {service_count} services")

                # Test transactions table
                result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
                transaction_count = result.scalar()
                print(f"✅ Transactions table accessible: {transaction_count} transactions")

                # Test wallets table
                result = conn.execute(text("SELECT COUNT(*) FROM wallets"))
                wallet_count = result.scalar()
                print(f"✅ Wallets table accessible: {wallet_count} wallets")

        except Exception as e:
            print(f"❌ Error testing queries: {e}")
            return False

        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_backend_app():
    """Test backend application"""
    try:
        print("\n🔍 Testing backend application...")

        from app.main import app
        print("✅ Backend app imported successfully")

        # Test auth endpoints
        from api.v1.auth import router as auth_router
        print("✅ Auth router imported successfully")

        # Test services endpoints
        from api.v1.services import router as services_router
        print("✅ Services router imported successfully")

        print("✅ Backend application components working")
        return True

    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    try:
        print("\n🔍 Testing environment configuration...")

        import os
        from dotenv import load_dotenv

        # Load environment
        load_dotenv("../config.env")

        # Check required environment variables
        required_vars = [
            "DATABASE_URL",
            "SECRET_KEY",
            "ALGORITHM"
        ]

        for var in required_vars:
            value = os.getenv(var)
            if value:
                print(f"✅ {var}: Configured")
            else:
                print(f"❌ {var}: Missing")
                return False

        print("✅ Environment configuration complete")
        return True

    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🔧 EHB Database & Backend Status Check")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Run all tests
    tests = [
        ("Environment Configuration", test_environment),
        ("Database Connection", test_database_connection),
        ("Backend Application", test_backend_app)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\n📈 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
