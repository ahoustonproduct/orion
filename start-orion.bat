@echo off
echo ============================================
echo   Orion Code - Starting Server
echo ============================================
echo.

echo [1/3] Checking Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo   ERROR: Ollama not found. Make sure Ollama is running.
    pause
    exit /b 1
)
echo   Ollama found.

echo.
echo [2/3] Starting backend on port 8001...
cd /d "%~dp0backend"
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
)
echo   Activating virtual environment and installing dependencies...
call "venv\Scripts\activate.bat"
pip install -r requirements.txt --quiet
start "Orion Backend" /MIN cmd /c "uvicorn main:app --host 0.0.0.0 --port 8001"
cd /d "%~dp0"

echo   Waiting for backend to start...
timeout /t 4 /nobreak >nul

echo.
echo [3/3] Starting frontend on port 3000...
set BACKEND_URL=http://localhost:8001
cd /d "%~dp0frontend"
call npm run dev -- -H 0.0.0.0
