@echo off
title VISAL ZLT Password Generator
cd /d "%~dp0"

echo ==========================================
echo     VISAL ZLT PASSWORD GENERATOR
echo ==========================================
echo.

where py >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not available in PATH.
    pause
    exit /b 1
)

echo Checking requirements...

py -m pip install customtkinter reportlab

if errorlevel 1 (
    echo.
    echo Failed to install requirements.
    pause
    exit /b 1
)

echo.
echo Starting application...
echo.

py Visal_ZLT_Password_Genarator.py

if errorlevel 1 (
    echo.
    echo Application stopped because of an error.
    pause
)
