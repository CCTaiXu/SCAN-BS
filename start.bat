@echo off
chcp 65001 >nul
echo ========================================
echo   Solidity 漏洞检测系统启动器
echo ========================================
echo.

echo [1/4] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请确保已安装 Python 3.7+
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Node.js，请确保已安装 Node.js 16+
    pause
    exit /b 1
)

echo [2/4] 激活虚拟环境...
if not exist ".venv\Scripts\activate.bat" (
    echo 错误: 未找到虚拟环境，请先运行安装脚本
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo [3/4] 启动后端服务...
start "Solidity检测后端" cmd /k "cd /d %~dp0 && call .venv\Scripts\activate.bat && echo 后端服务启动中... && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000"

echo [4/4] 启动前端服务...
cd frontend\web
start "Solidity检测前端" cmd /k "cd /d %~dp0frontend\web && echo 前端服务启动中... && npm run serve"

echo.
echo ========================================
echo   启动完成！
echo ========================================
echo.
echo 后端 API: http://127.0.0.1:8000
echo 前端界面: http://localhost:8080
echo API 文档: http://127.0.0.1:8000/docs
echo.
echo 按任意键关闭此窗口...
pause >nul