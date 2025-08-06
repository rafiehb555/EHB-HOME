import requests
import time
import json
from datetime import datetime
from typing import Dict, List


#!/usr/bin/env python3
"""
EHB Service Status Monitor
Checks the health of all EHB services
"""

# Service configurations
SERVICES = {
    "pss": {"port": 4001, "name": "Personal Security System"},
    "emo": {"port": 4003, "name": "Easy Management Office"},
    "edr": {"port": 4002, "name": "Exam Decision Registration"},
    "jps": {"port": 4004, "name": "Job Profile System"},
    "gosellr": {"port": 4005, "name": "GoSellr Marketplace"},
    "wallet": {"port": 4006, "name": "EHB Wallet"},
    "ai-agent": {"port": 4007, "name": "AI Agent"},
    "ai-robot": {"port": 4008, "name": "AI Robot"},
}


def check_service_health(service_name: str, port: int) -> Dict:
    """Check individual service health"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            return {
                "service": service_name,
                "status": "✅ Healthy",
                "port": port,
                "response_time": response.elapsed.total_seconds(),
                "data": response.json(),
            }
        else:
            return {
                "service": service_name,
                "status": "⚠️ Unhealthy",
                "port": port,
                "error": f"HTTP {response.status_code}",
            }
    except requests.exceptions.ConnectionError:
        return {
            "service": service_name,
            "status": "❌ Not Running",
            "port": port,
            "error": "Connection refused",
        }
    except requests.exceptions.Timeout:
        return {
            "service": service_name,
            "status": "⏰ Timeout",
            "port": port,
            "error": "Request timeout",
        }
    except Exception as e:
        return {
            "service": service_name,
            "status": "❌ Error",
            "port": port,
            "error": str(e),
        }


def check_backend_health() -> Dict:
    """Check main backend health"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            return {
                "service": "Backend API",
                "status": "✅ Healthy",
                "port": 8000,
                "response_time": response.elapsed.total_seconds(),
                "data": response.json(),
            }
        else:
            return {
                "service": "Backend API",
                "status": "⚠️ Unhealthy",
                "port": 8000,
                "error": f"HTTP {response.status_code}",
            }
    except requests.exceptions.ConnectionError:
        return {
            "service": "Backend API",
            "status": "❌ Not Running",
            "port": 8000,
            "error": "Connection refused",
        }
    except Exception as e:
        return {
            "service": "Backend API",
            "status": "❌ Error",
            "port": 8000,
            "error": str(e),
        }


def display_status_table(statuses: List[Dict]):
    """Display status in a formatted table"""
    print("\n" + "=" * 80)
    print("🔍 EHB SERVICE STATUS MONITOR")
    print("=" * 80)
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Header
    print(f"{'Service':<25} {'Status':<15} {'Port':<8} {'Details':<30}")
    print("-" * 80)

    # Backend status
    backend = statuses[0]
    details = backend.get("error", f"Response: {backend.get('response_time', 'N/A')}s")
    print(
        f"{backend['service']:<25} {backend['status']:<15} {backend['port']:<8} {details:<30}"
    )

    # Service statuses
    for status in statuses[1:]:
        details = status.get(
            "error", f"Response: {status.get('response_time', 'N/A')}s"
        )
        print(
            f"{status['service']:<25} {status['status']:<15} {status['port']:<8} {details:<30}"
        )

    print("-" * 80)

    # Summary
    healthy = sum(1 for s in statuses if "✅" in s["status"])
    total = len(statuses)
    print(f"📊 Summary: {healthy}/{total} services healthy")

    if healthy == total:
        print("🎉 All services are running!")
    elif healthy == 0:
        print("🚨 No services are running!")
    else:
        print("⚠️ Some services are not running")


def main():
    """Main monitoring function"""
    print("🔍 Starting EHB Service Status Monitor...")

    # Check all services
    statuses = [check_backend_health()]

    for service_name, config in SERVICES.items():
        status = check_service_health(service_name, config["port"])
        statuses.append(status)

    # Display results
    display_status_table(statuses)

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"service_status_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(
            {"timestamp": datetime.now().isoformat(), "services": statuses}, f, indent=2
        )

    print(f"\n💾 Status saved to: {filename}")
    print("=" * 80)


if __name__ == "__main__":
    main()
