#!/usr/bin/env python3
"""
EHB System Health Monitor
Monitors all services and provides real-time status
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("system_monitor.log"), logging.StreamHandler()],
)


class EHBSystemMonitor:
    def __init__(self):
        self.services = {
            "backend": {
                "url": "http://localhost:8000/health",
                "port": 8000,
                "name": "Backend API",
            },
            "pss": {
                "url": "http://localhost:4001/health",
                "port": 4001,
                "name": "PSS Service",
            },
            "emo": {
                "url": "http://localhost:4003/health",
                "port": 4003,
                "name": "EMO Service",
            },
            "edr": {
                "url": "http://localhost:4002/health",
                "port": 4002,
                "name": "EDR Service",
            },
            "frontend": {
                "url": "http://localhost:3000",
                "port": 3000,
                "name": "Frontend",
            },
        }

        self.stats = {
            "start_time": datetime.now(),
            "total_checks": 0,
            "successful_checks": 0,
            "failed_checks": 0,
            "system_uptime": 0,
        }

    async def check_service_health(
        self, session: aiohttp.ClientSession, service_key: str, service_info: Dict
    ) -> Dict:
        """Check individual service health"""
        try:
            start_time = time.time()
            async with session.get(service_info["url"], timeout=5) as response:
                response_time = time.time() - start_time

                if response.status == 200:
                    data = await response.json()
                    return {
                        "service": service_key,
                        "name": service_info["name"],
                        "status": "healthy",
                        "response_time": round(response_time, 3),
                        "port": service_info["port"],
                        "data": data,
                    }
                else:
                    return {
                        "service": service_key,
                        "name": service_info["name"],
                        "status": "unhealthy",
                        "response_time": round(response_time, 3),
                        "port": service_info["port"],
                        "error": f"HTTP {response.status}",
                    }
        except Exception as e:
            return {
                "service": service_key,
                "name": service_info["name"],
                "status": "error",
                "response_time": 0,
                "port": service_info["port"],
                "error": str(e),
            }

    def get_system_stats(self) -> Dict:
        """Get system resource statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": round(memory.used / (1024**3), 2),
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
            }
        except Exception as e:
            logging.error(f"Error getting system stats: {e}")
            return {}

    def get_process_info(self) -> List[Dict]:
        """Get information about running Python processes"""
        processes = []
        try:
            for proc in psutil.process_iter(
                ["pid", "name", "cmdline", "cpu_percent", "memory_percent"]
            ):
                if proc.info["name"] == "python.exe":
                    cmdline = (
                        " ".join(proc.info["cmdline"]) if proc.info["cmdline"] else ""
                    )
                    if any(service in cmdline for service in ["uvicorn", "main:app"]):
                        processes.append(
                            {
                                "pid": proc.info["pid"],
                                "cmdline": cmdline,
                                "cpu_percent": proc.info["cpu_percent"],
                                "memory_percent": proc.info["memory_percent"],
                            }
                        )
        except Exception as e:
            logging.error(f"Error getting process info: {e}")

        return processes

    async def monitor_all_services(self) -> Dict:
        """Monitor all EHB services"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for service_key, service_info in self.services.items():
                task = self.check_service_health(session, service_key, service_info)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            service_status = {}
            for result in results:
                if isinstance(result, dict):
                    service_status[result["service"]] = result
                    self.stats["total_checks"] += 1
                    if result["status"] == "healthy":
                        self.stats["successful_checks"] += 1
                    else:
                        self.stats["failed_checks"] += 1
                else:
                    logging.error(f"Service check failed: {result}")

            return service_status

    def print_status_report(
        self, service_status: Dict, system_stats: Dict, processes: List[Dict]
    ):
        """Print comprehensive status report"""
        os.system("cls" if os.name == "nt" else "clear")

        print("=" * 80)
        print("                    EHB SYSTEM HEALTH MONITOR")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Monitor Uptime: {datetime.now() - self.stats['start_time']}")
        print(
            f"Total Checks: {self.stats['total_checks']} | Success: {self.stats['successful_checks']} | Failed: {self.stats['failed_checks']}"
        )
        print()

        # Service Status
        print("SERVICE STATUS:")
        print("-" * 60)
        for service_key, status in service_status.items():
            status_icon = (
                "🟢"
                if status["status"] == "healthy"
                else "🔴"
                if status["status"] == "error"
                else "🟡"
            )
            print(
                f"{status_icon} {status['name']:<20} | Port: {status['port']:<5} | Status: {status['status']:<10} | Response: {status['response_time']}s"
            )
            if "error" in status:
                print(f"    Error: {status['error']}")
        print()

        # System Resources
        if system_stats:
            print("SYSTEM RESOURCES:")
            print("-" * 60)
            print(f"CPU Usage: {system_stats['cpu_percent']}%")
            print(
                f"Memory: {system_stats['memory_percent']}% ({system_stats['memory_used_gb']}GB / {system_stats['memory_total_gb']}GB)"
            )
            print(
                f"Disk: {system_stats['disk_percent']}% ({system_stats['disk_used_gb']}GB / {system_stats['disk_total_gb']}GB)"
            )
            print()

        # Running Processes
        if processes:
            print("RUNNING PROCESSES:")
            print("-" * 60)
            for proc in processes:
                print(
                    f"PID: {proc['pid']:<6} | CPU: {proc['cpu_percent']}% | Memory: {proc['memory_percent']}%"
                )
                print(f"     {proc['cmdline'][:80]}...")
                print()

        # Overall Health
        healthy_services = sum(
            1 for s in service_status.values() if s["status"] == "healthy"
        )
        total_services = len(service_status)
        health_percentage = (
            (healthy_services / total_services) * 100 if total_services > 0 else 0
        )

        print("OVERALL SYSTEM HEALTH:")
        print("-" * 60)
        if health_percentage >= 80:
            print(
                f"🟢 EXCELLENT: {health_percentage:.1f}% of services healthy ({healthy_services}/{total_services})"
            )
        elif health_percentage >= 60:
            print(
                f"🟡 GOOD: {health_percentage:.1f}% of services healthy ({healthy_services}/{total_services})"
            )
        else:
            print(
                f"🔴 POOR: {health_percentage:.1f}% of services healthy ({healthy_services}/{total_services})"
            )

        print("=" * 80)

    async def run_monitor(self, interval: int = 30):
        """Run the system monitor continuously"""
        print("Starting EHB System Health Monitor...")
        print(f"Monitoring interval: {interval} seconds")
        print("Press Ctrl+C to stop")
        print()

        try:
            while True:
                # Monitor services
                service_status = await self.monitor_all_services()

                # Get system stats
                system_stats = self.get_system_stats()

                # Get process info
                processes = self.get_process_info()

                # Print report
                self.print_status_report(service_status, system_stats, processes)

                # Save to log file
                log_data = {
                    "timestamp": datetime.now().isoformat(),
                    "service_status": service_status,
                    "system_stats": system_stats,
                    "stats": self.stats,
                }

                with open("system_monitor.json", "w") as f:
                    json.dump(log_data, f, indent=2)

                # Wait for next check
                await asyncio.sleep(interval)

        except KeyboardInterrupt:
            print("\nStopping EHB System Health Monitor...")
            print("Final Statistics:")
            print(f"Total Checks: {self.stats['total_checks']}")
            print(
                f"Success Rate: {(self.stats['successful_checks'] / self.stats['total_checks'] * 100):.1f}%"
                if self.stats["total_checks"] > 0
                else "No checks performed"
            )


if __name__ == "__main__":
    monitor = EHBSystemMonitor()
    asyncio.run(monitor.run_monitor())
