@echo off
REM Student Performance Prediction - Startup Script (Batch)
REM This script starts both the backend and frontend servers

echo Starting Student Performance Prediction Application...
echo.

REM Start Backend Server
echo Starting Backend Server (FastAPI)...
start "Backend Server" cmd /k "cd backend && C:/Python313/python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to initialize
timeout /t 3 /nobreak >nul

REM Start Frontend Server
echo Starting Frontend Server (Vite)...
start "Frontend Server" cmd /k "npm run dev"

echo.
echo Application is starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo.
echo Close the terminal windows to stop the servers.
pause
