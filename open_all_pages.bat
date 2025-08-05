@echo off
echo Opening all EHB pages in browser...

REM Wait a moment for servers to be ready
timeout /t 2 /nobreak >nul

REM Open all pages
start http://localhost:3000
timeout /t 1 /nobreak >nul

start http://localhost:3000/dashboard
timeout /t 1 /nobreak >nul

start http://localhost:3000/sql-system
timeout /t 1 /nobreak >nul

start http://localhost:3000/pss
timeout /t 1 /nobreak >nul

start http://localhost:3000/emo
timeout /t 1 /nobreak >nul

start http://localhost:8000/docs

echo All pages opened successfully!
echo.
echo Pages opened:
echo - Home Page: http://localhost:3000
echo - Dashboard: http://localhost:3000/dashboard
echo - SQL System: http://localhost:3000/sql-system
echo - PSS System: http://localhost:3000/pss
echo - EMO System: http://localhost:3000/emo
echo - API Docs: http://localhost:8000/docs
echo.
pause
