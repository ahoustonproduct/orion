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
start "Orion Backend" /MIN cmd /c "cd /d "%~dp0backend" && uvicorn main:app --host 0.0.0.0 --port 8001"

echo   Waiting for backend to start...
timeout /t 4 /nobreak >nul

echo.
echo [3/3] Starting frontend on port 3000...
set BACKEND_URL=http://localhost:8001
cd /d "%~dp0frontend"
call npm run dev
