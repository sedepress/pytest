@echo off
echo Phone Classifier Windows 构建工具
echo ==================================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 正在安装依赖...
python -m pip install --upgrade pip
python -m pip install pyinstaller drissionpage

echo 开始构建EXE文件...
python -m PyInstaller phone_classifier_windows.spec --clean --noconfirm

if %errorlevel% equ 0 (
    echo.
    echo ==================================
    echo 构建完成!
    echo EXE文件位置: dist\phone_classifier.exe
    echo 文件夹版本: dist\phone_classifier\
    echo ==================================
) else (
    echo 构建失败，请检查错误信息
)

pause