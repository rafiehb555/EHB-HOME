import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

"""
PostgreSQL Setup Script for EHB System
"""

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()


def check_postgresql_installation():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(["psql", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL is installed")
            return True
        else:
            print("❌ PostgreSQL is not installed")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed or not in PATH")
        return False


def create_database_and_user():
    """Create database and user for EHB"""
    print("🗄️  Setting up PostgreSQL database...")

    # Database configuration
    db_name = "ehb_database"
    db_user = "ehb_user"
    db_password = "ehb_password"

    try:
        # Create user
        create_user_cmd = [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"CREATE USER {db_user} WITH PASSWORD '{db_password}';",
        ]

        result = subprocess.run(create_user_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database user created successfully")
        else:
            print(f"⚠️  User might already exist: {result.stderr}")

        # Create database
        create_db_cmd = [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"CREATE DATABASE {db_name} OWNER {db_user};",
        ]

        result = subprocess.run(create_db_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database created successfully")
        else:
            print(f"⚠️  Database might already exist: {result.stderr}")

        # Grant privileges
        grant_cmd = [
            "psql",
            "-U",
            "postgres",
            "-d",
            db_name,
            "-c",
            f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};",
        ]

        result = subprocess.run(grant_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Privileges granted successfully")
        else:
            print(f"⚠️  Error granting privileges: {result.stderr}")

        return True

    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False


def run_docker_compose():
    """Run Docker Compose to start PostgreSQL"""
    print("🐳 Starting PostgreSQL with Docker Compose...")

    try:
        # Change to the project root directory
        project_root = Path(__file__).parent.parent.parent
        os.chdir(project_root)

        # Start PostgreSQL service only
        cmd = ["docker-compose", "up", "-d", "postgres"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ PostgreSQL started successfully with Docker")
            return True
        else:
            print(f"❌ Error starting PostgreSQL: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error running Docker Compose: {e}")
        return False


def wait_for_database():
    """Wait for database to be ready"""
    print("⏳ Waiting for database to be ready...")

    max_attempts = 30
    attempt = 0

    while attempt < max_attempts:
        try:
            # Test database connection
            test_cmd = [
                "psql",
                "-h",
                "localhost",
                "-p",
                "5432",
                "-U",
                "ehb_user",
                "-d",
                "ehb_database",
                "-c",
                "SELECT 1;",
            ]

            result = subprocess.run(test_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Database is ready!")
                return True
            else:
                print(
                    f"⏳ Attempt {attempt + 1}/{max_attempts}: Database not ready yet..."
                )
                time.sleep(2)
                attempt += 1

        except Exception as e:
            print(f"⏳ Attempt {attempt + 1}/{max_attempts}: {e}")
            time.sleep(2)
            attempt += 1

    print("❌ Database did not become ready in time")
    return False


def run_database_setup():
    """Run the database setup script"""
    print("🔧 Running database setup...")

    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent.parent
        os.chdir(backend_dir)

        # Run the setup script
        cmd = ["python", "database/setup.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Database setup completed successfully")
            return True
        else:
            print(f"❌ Database setup failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error running database setup: {e}")
        return False


def run_migrations():
    """Run Alembic migrations"""
    print("🔄 Running database migrations...")

    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent.parent
        os.chdir(backend_dir)

        # Initialize Alembic if not already done
        if not os.path.exists("alembic/versions"):
            init_cmd = ["alembic", "init", "alembic"]
            subprocess.run(init_cmd, capture_output=True)

        # Create initial migration
        revision_cmd = [
            "alembic",
            "revision",
            "--autogenerate",
            "-m",
            "Initial migration",
        ]
        result = subprocess.run(revision_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Migration created successfully")
        else:
            print(f"⚠️  Migration creation: {result.stderr}")

        # Apply migrations
        upgrade_cmd = ["alembic", "upgrade", "head"]
        result = subprocess.run(upgrade_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Migrations applied successfully")
            return True
        else:
            print(f"❌ Error applying migrations: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Starting EHB PostgreSQL Setup...")
    print("=" * 50)

    # Check PostgreSQL installation
    if not check_postgresql_installation():
        print("\n📋 PostgreSQL Installation Instructions:")
        print("1. Download PostgreSQL from: https://www.postgresql.org/download/")
        print("2. Install with default settings")
        print("3. Add PostgreSQL bin directory to your PATH")
        print("4. Run this script again")
        return

    # Try to start with Docker Compose first
    if run_docker_compose():
        print("✅ Using Docker Compose for PostgreSQL")
    else:
        print("⚠️  Docker Compose failed, trying local PostgreSQL...")
        if not create_database_and_user():
            print("❌ Failed to create database and user")
            return

    # Wait for database to be ready
    if not wait_for_database():
        print("❌ Database is not accessible")
        return

    # Run database setup
    if not run_database_setup():
        print("❌ Database setup failed")
        return

    # Run migrations
    if not run_migrations():
        print("❌ Migration failed")
        return

    print("\n🎉 EHB PostgreSQL Setup Completed Successfully!")
    print("=" * 50)
    print("\n📋 Database Information:")
    print(f"Host: localhost")
    print(f"Port: 5432")
    print(f"Database: ehb_database")
    print(f"Username: ehb_user")
    print(f"Password: ehb_password")
    print(
        f"Connection URL: postgresql://ehb_user:ehb_password@localhost:5432/ehb_database"
    )

    print("\n📋 Next Steps:")
    print("1. Update your .env file with the database URL")
    print("2. Start your application: python -m uvicorn app.main:app --reload")
    print("3. Access the API at: http://localhost:8000")
    print("4. View API documentation at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
