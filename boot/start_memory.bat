@echo off
setlocal
chcp 65001 >nul
REM Quick entrypoint for the local memory loader.
REM Usage:
REM   start_memory.bat
REM   start_memory.bat LabSOPGuard
REM   start_memory.bat LabSOPGuard full

if defined KEALAN_MEMORY_ROOT (
    for %%I in ("%KEALAN_MEMORY_ROOT%") do set "ROOT=%%~fI"
) else (
    for %%I in ("%~dp0..") do set "ROOT=%%~fI"
)

set "PYTHON=python"
set "LOADER=%ROOT%\boot\load_memory.py"
set "OUTPUT=%ROOT%\boot\assembled_context.txt"

%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [error] python command was not found. Activate the expected environment and retry.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo Load mode: core memory
    %PYTHON% "%LOADER%"
) else if /I "%~2"=="full" (
    echo Load mode: core + project [%~1] + optional memory
    %PYTHON% "%LOADER%" --project "%~1" --full
) else (
    echo Load mode: core + project [%~1]
    %PYTHON% "%LOADER%" --project "%~1"
)

if errorlevel 1 (
    echo [error] Generation failed. Check the Python script output above.
    pause
    exit /b 1
)

echo.
echo Generated: %OUTPUT%
if /I not "%KEALAN_MEMORY_NO_NOTEPAD%"=="1" notepad "%OUTPUT%"
