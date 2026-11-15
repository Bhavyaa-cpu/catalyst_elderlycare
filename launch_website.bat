@echo off
title Catalyst Care - Web Application Launcher
color 0A
cls
echo ======================================================================
echo          🌿 Catalyst Care - Intelligent Healthcare System 🌿
echo               Smart Geriatric Health & Care Coordination
echo ======================================================================
echo.
echo [1/3] Navigating to project directory...
cd /d "%~dp0"

echo [2/3] Checking database initialization...
if not exist "catalyst_care.db" (
    echo Database not detected. Initializing with sample demo data...
    python init_db.py
)

echo [3/3] Starting Web Application Server on http://localhost:8501...
echo.
echo Your default web browser will open automatically in a moment.
echo (Press Ctrl+C in this terminal window when you want to stop the website)
echo ======================================================================
echo.

python app.py
pause
