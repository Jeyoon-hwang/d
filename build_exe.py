# Simple EXE Build Script
# Run this file to build LOL_AI_Assistant.exe

import sys
import subprocess
import os

def main():
    print("=" * 60)
    print("LOL AI Assistant - EXE Builder")
    print("=" * 60)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LOL_AI_Assistant",
        "--onefile",
        "--windowed",
        "--add-data=src;src",
        "--hidden-import=PyQt5",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "--clean",
        "--noconfirm",
        "src/gui/modern_window.py"
    ]

    print()
    print("Building EXE file...")
    print()

    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 60)
        print("✓ Build SUCCESS!")
        print("=" * 60)
        print()
        print(f"EXE location: {os.path.join(os.getcwd(), 'dist', 'LOL_AI_Assistant.exe')}")
        print()
        print("You can now run: dist\\LOL_AI_Assistant.exe")

    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("✗ Build FAILED!")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
