@echo off
echo Starting EHB Frontend...
echo.

echo Installing dependencies...
cd frontend
npm install

echo.
echo Starting Next.js development server...
npm run dev

echo.
echo Frontend started at http://localhost:3000
pause
