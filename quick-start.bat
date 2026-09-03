@echo off
REM Quick Start Script for SEO Analyzer Pro
REM Windows PowerShell / CMD

echo ============================================
echo SEO Analyzer Pro - Quick Start
echo ============================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    exit /b 1
)

echo.
echo [2/4] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    exit /b 1
)

cd ..

echo.
echo [3/4] Checking Node.js...
node --version
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    exit /b 1
)

echo.
echo [4/4] Installing Frontend Dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    exit /b 1
)

cd ..

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Start Backend:
echo    cd backend
echo    python -m uvicorn main:app --reload
echo    (Visit: http://localhost:8000/docs)
echo.
echo 2. Start Frontend (in a new terminal):
echo    cd frontend
echo    npm run dev
echo    (Visit: http://localhost:5173)
echo.
echo ============================================
