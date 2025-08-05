@echo off
echo 🎯 EHB Applications Auto-Start
echo ==================================================

echo 🚀 Starting Frontend (Next.js)...
cd frontend
start "Frontend" cmd /k "npm run dev"
cd ..

echo 🚀 Starting Backend (FastAPI)...
cd backend
start "Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..

echo ⏳ Waiting for servers to start...
timeout /t 10 /nobreak > nul

echo 🌐 Opening applications in browser...
start http://localhost:3000
timeout /t 2 /nobreak > nul
start http://localhost:8000/docs
timeout /t 2 /nobreak > nul
start http://localhost:8000/health

echo.
echo 🎉 Applications started successfully!
echo ==================================================
echo 📱 Frontend: http://localhost:3000
echo 📚 Backend API: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/health
echo ==================================================
echo.
echo 🚀 Applications are running!
echo Press any key to close this window...
pause > nul
