@echo off
cd /d "%~dp0"
title 5G Healthcare Monitoring Prototype
echo ======================================================================
echo   5G-Enabled Intelligent Healthcare Monitoring Desktop Prototype
echo ======================================================================
echo.
echo [1/2] Verifying Python and Matplotlib environment...
python -c "import tkinter, matplotlib, numpy; print('    All dependencies ready.')"
echo [2/2] Launching Python Desktop Clinical Workstation...
echo.
python gui_app.py
if errorlevel 1 (
    echo.
    echo An error occurred while running the GUI.
    pause
)
