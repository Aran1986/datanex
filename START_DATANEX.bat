@echo off
title DataNex Launcher
color 0A

echo.
echo ========================================
echo   DataNex - Starting...
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check Node
echo [2/6] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM Check Docker
echo [3/6] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not running!
    pause
    exit /b 1
)
echo [OK] Docker found
echo.

REM Setup Backend
echo [4/6] Setting up Backend...
if not exist "venv\" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
echo [OK] Backend ready
echo.

REM Setup Frontend
echo [5/6] Setting up Frontend...
cd frontend
if not exist "node_modules\" (
    call npm install
)
cd ..
echo [OK] Frontend ready
echo.

REM Start Docker
echo [6/6] Starting Docker...
docker-compose up -d
timeout /t 5 /nobreak >nul
echo [OK] Docker started
echo.

REM Start Backend
start "DataNex Backend" cmd /k "cd /d "%CD%" && call venv\Scripts\activate.bat && uvicorn api.main:app --reload"
timeout /t 3 /nobreak >nul

REM Start Frontend
start "DataNex Frontend" cmd /k "cd /d "%CD%\frontend" && npm run dev"
timeout /t 10 /nobreak >nul

REM Open Browser
start http://localhost:3000

echo.
echo DataNex is Ready!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo.
pause
