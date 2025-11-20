# Quick Start Guide - Windows

## Step 1: Install Dependencies

Open Command Prompt and run:

```cmd
pip install -r requirements.txt
pip install pyinstaller
```

## Step 2: Build EXE

### Option A: Use Python script (Recommended)
```cmd
python build_exe.py
```

### Option B: Use Batch file
```cmd
build_exe.bat
```

### Option C: Manual build
```cmd
python -m PyInstaller --name=LOL_AI_Assistant --onefile --windowed --add-data="src;src" --hidden-import=PyQt5 src/gui/modern_window.py
```

## Step 3: Run the App

```cmd
dist\LOL_AI_Assistant.exe
```

## Troubleshooting

### "pyinstaller is not recognized"
```cmd
pip install pyinstaller
```

### "No module named PyQt5"
```cmd
pip install PyQt5
```

### "DLL load failed"
Install Visual C++ Redistributable:
https://aka.ms/vs/17/release/vc_redist.x64.exe

### Permission denied
Run Command Prompt as Administrator

## Alternative: Run without building EXE

```cmd
python main.py
```

This will run the app directly from Python.

---

For detailed build instructions, see BUILD_GUIDE.md
