#!/usr/bin/env python3
"""
EHB Applications Auto-Start Script
Automatically starts frontend and backend servers and opens them in browser
"""

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path


def check_port(port):
    """Check if a port is in use"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False


def wait_for_server(port, timeout=30):
    """Wait for server to be ready"""
    print(f"⏳ Waiting for server on port {port}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        if check_port(port):
            print(f"✅ Server on port {port} is ready!")
            return True
        time.sleep(1)

    print(f"❌ Server on port {port} did not start within {timeout} seconds")
    return False


def start_frontend():
    """Start the Next.js frontend"""
    print("🚀 Starting Frontend (Next.js)...")

    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False

    try:
        # Change to frontend directory
        os.chdir(frontend_dir)

        # Check if node_modules exists
        if not Path("node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)

        # Start the development server
        print("🌐 Starting Next.js development server...")
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for server to be ready
        if wait_for_server(3000):
            print("✅ Frontend started successfully!")
            return True
        else:
            print("❌ Frontend failed to start")
            return False

    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False


def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting Backend (FastAPI)...")

    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False

    try:
        # Change to backend directory
        os.chdir(backend_dir)

        # Check if static directory exists
        static_dir = Path("static")
        if not static_dir.exists():
            print("📁 Creating static directory...")
            static_dir.mkdir(exist_ok=True)

        # Start the FastAPI server
        print("🌐 Starting FastAPI development server...")
        process = subprocess.Popen(
            ["python", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for server to be ready
        if wait_for_server(8000):
            print("✅ Backend started successfully!")
            return True
        else:
            print("❌ Backend failed to start")
            return False

    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False


def open_browsers():
    """Open applications in browser"""
    print("🌐 Opening applications in browser...")

    # Wait a bit for servers to fully initialize
    time.sleep(3)

    try:
        # Open frontend
        print("📱 Opening Frontend: http://localhost:3000")
        webbrowser.open("http://localhost:3000")

        # Wait a bit
        time.sleep(2)

        # Open backend API docs
        print("📚 Opening Backend API Docs: http://localhost:8000/docs")
        webbrowser.open("http://localhost:8000/docs")

        # Wait a bit
        time.sleep(2)

        # Open backend health check
        print("🏥 Opening Backend Health: http://localhost:8000/health")
        webbrowser.open("http://localhost:8000/health")

        print("✅ All applications opened in browser!")

    except Exception as e:
        print(f"❌ Error opening browsers: {e}")


def main():
    """Main function"""
    print("🎯 EHB Applications Auto-Start")
    print("=" * 50)

    # Store original directory
    original_dir = os.getcwd()

    try:
        # Start frontend
        frontend_success = start_frontend()

        # Go back to original directory
        os.chdir(original_dir)

        # Start backend
        backend_success = start_backend()

        # Go back to original directory
        os.chdir(original_dir)

        if frontend_success and backend_success:
            print("\n🎉 Both servers started successfully!")
            print("=" * 50)
            print("📱 Frontend: http://localhost:3000")
            print("📚 Backend API: http://localhost:8000")
            print("📖 API Docs: http://localhost:8000/docs")
            print("🏥 Health Check: http://localhost:8000/health")
            print("=" * 50)

            # Open browsers
            open_browsers()

            print("\n🚀 Applications are running!")
            print("Press Ctrl+C to stop all servers")

            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping servers...")

        else:
            print("\n❌ Failed to start one or more servers")
            if not frontend_success:
                print("- Frontend failed to start")
            if not backend_success:
                print("- Backend failed to start")

    except Exception as e:
        print(f"❌ Error: {e}")
        os.chdir(original_dir)


if __name__ == "__main__":
    main()
