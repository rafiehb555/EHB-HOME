        from sqlalchemy import text
        from utils.database.connection import engine, test_connection




#!/usr/bin/env python3
"""
Simple Database Test
"""

def test_db():
    try:
        print("Testing database connection...")
        # Test connection
        if test_connection():
            print("✅ Connection successful")
        else:
            print("❌ Connection failed")
            return

        # Test queries
        with engine.connect() as conn:
            # Test users table
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"✅ Users table: {count} records")
            except Exception as e:
                print(f"❌ Users table error: {e}")

            # Test services table
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM services"))
                count = result.scalar()
                print(f"✅ Services table: {count} records")
            except Exception as e:
                print(f"❌ Services table error: {e}")

            # Test transactions table
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
                count = result.scalar()
                print(f"✅ Transactions table: {count} records")
            except Exception as e:
                print(f"❌ Transactions table error: {e}")

            # Test wallets table
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM wallets"))
                count = result.scalar()
                print(f"✅ Wallets table: {count} records")
            except Exception as e:
                print(f"❌ Wallets table error: {e}")

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_db()
