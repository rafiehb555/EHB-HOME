import glob
import re

#!/usr/bin/env python3
"""
Python Error Fixer
Fixes common Python linting errors automatically
"""


def fix_python_file(file_path):
    """Fix common Python linting errors in a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix 1: Add missing newline at end of file
        if not content.endswith("\n"):
            content += "\n"

        # Fix 2: Remove trailing whitespace
        lines = content.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line.rstrip())
        content = "\n".join(new_lines)

        # Fix 3: Add proper spacing between functions (2 blank lines)
        content = re.sub(
            r"(\n\s*def\s+\w+[^}]*\n[^}]*\n)(\s*def\s+)", r"\1\n\2", content
        )
        content = re.sub(
            r"(\n\s*class\s+\w+[^}]*\n[^}]*\n)(\s*def\s+)", r"\1\n\2", content
        )

        # Fix 4: Add proper spacing between classes (2 blank lines)
        content = re.sub(
            r"(\n\s*class\s+\w+[^}]*\n[^}]*\n)(\s*class\s+)", r"\1\n\2", content
        )

        # Fix 5: Fix import order (standard library first, then third party)
        # This is a simplified fix - in practice you'd use isort
        lines = content.split("\n")
        import_lines = []
        other_lines = []
        in_imports = False

        for line in lines:
            if line.strip().startswith(("import ", "from ")):
                import_lines.append(line)
                in_imports = True
            elif in_imports and line.strip() == "":
                import_lines.append(line)
            else:
                if in_imports and line.strip() != "":
                    in_imports = False
                other_lines.append(line)

        # Reconstruct with proper spacing
        if import_lines:
            content = "\n".join(import_lines) + "\n\n" + "\n".join(other_lines)

        # Only write if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"✅ Already clean: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False


def check_missing_imports(file_path):
    """Check for missing imports and create requirements"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        missing_imports = []

        # Common imports that might be missing
        imports_to_check = [
            "boto3",
            "botocore",
            "google.cloud",
            "openai",
            "anthropic",
            "stripe",
            "paypalrestsdk",
            "sendgrid",
            "twilio",
            "slack_sdk",
            "discord",
            "telegram",
            "psycopg2",
            "redis",
            "sqlalchemy",
            "sentry_sdk",
            "dotenv",
        ]

        for import_name in imports_to_check:
            if import_name in content and f"import {import_name}" not in content:
                missing_imports.append(import_name)

        return missing_imports

    except Exception as e:
        print(f"❌ Error checking imports in {file_path}: {e}")
        return []


def create_requirements_file():
    """Create a comprehensive requirements.txt file"""
    requirements = """# Core Dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Database
redis==5.0.1

# AWS Services
boto3==1.34.0
botocore==1.34.0

# Google Cloud
google-cloud-storage==2.10.0
google-cloud-vision==3.4.4
google-cloud-translate==3.12.0
google-cloud-speech==2.21.0

# AI Services
openai==1.3.7
anthropic==0.7.8
google-generativeai==0.3.2
huggingface-hub==0.19.4

# Payment Services
stripe==7.8.0
paypalrestsdk==1.13.1

# Communication Services
sendgrid==6.10.0
twilio==8.10.0
slack-sdk==3.26.1
discord.py==2.3.2
python-telegram-bot==20.7

# Monitoring
sentry-sdk[fastapi]==1.38.0

# Development Tools
black==23.11.0
flake8==6.1.0
isort==5.12.0
mypy==1.7.1
pre-commit==3.6.0
pytest==7.4.3
pytest-asyncio==0.21.1

# Testing
httpx==0.25.2
pytest-cov==4.1.0
"""

    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✅ Created comprehensive requirements.txt")


def main():
    """Main function to fix all Python files"""
    print("🔧 Fixing Python Linting Errors...")

    # Find all Python files
    python_files = glob.glob("**/*.py", recursive=True)
    python_files = [
        f
        for f in python_files
        if not any(x in f for x in ["venv", "node_modules", "__pycache__"])
    ]

    fixed_count = 0
    total_count = len(python_files)
    missing_imports = set()

    for file_path in python_files:
        if fix_python_file(file_path):
            fixed_count += 1

        # Check for missing imports
        missing = check_missing_imports(file_path)
        missing_imports.update(missing)

    print("\n📊 Summary:")
    print(f"Total Python files: {total_count}")
    print(f"Fixed files: {fixed_count}")
    print(f"Already clean: {total_count - fixed_count}")

    if missing_imports:
        print(f"\n⚠️ Missing imports detected: {', '.join(missing_imports)}")
        print("Creating comprehensive requirements.txt...")
        create_requirements_file()

    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} Python files!")
    else:
        print("\n✅ All Python files are already clean!")


if __name__ == "__main__":
    main()
