@echo off
REM Human Digital Twin - Quick Start Script for Windows

echo ====================================
echo Human Digital Twin - Quick Start
echo ====================================
echo.
echo This script will start all required services:
echo 1. Backend API (FastAPI)
echo 2. Frontend Server (HTTP)
echo.
echo Two PowerShell windows will open. Keep them running while using the app.
echo Note: The model may take a minute to load on first startup.
echo.
pause

REM Start backend API
echo Starting Backend API on localhost:8000...
start powershell -NoExit -Command "cd d:\hackathon\HUMAN_TWIN; uvicorn backend_api:app --reload --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak

REM Start frontend server
echo Starting Frontend Server on localhost:3000...
start powershell -NoExit -Command "cd d:\hackathon\HUMAN_TWIN; python serve_frontend.py"

timeout /t 2 /nobreak

echo.
echo ====================================
echo Services are starting...
echo ====================================
echo Backend API: http://localhost:8000
echo Frontend:    http://localhost:3000
echo.
echo Open your browser and go to: http://localhost:3000
echo Press Ctrl+C in each window to stop the services.
echo.
pause
