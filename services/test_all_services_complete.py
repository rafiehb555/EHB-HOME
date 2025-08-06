#!/usr/bin/env python3
"""
Complete Test Script for EHB Services
Tests all services and provides detailed status
"""

import json
import time
from datetime import datetime

import requests

# Service configuration
SERVICES = {
    "main_backend": {
        "port": 8000,
        "name": "Main Backend API",
        "url": "http://localhost:8000"
    },
    "pss": {
        "port": 4001,
        "name": "PSS Service",
        "url": "http://localhost:4001"
    },
    "emo": {
        "port": 4003,
        "name": "EMO Service",
        "url": "http://localhost:4003"
    },
    "edr": {
        "port": 4002,
        "name": "EDR Service",
        "url": "http://localhost:4002"
    },
    "frontend": {
        "port": 3000,
        "name": "Frontend",
        "url": "http://localhost:3000"
    }
}

def test_service(service_name, config):
    """Test a single service"""
    print(f"🔍 Testing {config['name']}...")

    try:
        # Test health endpoint
        health_url = f"{config['url']}/health"
        start_time = time.time()
        response = requests.get(health_url, timeout=5)
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            print(f"  ✅ {config['name']}: HEALTHY ({response_time:.1f}ms)")
            return {
                "status": "healthy",
                "response_time": response_time,
                "data": response.json()
            }
        else:
            print(f"  ❌ {config['name']}: ERROR (HTTP {response.status_code})")
            return {
                "status": "error",
                "error": f"HTTP {response.status_code}",
                "response_time": response_time
            }

    except requests.exceptions.ConnectionError:
        print(f"  🔴 {config['name']}: OFFLINE (Connection refused)")
        return {
            "status": "offline",
            "error": "Connection refused"
        }
    except requests.exceptions.Timeout:
        print(f"  ⏰ {config['name']}: TIMEOUT")
        return {
            "status": "timeout",
            "error": "Request timeout"
        }
    except Exception as e:
        print(f"  ❌ {config['name']}: ERROR ({str(e)})")
        return {
            "status": "error",
            "error": str(e)
        }

def test_frontend_pages():
    """Test frontend pages"""
    print("\n🎨 Testing Frontend Pages...")

    pages = [
        ("/", "Home Page"),
        ("/dashboard", "Dashboard"),
        ("/admin", "Admin Panel")
    ]

    results = {}
    for path, name in pages:
        try:
            url = f"http://localhost:3000{path}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(f"  ✅ {name}: OK (HTTP 200)")
                results[path] = {"status": "success", "status_code": 200}
            else:
                print(f"  ❌ {name}: ERROR (HTTP {response.status_code})")
                results[path] = {"status": "error", "status_code": response.status_code}

        except Exception as e:
            print(f"  🔴 {name}: OFFLINE ({str(e)})")
            results[path] = {"status": "offline", "error": str(e)}

    return results

def main():
    """Main test function"""
    print("🚀 EHB SERVICES - COMPLETE TEST")
    print("=" * 50)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Test all services
    results = {}
    healthy_count = 0
    total_count = len(SERVICES)

    for service_name, config in SERVICES.items():
        result = test_service(service_name, config)
        results[service_name] = result

        if result["status"] == "healthy":
            healthy_count += 1

    # Test frontend pages
    frontend_results = test_frontend_pages()
    results["frontend_pages"] = frontend_results

    # Calculate summary
    health_percentage = (healthy_count / total_count) * 100

    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Total Services: {total_count}")
    print(f"Healthy Services: {healthy_count}")
    print(f"Health Percentage: {health_percentage:.1f}%")

    if health_percentage >= 80:
        print("🎉 EXCELLENT! Most services are healthy.")
        status = "EXCELLENT"
    elif health_percentage >= 60:
        print("⚠️  WARNING: Some services are having issues.")
        status = "WARNING"
    else:
        print("❌ CRITICAL: Many services are unhealthy.")
        status = "CRITICAL"

    # Save results
    test_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_services": total_count,
            "healthy_services": healthy_count,
            "health_percentage": health_percentage,
            "status": status
        },
        "results": results
    }

    with open("complete_test_results.json", "w") as f:
        json.dump(test_data, f, indent=2)

    print(f"\n💾 Results saved to: complete_test_results.json")
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return 0 if health_percentage >= 60 else 1

if __name__ == "__main__":
    exit(main())
