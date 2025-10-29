# Student Performance Prediction - Startup Script
# This script starts both the backend and frontend servers

Write-Host "Starting Student Performance Prediction Application..." -ForegroundColor Green
Write-Host ""

# Start Backend Server
Write-Host "Starting Backend Server (FastAPI)..." -ForegroundColor Cyan
$backendPath = Join-Path $PSScriptRoot "backend"
$pythonExe = "C:/Python313/python.exe"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'Backend Server Starting...' -ForegroundColor Yellow; $pythonExe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host "Starting Frontend Server (Vite)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; Write-Host 'Frontend Server Starting...' -ForegroundColor Yellow; npm run dev"

Write-Host ""
Write-Host "Application is starting..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend will be available at: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop the servers." -ForegroundColor Yellow
