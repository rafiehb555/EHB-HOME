@echo off
echo ========================================
echo EHB COMPLETE SERVICES ACTIVATION
echo ========================================
echo.

echo [1/10] Checking system requirements...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo [2/10] Starting EHB Home Page (Main System)...
cd "EHB HOME PAGE"
start "EHB Home Page Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul

start "EHB Home Page Frontend" cmd /k "cd frontend && npm start"
timeout /t 5 /nobreak >nul

echo [3/10] Starting PSS Service (Personal Security System)...
cd ..\ehb-PSS
if exist "main.py" (
    start "EHB PSS Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload"
) else (
    echo WARNING: PSS service not found, creating placeholder...
    echo # PSS Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "PSS"} >> main.py
    start "EHB PSS Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload"
)
timeout /t 2 /nobreak >nul

echo [4/10] Starting EMO Service (Easy Management Office)...
cd ..\EMO
if exist "main.py" (
    start "EHB EMO Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload"
) else (
    echo WARNING: EMO service not found, creating placeholder...
    echo # EMO Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "EMO"} >> main.py
    start "EHB EMO Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload"
)
timeout /t 2 /nobreak >nul

echo [5/10] Starting EDR Service (Exam Decision Registration)...
cd ..\EHB-EDR
if exist "main.py" (
    start "EHB EDR Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4002 --reload"
) else (
    echo WARNING: EDR service not found, creating placeholder...
    echo # EDR Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "EDR"} >> main.py
    start "EHB EDR Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4002 --reload"
)
timeout /t 2 /nobreak >nul

echo [6/10] Starting JPS Service (Job Profile System)...
cd ..\EHB-JPS
if exist "main.py" (
    start "EHB JPS Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4004 --reload"
) else (
    echo WARNING: JPS service not found, creating placeholder...
    echo # JPS Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "JPS"} >> main.py
    start "EHB JPS Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4004 --reload"
)
timeout /t 2 /nobreak >nul

echo [7/10] Starting GoSellr Service (E-commerce)...
cd ..\EHB-GOSELLER
if exist "main.py" (
    start "EHB GoSellr Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4005 --reload"
) else (
    echo WARNING: GoSellr service not found, creating placeholder...
    echo # GoSellr Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "GoSellr"} >> main.py
    start "EHB GoSellr Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4005 --reload"
)
timeout /t 2 /nobreak >nul

echo [8/10] Starting Wallet Service...
cd ..\EHB-WALLET
if exist "main.py" (
    start "EHB Wallet Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload"
) else (
    echo WARNING: Wallet service not found, creating placeholder...
    echo # Wallet Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "Wallet"} >> main.py
    start "EHB Wallet Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload"
)
timeout /t 2 /nobreak >nul

echo [9/10] Starting AI Agent Service...
cd ..\..\ehb-agent
if exist "main.py" (
    start "EHB AI Agent Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4007 --reload"
) else (
    echo WARNING: AI Agent service not found, creating placeholder...
    echo # AI Agent Service Placeholder > main.py
    echo from fastapi import FastAPI > main.py
    echo app = FastAPI() >> main.py
    echo @app.get("/health") >> main.py
    echo def health_check(): >> main.py
    echo     return {"status": "healthy", "service": "AI Agent"} >> main.py
    start "EHB AI Agent Service" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 4007 --reload"
)
timeout /t 2 /nobreak >nul

echo [10/10] Starting System Monitor...
cd ..\services
start "EHB System Monitor" cmd /k "python system_monitor.py"

echo.
echo ========================================
echo ALL EHB SERVICES ACTIVATED!
echo ========================================
echo.
echo Services running on:
echo - EHB Home Page: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - PSS Service: http://localhost:4001
echo - EMO Service: http://localhost:4003
echo - EDR Service: http://localhost:4002
echo - JPS Service: http://localhost:4004
echo - GoSellr Service: http://localhost:4005
echo - Wallet Service: http://localhost:5001
echo - AI Agent Service: http://localhost:4007
echo.
echo Admin Dashboard: http://localhost:3000/admin
echo User Dashboard: http://localhost:3000/dashboard
echo API Documentation: http://localhost:8000/docs
echo.
echo System Monitor: Running in background
echo.
pause
