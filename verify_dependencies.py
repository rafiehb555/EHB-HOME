import sys
import importlib
from typing import List, Tuple


#!/usr/bin/env python3
"""
EHB Dependencies Verification Script
Tests all installed dependencies for the EHB project
"""


def test_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Test if a module can be imported successfully"""
    try:
        if package_name:
            module = importlib.import_module(package_name)
        else:
            module = importlib.import_module(module_name)
        return (
            True,
            f"✅ {module_name} ({getattr(module, '__version__', 'unknown version')})",
        )
    except ImportError as e:
        return False, f"❌ {module_name} - {str(e)}"
    except Exception as e:
        return False, f"⚠️ {module_name} - {str(e)}"


def main():
    """Main verification function"""
    print("🔍 EHB Dependencies Verification")
    print("=" * 50)

    # Core dependencies
    core_deps = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlalchemy", "sqlalchemy"),
        ("psycopg2", "psycopg2"),
        ("alembic", "alembic"),
        ("pydantic", "pydantic"),
        ("python-dotenv", "dotenv"),
        ("redis", "redis"),
        ("asyncpg", "asyncpg"),
    ]

    # Blockchain dependencies
    blockchain_deps = [
        ("web3", "web3"),
        ("eth-account", "eth_account"),
        ("eth-utils", "eth_utils"),
        ("eth-abi", "eth_abi"),
        ("eth-hash", "eth_hash"),
        ("eth-typing", "eth_typing"),
        ("hexbytes", "hexbytes"),
    ]

    # AI dependencies
    ai_deps = [
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("langchain", "langchain"),
        ("langchain-openai", "langchain_openai"),
        ("langchain-core", "langchain_core"),
        ("tiktoken", "tiktoken"),
    ]

    # Monitoring dependencies
    monitoring_deps = [
        ("prometheus-client", "prometheus_client"),
        ("structlog", "structlog"),
        ("httpx", "httpx"),
        ("aiohttp", "aiohttp"),
    ]

    # Testing dependencies
    testing_deps = [
        ("pytest", "pytest"),
        ("pytest-asyncio", "pytest_asyncio"),
        ("black", "black"),
        ("isort", "isort"),
        ("flake8", "flake8"),
        ("mypy", "mypy"),
    ]

    # Security dependencies
    security_deps = [
        ("python-jose", "jose"),
        ("passlib", "passlib"),
        ("bcrypt", "bcrypt"),
        ("cryptography", "cryptography"),
    ]

    # Utility dependencies
    utility_deps = [
        ("aiofiles", "aiofiles"),
        ("Pillow", "PIL"),
        ("requests", "requests"),
        ("websockets", "websockets"),
    ]

    all_deps = {
        "🚀 Core Dependencies": core_deps,
        "🌐 Blockchain Dependencies": blockchain_deps,
        "🤖 AI Dependencies": ai_deps,
        "📊 Monitoring Dependencies": monitoring_deps,
        "🧪 Testing Dependencies": testing_deps,
        "🔒 Security Dependencies": security_deps,
        "🔧 Utility Dependencies": utility_deps,
    }

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    for category, deps in all_deps.items():
        print(f"\n{category}")
        print("-" * 30)

        for dep_name, module_name in deps:
            total_tests += 1
            success, message = test_import(dep_name, module_name)
            print(f"  {message}")

            if success:
                passed_tests += 1
            else:
                failed_tests.append(dep_name)

    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Total Dependencies Tested: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if failed_tests:
        print(f"\n❌ Failed Dependencies:")
        for dep in failed_tests:
            print(f"  - {dep}")

    # System information
    print(f"\n🔧 System Information:")
    print(f"  Python Version: {sys.version}")
    print(f"  Platform: {sys.platform}")

    # Final status
    if passed_tests == total_tests:
        print("\n🎉 ALL DEPENDENCIES VERIFIED SUCCESSFULLY!")
        print("Your EHB project is ready to run!")
        return 0
    else:
        print(f"\n⚠️ {len(failed_tests)} dependencies failed verification.")
        print("Please install missing dependencies before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
