@echo off
echo Restarting EHB development server and testing all pages...

REM Kill any existing processes
taskkill /f /im node.exe 2>nul
timeout /t 2 /nobreak >nul

REM Start frontend
cd frontend
start "Frontend" cmd /k "npm run dev"
timeout /t 5 /nobreak >nul

REM Start backend
cd ..\backend
start "Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

REM Wait for servers to start
echo Waiting for servers to start...
timeout /t 10 /nobreak >nul

REM Test all pages
echo Testing all pages...
start http://localhost:3000
timeout /t 2 /nobreak >nul

start http://localhost:3000/dashboard
timeout /t 2 /nobreak >nul

start http://localhost:3000/sql-system
timeout /t 2 /nobreak >nul

start http://localhost:3000/pss
timeout /t 2 /nobreak >nul

start http://localhost:3000/emo
timeout /t 2 /nobreak >nul

start http://localhost:8000/docs

echo.
echo All pages tested! Check browser for any errors.
echo.
echo Pages tested:
echo - Home: http://localhost:3000
echo - Dashboard: http://localhost:3000/dashboard
echo - SQL System: http://localhost:3000/sql-system
echo - PSS: http://localhost:3000/pss
echo - EMO: http://localhost:3000/emo
echo - API Docs: http://localhost:8000/docs
echo.
pause
