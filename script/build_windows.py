#!/usr/bin/env python3
"""
Windows executable builder for phone_classifier.py
This script helps build the Windows executable
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("Windows Executable Builder for phone_classifier.py")
    print("=" * 50)
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("⚠️  Warning: This script is designed for Windows.")
        print("   Current platform:", sys.platform)
        print("   The build may not work correctly on this platform.")
    
    # Install PyInstaller if not present
    if not run_command("pip show pyinstaller", "Checking PyInstaller installation"):
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            print("Failed to install PyInstaller. Please install it manually:")
            print("pip install pyinstaller")
            return False
    
    # Install required dependencies
    deps = ["requests", "pysocks", "urllib3", "setuptools"]
    for dep in deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"Failed to install {dep}")
            return False
    
    # Build the executable
    if not run_command("pyinstaller phone_classifier_windows.spec --clean", "Building executable"):
        print("Build failed!")
        return False
    
    print("\n" + "=" * 50)
    print("✓ Build completed successfully!")
    print("\nExecutables created:")
    print("  - dist\\phone_classifier\\phone_classifier.exe (one-folder version)")
    print("  - dist\\phone_classifier.exe (one-file version)")
    print("\nYou can now run phone_classifier.exe on Windows systems.")
    print("\nTo test the executable:")
    print("  1. Navigate to the dist/ folder")
    print("  2. Double-click phone_classifier.exe")
    print("  3. Or run it from command line: phone_classifier.exe")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)