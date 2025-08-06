import subprocess
import sys
import os
from pathlib import Path


#!/usr/bin/env python3
"""
Test runner for EHB Home Page & Dashboard
"""


def run_tests():
    """Run all tests"""
    print("🧪 Running EHB Tests...")
    print("=" * 50)

    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # Run pytest
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--tb=short",
                "--color=yes",
            ],
            capture_output=True,
            text=True,
        )

        print("Test Results:")
        print("-" * 30)
        print(result.stdout)

        if result.stderr:
            print("Errors:")
            print("-" * 30)
            print(result.stderr)

        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_specific_test(test_file):
    """Run a specific test file"""
    print(f"🧪 Running test: {test_file}")
    print("=" * 50)

    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                f"tests/{test_file}",
                "-v",
                "--tb=short",
                "--color=yes",
            ],
            capture_output=True,
            text=True,
        )

        print("Test Results:")
        print("-" * 30)
        print(result.stdout)

        if result.stderr:
            print("Errors:")
            print("-" * 30)
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Test passed!")
            return True
        else:
            print("❌ Test failed!")
            return False

    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False


def run_coverage():
    """Run tests with coverage"""
    print("🧪 Running tests with coverage...")
    print("=" * 50)

    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "--cov=app",
                "--cov=services",
                "--cov=api",
                "--cov-report=term-missing",
                "--cov-report=html",
                "-v",
            ],
            capture_output=True,
            text=True,
        )

        print("Coverage Results:")
        print("-" * 30)
        print(result.stdout)

        if result.stderr:
            print("Errors:")
            print("-" * 30)
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Coverage test completed!")
            return True
        else:
            print("❌ Coverage test failed!")
            return False

    except Exception as e:
        print(f"❌ Error running coverage: {e}")
        return False


def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "coverage":
            run_coverage()
        elif command == "test" and len(sys.argv) > 2:
            test_file = sys.argv[2]
            run_specific_test(test_file)
        else:
            print("Usage:")
            print("  python run_tests.py              # Run all tests")
            print("  python run_tests.py test <file>  # Run specific test")
            print("  python run_tests.py coverage     # Run with coverage")
    else:
        run_tests()


if __name__ == "__main__":
    main()
