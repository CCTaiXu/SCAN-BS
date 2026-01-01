@echo off
chcp 65001 >nul
echo ========================================
echo   Solidity 漏洞检测系统安装脚本
echo ========================================
echo.

echo [1/6] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python 版本正常

echo.
echo [2/6] 检查 Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Node.js，请先安装 Node.js 16+
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)
echo Node.js 版本正常

echo.
echo [3/6] 创建 Python 虚拟环境...
if exist ".venv" (
    echo 虚拟环境已存在，跳过创建
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)

echo.
echo [4/6] 激活虚拟环境并安装 Python 依赖...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo 错误: 激活虚拟环境失败
    pause
    exit /b 1
)

pip install --upgrade pip
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo 错误: 安装 Python 依赖失败
    pause
    exit /b 1
)
echo Python 依赖安装完成

echo.
echo [5/6] 安装前端依赖...
cd frontend\web
if not exist "node_modules" (
    npm install
    if errorlevel 1 (
        echo 错误: 安装前端依赖失败
        cd ..\..
        pause
        exit /b 1
    )
) else (
    echo 前端依赖已存在，跳过安装
)
cd ..\..

echo.
echo [6/6] 验证安装...
call .venv\Scripts\activate.bat
python -c "import fastapi, uvicorn, tensorflow; print('Python 依赖验证通过')" >nul 2>&1
if errorlevel 1 (
    echo 警告: Python 依赖验证失败，可能影响功能
) else (
    echo Python 依赖验证通过
)

cd frontend\web
npm list --depth=0 >nul 2>&1
if errorlevel 1 (
    echo 警告: 前端依赖验证失败
) else (
    echo 前端依赖验证通过
)
cd ..\..

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以运行 start.bat 启动系统
echo 或手动执行以下命令:
echo.
echo 启动后端: .venv\Scripts\activate && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
echo 启动前端: cd frontend\web && npm run serve
echo.
pause