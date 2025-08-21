@echo off
echo Building Windows executable for phone_classifier.py...
echo.

REM Check if PyInstaller is installed
where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller. Please install it manually:
        echo pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Install required dependencies
echo Installing required dependencies...
pip install requests pysocks urllib3
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
        exit /b 1
)

REM Build the executable
echo Building executable...
pyinstaller phone_classifier_windows.spec --clean

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Executables created in:
echo - dist\phone_classifier\phone_classifier.exe (one-folder version)
echo - dist\phone_classifier.exe (one-file version)
echo.
echo You can now run phone_classifier.exe on Windows systems.
pause