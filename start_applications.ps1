# EHB Applications Auto-Start Script for Windows
# Automatically starts frontend and backend servers and opens them in browser

Write-Host "🎯 EHB Applications Auto-Start" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Function to check if port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet
        return $connection.TcpTestSucceeded
    }
    catch {
        return $false
    }
}

# Function to wait for server
function Wait-ForServer {
    param([int]$Port, [int]$Timeout = 30)
    Write-Host "⏳ Waiting for server on port $Port..." -ForegroundColor Yellow
    $startTime = Get-Date

    while (((Get-Date) - $startTime).TotalSeconds -lt $Timeout) {
        if (Test-Port -Port $Port) {
            Write-Host "✅ Server on port $Port is ready!" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Seconds 1
    }

    Write-Host "❌ Server on port $Port did not start within $Timeout seconds" -ForegroundColor Red
    return $false
}

# Function to start frontend
function Start-Frontend {
    Write-Host "🚀 Starting Frontend (Next.js)..." -ForegroundColor Cyan

    if (-not (Test-Path "frontend")) {
        Write-Host "❌ Frontend directory not found!" -ForegroundColor Red
        return $false
    }

    try {
        Set-Location "frontend"

        # Check if node_modules exists
        if (-not (Test-Path "node_modules")) {
            Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
            npm install
        }

        # Start the development server
        Write-Host "🌐 Starting Next.js development server..." -ForegroundColor Yellow
        Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Hidden

        # Wait for server to be ready
        if (Wait-ForServer -Port 3000) {
            Write-Host "✅ Frontend started successfully!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Frontend failed to start" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error starting frontend: $_" -ForegroundColor Red
        return $false
    }
    finally {
        Set-Location ".."
    }
}

# Function to start backend
function Start-Backend {
    Write-Host "🚀 Starting Backend (FastAPI)..." -ForegroundColor Cyan

    if (-not (Test-Path "backend")) {
        Write-Host "❌ Backend directory not found!" -ForegroundColor Red
        return $false
    }

    try {
        Set-Location "backend"

        # Check if static directory exists
        if (-not (Test-Path "static")) {
            Write-Host "📁 Creating static directory..." -ForegroundColor Yellow
            New-Item -ItemType Directory -Name "static" -Force | Out-Null
        }

        # Start the FastAPI server
        Write-Host "🌐 Starting FastAPI development server..." -ForegroundColor Yellow
        Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" -WindowStyle Hidden

        # Wait for server to be ready
        if (Wait-ForServer -Port 8000) {
            Write-Host "✅ Backend started successfully!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Backend failed to start" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error starting backend: $_" -ForegroundColor Red
        return $false
    }
    finally {
        Set-Location ".."
    }
}

# Function to open browsers
function Open-Browsers {
    Write-Host "🌐 Opening applications in browser..." -ForegroundColor Cyan

    # Wait a bit for servers to fully initialize
    Start-Sleep -Seconds 3

    try {
        # Open frontend
        Write-Host "📱 Opening Frontend: http://localhost:3000" -ForegroundColor Green
        Start-Process "http://localhost:3000"

        # Wait a bit
        Start-Sleep -Seconds 2

        # Open backend API docs
        Write-Host "📚 Opening Backend API Docs: http://localhost:8000/docs" -ForegroundColor Green
        Start-Process "http://localhost:8000/docs"

        # Wait a bit
        Start-Sleep -Seconds 2

        # Open backend health check
        Write-Host "🏥 Opening Backend Health: http://localhost:8000/health" -ForegroundColor Green
        Start-Process "http://localhost:8000/health"

        Write-Host "✅ All applications opened in browser!" -ForegroundColor Green

    }
    catch {
        Write-Host "❌ Error opening browsers: $_" -ForegroundColor Red
    }
}

# Main execution
try {
    # Start frontend
    $frontendSuccess = Start-Frontend

    # Start backend
    $backendSuccess = Start-Backend

    if ($frontendSuccess -and $backendSuccess) {
        Write-Host ""
        Write-Host "🎉 Both servers started successfully!" -ForegroundColor Green
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "📚 Backend API: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "🏥 Health Check: http://localhost:8000/health" -ForegroundColor Cyan
        Write-Host "==================================================" -ForegroundColor Green

        # Open browsers
        Open-Browsers

        Write-Host ""
        Write-Host "🚀 Applications are running!" -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow

        # Keep the script running
        try {
            while ($true) {
                Start-Sleep -Seconds 1
            }
        }
        catch {
            Write-Host ""
            Write-Host "🛑 Stopping servers..." -ForegroundColor Yellow
        }

    }
    else {
        Write-Host ""
        Write-Host "❌ Failed to start one or more servers" -ForegroundColor Red
        if (-not $frontendSuccess) {
            Write-Host "- Frontend failed to start" -ForegroundColor Red
        }
        if (-not $backendSuccess) {
            Write-Host "- Backend failed to start" -ForegroundColor Red
        }
    }
}
catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}
