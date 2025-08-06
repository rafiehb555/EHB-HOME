#!/usr/bin/env python3
"""
Comprehensive Test Script for EHB Home Page Services
Tests all services and their functionality
"""

import asyncio
import json
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict, List

import requests

# Test configuration
SERVICES = {
    "main_backend": {"port": 8000, "name": "Main Backend API"},
    "pss": {"port": 4001, "name": "PSS Service"},
    "emo": {"port": 4003, "name": "EMO Service"},
    "edr": {"port": 4002, "name": "EDR Service"},
    "gosellr": {"port": 4004, "name": "GoSellr Service"},
    "frontend": {"port": 3000, "name": "Frontend Application"}
}

class ServiceTester:
    """Test all EHB services"""

    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()

    def test_service_health(self, service_name: str, port: int) -> Dict[str, Any]:
        """Test if a service is responding"""
        try:
            url = f"http://localhost:{port}/health"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds() * 1000,
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "response_time": response.elapsed.total_seconds() * 1000
                }
        except requests.exceptions.ConnectionError:
            return {
                "status": "offline",
                "error": "Connection refused",
                "response_time": None
            }
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "error": "Request timeout",
                "response_time": None
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "response_time": None
            }

    def test_main_backend_endpoints(self) -> Dict[str, Any]:
        """Test main backend API endpoints"""
        base_url = "http://localhost:8000"
        endpoints = {
            "health": "/health",
            "services": "/api/services",
            "dashboard": "/api/dashboard",
            "stats": "/api/stats/overview"
        }

        results = {}
        for name, endpoint in endpoints.items():
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                results[name] = {
                    "status": "success" if response.status_code == 200 else "error",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds() * 1000
                }
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e)
                }

        return results

    def test_frontend_pages(self) -> Dict[str, Any]:
        """Test frontend pages"""
        base_url = "http://localhost:3000"
        pages = ["/", "/dashboard", "/services"]

        results = {}
        for page in pages:
            try:
                response = requests.get(f"{base_url}{page}", timeout=5)
                results[page] = {
                    "status": "success" if response.status_code == 200 else "error",
                    "status_code": response.status_code,
                    "content_length": len(response.content)
                }
            except Exception as e:
                results[page] = {
                    "status": "error",
                    "error": str(e)
                }

        return results

    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive tests"""
        print("🧪 Starting comprehensive service tests...")

        # Test service health
        for service_name, config in SERVICES.items():
            print(f"  Testing {config['name']} (port {config['port']})...")
            self.results[service_name] = self.test_service_health(service_name, config['port'])

        # Test main backend endpoints
        print("  Testing main backend endpoints...")
        self.results["main_backend_endpoints"] = self.test_main_backend_endpoints()

        # Test frontend pages
        print("  Testing frontend pages...")
        self.results["frontend_pages"] = self.test_frontend_pages()

        # Calculate summary
        self.results["summary"] = self.calculate_summary()

        return self.results

    def calculate_summary(self) -> Dict[str, Any]:
        """Calculate test summary"""
        total_services = len(SERVICES)
        healthy_services = 0
        total_response_time = 0
        response_times = []

        for service_name in SERVICES.keys():
            if service_name in self.results:
                result = self.results[service_name]
                if result["status"] == "healthy":
                    healthy_services += 1
                    if "response_time" in result and result["response_time"]:
                        response_times.append(result["response_time"])
                        total_response_time += result["response_time"]

        avg_response_time = total_response_time / len(response_times) if response_times else 0

        return {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "unhealthy_services": total_services - healthy_services,
            "health_percentage": (healthy_services / total_services) * 100,
            "average_response_time": avg_response_time,
            "test_duration": (datetime.now() - self.start_time).total_seconds(),
            "timestamp": datetime.now().isoformat()
        }

    def print_results(self):
        """Print test results in a formatted way"""
        print("\n" + "="*60)
        print("📊 EHB SERVICES TEST RESULTS")
        print("="*60)

        # Service health results
        print("\n🔍 SERVICE HEALTH:")
        for service_name, config in SERVICES.items():
            if service_name in self.results:
                result = self.results[service_name]
                status_icon = "✅" if result["status"] == "healthy" else "❌"
                response_time = f"{result['response_time']:.1f}ms" if result.get("response_time") else "N/A"
                print(f"  {status_icon} {config['name']}: {result['status']} ({response_time})")

        # Main backend endpoints
        if "main_backend_endpoints" in self.results:
            print("\n🌐 MAIN BACKEND ENDPOINTS:")
            for endpoint, result in self.results["main_backend_endpoints"].items():
                status_icon = "✅" if result["status"] == "success" else "❌"
                response_time = f"{result['response_time']:.1f}ms" if "response_time" in result else "N/A"
                print(f"  {status_icon} {endpoint}: {result['status']} ({response_time})")

        # Frontend pages
        if "frontend_pages" in self.results:
            print("\n🎨 FRONTEND PAGES:")
            for page, result in self.results["frontend_pages"].items():
                status_icon = "✅" if result["status"] == "success" else "❌"
                print(f"  {status_icon} {page}: {result['status']} (HTTP {result.get('status_code', 'N/A')})")

        # Summary
        if "summary" in self.results:
            summary = self.results["summary"]
            print(f"\n📈 SUMMARY:")
            print(f"  Total Services: {summary['total_services']}")
            print(f"  Healthy Services: {summary['healthy_services']}")
            print(f"  Health Percentage: {summary['health_percentage']:.1f}%")
            print(f"  Average Response Time: {summary['average_response_time']:.1f}ms")
            print(f"  Test Duration: {summary['test_duration']:.2f}s")

        print("\n" + "="*60)

    def save_results(self, filename: str = "test_results.json"):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"💾 Test results saved to {filename}")

def main():
    """Main test function"""
    print("🚀 EHB Home Page - Comprehensive Service Test")
    print("=" * 50)

    tester = ServiceTester()
    results = tester.run_all_tests()

    tester.print_results()
    tester.save_results()

    # Return exit code based on health percentage
    summary = results.get("summary", {})
    health_percentage = summary.get("health_percentage", 0)

    if health_percentage >= 80:
        print("🎉 Excellent! Most services are healthy.")
        return 0
    elif health_percentage >= 60:
        print("⚠️  Warning: Some services are having issues.")
        return 1
    else:
        print("❌ Critical: Many services are unhealthy.")
        return 2

if __name__ == "__main__":
    sys.exit(main())
