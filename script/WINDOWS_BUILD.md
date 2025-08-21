# Windows Executable Build Instructions

## Overview
The current `phone_classifier` executable is built for macOS ARM64 and cannot run on Windows. Follow these instructions to build a Windows-compatible executable.

## Prerequisites
1. **Windows Operating System** (Windows 10/11 recommended)
2. **Python 3.8 or higher** installed on Windows
3. **Administrator privileges** (for package installation)

## Method 1: Using Python Build Script (Recommended)

### Steps:
1. Copy these files to a Windows machine:
   - `phone_classifier.py`
   - `phone_classifier_windows.spec`
   - `build_windows.py`

2. Open Command Prompt as Administrator and navigate to the folder containing the files

3. Run the build script:
   ```cmd
   python build_windows.py
   ```

4. The script will automatically:
   - Install PyInstaller if not present
   - Install required dependencies (requests, pysocks, urllib3)
   - Build the Windows executable
   - Create both one-file and one-folder versions

## Method 2: Manual Build

### Step 1: Install Dependencies
Open Command Prompt as Administrator:
```cmd
pip install pyinstaller requests pysocks urllib3 setuptools
```

### Step 2: Build the Executable
```cmd
pyinstaller phone_classifier_windows.spec --clean
```

### Step 3: Find the Executables
After successful build, you'll find:
- `dist\phone_classifier.exe` (single executable file)
- `dist\phone_classifier\phone_classifier.exe` (one-folder version)

## Method 3: Using Batch File

1. Copy `build_windows.bat` to the Windows machine
2. Double-click `build_windows.bat`
3. Follow the on-screen instructions

## File Locations
After building, the executables will be in the `dist` folder:
- **One-file version**: `dist\phone_classifier.exe` (~15-20MB)
- **One-folder version**: `dist\phone_classifier\phone_classifier.exe` with supporting files

## Testing the Windows Executable

1. **Run the executable**:
   ```cmd
   cd dist
   phone_classifier.exe
   ```

2. **Test with a sample ZIP file**:
   - Place a test ZIP file in the same directory
   - Run the executable
   - Select the ZIP file when prompted
   - Verify it processes correctly

## Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError"**:
   - Ensure all dependencies are installed
   - Run: `pip install requests pysocks urllib3`

2. **"Access Denied"**:
   - Run Command Prompt as Administrator
   - Check antivirus software blocking the executable

3. **"Tkinter not available"**:
   - Install Python with Tcl/Tk support
   - Or reinstall Python ensuring "tcl/tk and IDLE" is selected

4. **Build fails**:
   - Clean the build directory: `pyinstaller --clean`
   - Try the one-folder version first

### If Build Fails:
Try building a simpler version:
```cmd
pyinstaller --onefile --windowed --hidden-import=tkinter --hidden-import=tkinter.filedialog phone_classifier.py
```

## Expected Output
The Windows executable should:
- Open a file selection dialog when run
- Process ZIP files containing JSON data
- Work with SOCKS5 proxies (if configured)
- Create output ZIP files in the same directory
- Show progress information in the console window

## File Size
- macOS version: ~8.4MB
- Windows version: ~15-20MB (larger due to Windows runtime components)

## Distribution
The generated `phone_classifier.exe` can be distributed to other Windows machines without requiring Python installation.