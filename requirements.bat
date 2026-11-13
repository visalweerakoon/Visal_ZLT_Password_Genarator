@echo off
title Visal ZLT Password Generator - Requirements Installer

cd /d "%~dp0"

echo ==========================================
echo   Visal ZLT Password Generator
echo   Installing Requirements
echo ==========================================
echo.

py -m pip install --upgrade pip
if errorlevel 1 goto INSTALL_FAILED

py -m pip install reportlab
if errorlevel 1 goto INSTALL_FAILED

echo.
echo All requirements installed successfully.
echo.
echo Starting application...
echo.

if not exist "run.bat" (
    echo ERROR: run.bat not found!
    pause
    exit /b 1
)

call "run.bat"
exit /b 0

:INSTALL_FAILED
echo.
echo Installation failed. Check your Python installation.
pause
exit /b 1
