#!/usr/bin/env python3
"""
Complete EHB Services Startup Script
Starts all services and verifies they're running
"""

import subprocess
import time
import requests
import sys
from datetime import datetime

# Service configuration
SERVICES = {
    "main_backend": {
        "name": "Main Backend API",
        "port": 8000,
        "command": ["python", "-m", "uvicorn", "backend.app.main:app", "--reload", "--port", "8000"],
        "cwd": "."
    },
    "pss": {
        "name": "PSS Service",
        "port": 4001,
        "command": ["python", "main.py"],
        "cwd": "services/pss"
    },
    "emo": {
        "name": "EMO Service", 
        "port": 4003,
        "command": ["python", "main.py"],
        "cwd": "services/emo"
    },
    "edr": {
        "name": "EDR Service",
        "port": 4002,
        "command": ["python", "main.py"],
        "cwd": "services/edr"
    },
    "gosellr": {
        "name": "GoSellr Service",
        "port": 4004,
        "command": ["python", "main.py"],
        "cwd": "services/gosellr"
    }
}

class ServiceManager:
    """Manage all EHB services"""
    
    def __init__(self):
        self.processes = {}
        self.start_time = datetime.now()
    
    def start_service(self, service_name: str, config: dict):
        """Start a single service"""
        try:
            print(f"🚀 Starting {config['name']} on port {config['port']}...")
            
            # Start the service
            process = subprocess.Popen(
                config['command'],
                cwd=config['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[service_name] = {
                'process': process,
                'config': config,
                'started_at': datetime.now()
            }
            
            print(f"  ✅ {config['name']} started (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to start {config['name']}: {str(e)}")
            return False
    
    def start_all_services(self):
        """Start all services"""
        print("🎯 Starting all EHB services...")
        print("=" * 50)
        
        success_count = 0
        for service_name, config in SERVICES.items():
            if self.start_service(service_name, config):
                success_count += 1
            time.sleep(2)  # Give each service time to start
        
        print(f"\n📊 Started {success_count}/{len(SERVICES)} services successfully")
        return success_count
    
    def wait_for_services(self, timeout: int = 30):
        """Wait for services to be ready"""
        print(f"\n⏳ Waiting for services to be ready (timeout: {timeout}s)...")
        
        ready_services = 0
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            ready_services = 0
            
            for service_name, config in SERVICES.items():
                try:
                    response = requests.get(f"http://localhost:{config['port']}/health", timeout=2)
                    if response.status_code == 200:
                        ready_services += 1
                        print(f"  ✅ {config['name']} is ready")
                    else:
                        print(f"  ⏳ {config['name']} starting...")
                except:
                    print(f"  ⏳ {config['name']} starting...")
            
            if ready_services == len(SERVICES):
                print(f"\n🎉 All {ready_services} services are ready!")
                return True
            
            time.sleep(2)
        
        print(f"\n⚠️  Timeout reached. {ready_services}/{len(SERVICES)} services ready")
        return False
    
    def test_all_services(self):
        """Test all services"""
        print("\n🧪 Testing all services...")
        print("=" * 30)
        
        results = {}
        for service_name, config in SERVICES.items():
            try:
                response = requests.get(f"http://localhost:{config['port']}/health", timeout=5)
                if response.status_code == 200:
                    results[service_name] = {
                        "status": "healthy",
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "data": response.json()
                    }
                    print(f"  ✅ {config['name']}: HEALTHY ({response.elapsed.total_seconds()*1000:.1f}ms)")
                else:
                    results[service_name] = {
                        "status": "error",
                        "status_code": response.status_code
                    }
                    print(f"  ❌ {config['name']}: ERROR (HTTP {response.status_code})")
            except Exception as e:
                results[service_name] = {
                    "status": "offline",
                    "error": str(e)
                }
                print(f"  ❌ {config['name']}: OFFLINE")
        
        return results
    
    def print_summary(self, results):
        """Print service summary"""
        print("\n" + "="*60)
        print("📊 EHB SERVICES SUMMARY")
        print("="*60)
        
        healthy_count = sum(1 for r in results.values() if r["status"] == "healthy")
        total_count = len(results)
        
        print(f"Total Services: {total_count}")
        print(f"Healthy Services: {healthy_count}")
        print(f"Health Percentage: {(healthy_count/total_count)*100:.1f}%")
        
        if healthy_count == total_count:
            print("\n🎉 ALL SERVICES ARE HEALTHY!")
            print("🚀 EHB Home Page is 100% COMPLETE!")
        else:
            print(f"\n⚠️  {total_count - healthy_count} services need attention")
        
        print("="*60)
    
    def cleanup(self):
        """Cleanup all processes"""
        print("\n🧹 Cleaning up processes...")
        for service_name, data in self.processes.items():
            try:
                data['process'].terminate()
                print(f"  ✅ Stopped {data['config']['name']}")
            except:
                print(f"  ❌ Failed to stop {data['config']['name']}")

def main():
    """Main function"""
    print("🚀 EHB Home Page - Complete Service Startup")
    print("=" * 50)
    
    manager = ServiceManager()
    
    try:
        # Start all services
        success_count = manager.start_all_services()
        
        if success_count == 0:
            print("❌ No services started successfully")
            return 1
        
        # Wait for services to be ready
        if manager.wait_for_services(timeout=60):
            # Test all services
            results = manager.test_all_services()
            manager.print_summary(results)
            
            if all(r["status"] == "healthy" for r in results.values()):
                print("\n🏆 ACHIEVEMENT UNLOCKED: 100% COMPLETE!")
                print("🎉 All EHB services are running and healthy!")
                return 0
            else:
                print("\n⚠️  Some services need attention")
                return 1
        else:
            print("\n❌ Services failed to start properly")
            return 1
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        manager.cleanup()
        return 1
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        manager.cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 