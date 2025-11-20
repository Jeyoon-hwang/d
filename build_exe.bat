@echo off
REM LOL AI Assistant EXE 빌드 스크립트 (Windows)

echo ========================================
echo LOL AI Assistant EXE Builder
echo ========================================
echo.

REM 가상환경 활성화 (있을 경우)
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM PyInstaller 설치 확인
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM 이전 빌드 정리
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM EXE 빌드
echo.
echo Building EXE file...
echo.

pyinstaller ^
    --name=LOL_AI_Assistant ^
    --onefile ^
    --windowed ^
    --add-data="src;src" ^
    --hidden-import=PyQt5 ^
    --hidden-import=requests ^
    --hidden-import=dotenv ^
    --clean ^
    --noconfirm ^
    src/gui/modern_window.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
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
