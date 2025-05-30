@echo off
REM 智能旅游规划助手 - 一键自动更新脚本
REM 功能：自动检测destination目录变化并更新index.html
REM 适用系统：Windows

echo ================================================
echo 智能旅游规划助手 - 自动更新系统
echo ================================================
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python！请先安装Python 3.7+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 检测到Python已安装
echo.

REM 检查并安装依赖包
echo 正在检查依赖包...
pip install -r requirements.txt

if errorlevel 1 (
    echo 错误：依赖包安装失败！
    pause
    exit /b 1
)

echo.
echo 依赖包检查完成，开始运行自动更新...
echo.

REM 运行自动更新脚本
python auto_update_index.py

echo.
echo 按任意键退出...
pause >nul 