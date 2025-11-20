@echo off
chcp 65001 >nul
REM LOL AI Assistant EXE Builder

echo ========================================
echo LOL AI Assistant EXE Builder
echo ========================================
echo.

REM Check if venv exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install PyInstaller if not installed
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM Build EXE
echo.
echo Building EXE file...
echo.

python -m PyInstaller --name=LOL_AI_Assistant --onefile --windowed --add-data="src;src" --hidden-import=PyQt5 --hidden-import=requests --hidden-import=dotenv --clean --noconfirm src/gui/modern_window.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo Make sure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build SUCCESS!
echo ========================================
echo.
echo EXE file location: dist\LOL_AI_Assistant.exe
echo.
echo You can now run the application!
echo.
pause
