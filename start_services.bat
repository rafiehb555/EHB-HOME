@echo off
echo Starting EHB Services...
echo.

echo Starting Backend API on port 8000...
start "Backend API" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8000"

echo Starting PSS Service on port 4001...
start "PSS Service" cmd /k "cd services\pss && python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload"

echo Starting EMO Service on port 4003...
start "EMO Service" cmd /k "cd services\emo && python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload"

echo Starting EDR Service on port 4002...
start "EDR Service" cmd /k "cd services\edr && python -m uvicorn main:app --host 0.0.0.0 --port 4002 --reload"

echo.
echo All services started in separate windows.
echo Wait 10 seconds for services to initialize...
timeout /t 10 /nobreak > nul

echo.
echo Testing services...
cd backend
python simple_test.py

echo.
echo Services startup complete!
pause
