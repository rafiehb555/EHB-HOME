#!/usr/bin/env python3
"""
EHB Services Startup Script
Starts all EHB services in separate processes
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_service(name, command, cwd=None):
    """Start a service in a new process"""
    try:
        print(f"🚀 Starting {name}...")
        if cwd:
            os.chdir(cwd)
        
        # Start the service
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print(f"✅ {name} started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    """Start all EHB services"""
    print("🚀 Starting EHB Services...")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Define services to start
    services = [
        {
            "name": "Backend API",
            "command": "python -m uvicorn app.main:app --reload --port 8000",
            "cwd": project_root / "backend"
        },
        {
            "name": "PSS Service",
            "command": "python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload",
            "cwd": project_root / "services" / "pss"
        },
        {
            "name": "EMO Service", 
            "command": "python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload",
            "cwd": project_root / "services" / "emo"
        },
        {
            "name": "EDR Service",
            "command": "python -m uvicorn main:app --host 0.0.0.0 --port 4002 --reload", 
            "cwd": project_root / "services" / "edr"
        }
    ]
    
    processes = []
    
    # Start each service
    for service in services:
        process = start_service(
            service["name"], 
            service["command"],
            service["cwd"]
        )
        if process:
            processes.append((service["name"], process))
    
    print("\n⏳ Waiting for services to initialize...")
    time.sleep(10)
    
    print("\n📊 Service Status:")
    print("-" * 30)
    
    # Check if services are running
    for name, process in processes:
        if process.poll() is None:
            print(f"✅ {name}: Running (PID: {process.pid})")
        else:
            print(f"❌ {name}: Stopped")
    
    print("\n🎯 Services started successfully!")
    print("Access URLs:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:8000")
    print("- PSS Service: http://localhost:4001")
    print("- EMO Service: http://localhost:4003")
    print("- EDR Service: http://localhost:4002")
    
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        for name, process in processes:
            if process.poll() is None:
                process.terminate()
                print(f"🛑 Stopped {name}")
        print("✅ All services stopped")

if __name__ == "__main__":
    main() 