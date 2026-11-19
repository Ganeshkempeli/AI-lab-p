@echo off
setlocal
echo ======================================================================
echo   Starting N-Queens: Backtracking vs Hill Climbing Streamlit App...
echo ======================================================================

cd /d "%~dp0"

:: 1. Check known local Python 3.13 installation
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto RUN
)

:: 2. Test if python in PATH actually executes
python -c "import sys; sys.exit(0)" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
    goto RUN
)

:: 3. Test py launcher
py -3 -c "import sys; sys.exit(0)" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=py -3"
    goto RUN
)

echo [ERROR] Python 3 was not detected in PATH or standard installation directory.
pause
exit /b 1

:RUN
echo Using Python: %PY_CMD%
"%PY_CMD%" -m streamlit run app.py
pause
endlocal
