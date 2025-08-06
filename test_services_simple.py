import requests
import time


#!/usr/bin/env python3
"""
Simple EHB Services Test
Quick test to check if services are running
"""


def test_service(url, name):
    """Test a service endpoint"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: Running")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: Connection refused")
        return False
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False


def main():
    """Test all EHB services"""
    print("🧪 Testing EHB Services...")
    print("=" * 40)

    services = [
        ("http://localhost:8000/health", "Backend API"),
        ("http://localhost:4001/health", "PSS Service"),
        ("http://localhost:4002/health", "EDR Service"),
        ("http://localhost:4003/health", "EMO Service"),
    ]

    results = []
    for url, name in services:
        result = test_service(url, name)
        results.append(result)

    print("\n📊 Summary:")
    print("-" * 20)
    running = sum(results)
    total = len(results)
    print(f"Running: {running}/{total} services")

    if running == total:
        print("🎉 All services are running!")
    else:
        print("⚠️  Some services are not running")
        print("\nTo start services manually:")
        print(
            "1. Backend: cd backend && python -m uvicorn app.main:app --reload --port 8000"
        )
        print(
            "2. PSS: cd services/pss && python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload"
        )
        print(
            "3. EMO: cd services/emo && python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload"
        )
        print(
            "4. EDR: cd services/edr && python -m uvicorn main:app --host 0.0.0.0 --port 4002 --reload"
        )


if __name__ == "__main__":
    main()
