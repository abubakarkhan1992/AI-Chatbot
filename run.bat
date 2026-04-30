@echo off
REM =========================================================================
REM AI Chatbot - Windows Startup Script
REM This script starts both the backend and frontend servers
REM =========================================================================

echo.
echo ========================================
echo   AI Chatbot - Startup Script
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it with your GROQ_API_KEY
    pause
    exit /b 1
)

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

echo Checking dependencies...
pip show uvicorn >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting services...
echo.

REM Create two terminal windows: one for backend, one for frontend
echo Starting Backend (FastAPI on port 8000)...
start cmd /k "cd /d %~dp0 && python -m uvicorn app.main:app --reload --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak

echo Starting Frontend (Streamlit on port 8501)...
start cmd /k "cd /d %~dp0 && streamlit run streamlit_app.py"

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Press Ctrl+C in either terminal to stop the services.
echo.

pause
