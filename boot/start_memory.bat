@echo off
chcp 65001 >nul
REM start_memory.bat — 快速记忆加载入口
REM 用法：双击运行，或命令行传参：
REM   start_memory.bat                    仅核心记忆
REM   start_memory.bat LabSOPGuard        核心 + 项目记忆
REM   start_memory.bat LabSOPGuard full   核心 + 项目 + 完整规范

set ROOT=D:\KealanMemory
set PYTHON=python

REM 检查 Python 是否可用
%PYTHON% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 找不到 python 命令，请确认 conda 环境已激活
    pause
    exit /b 1
)

REM 根据参数决定加载模式
if "%1"=="" (
    echo 加载模式：核心记忆
    %PYTHON% "%ROOT%\boot\load_memory.py"
) else if "%2"=="full" (
    echo 加载模式：核心 + 项目 [%1] + 完整规范
    %PYTHON% "%ROOT%\boot\load_memory.py" --project %1 --full
) else (
    echo 加载模式：核心 + 项目 [%1]
    %PYTHON% "%ROOT%\boot\load_memory.py" --project %1
)

if %errorlevel% equ 0 (
    echo.
    echo 已生成：%ROOT%\boot\assembled_context.txt
    echo 请用文本编辑器打开，复制内容粘贴给 Claude。
    REM 自动用记事本打开
    notepad "%ROOT%\boot\assembled_context.txt"
) else (
    echo [错误] 生成失败，请检查 Python 脚本输出
    pause
)
