@echo off
echo ========================================
echo EHB Production Deployment Script
echo ========================================
echo.

echo [1/6] Checking system requirements...
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

echo [2/6] Installing backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo [3/6] Installing frontend dependencies...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo [4/6] Building frontend for production...
npm run build
if errorlevel 1 (
    echo ERROR: Failed to build frontend
    pause
    exit /b 1
)

echo [5/6] Starting production services...
cd ..
start "EHB Backend API" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

start "EHB PSS Service" cmd /k "cd pss && python -m uvicorn main:app --host 0.0.0.0 --port 4001"
timeout /t 2 /nobreak >nul

start "EHB EMO Service" cmd /k "cd emo && python -m uvicorn main:app --host 0.0.0.0 --port 4003"
timeout /t 2 /nobreak >nul

start "EHB EDR Service" cmd /k "cd edr && python -m uvicorn main:app --host 0.0.0.0 --port 4002"
timeout /t 2 /nobreak >nul

echo [6/6] Starting frontend production server...
start "EHB Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Production Deployment Complete!
echo ========================================
echo.
echo Services running on:
echo - Backend API: http://localhost:8000
echo - PSS Service: http://localhost:4001
echo - EMO Service: http://localhost:4003
echo - EDR Service: http://localhost:4002
echo - Frontend: http://localhost:3000
echo.
echo Admin Dashboard: http://localhost:3000/admin
echo User Dashboard: http://localhost:3000/dashboard
echo.
pause
