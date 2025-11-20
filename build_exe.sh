#!/bin/bash
# LOL AI Assistant EXE 빌드 스크립트 (Linux/Mac)

echo "========================================"
echo "LOL AI Assistant EXE Builder"
echo "========================================"
echo ""

# 가상환경 활성화 (있을 경우)
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# PyInstaller 설치 확인
echo "Checking PyInstaller..."
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# 이전 빌드 정리
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# EXE 빌드
echo ""
echo "Building executable..."
echo ""

pyinstaller \
    --name=LOL_AI_Assistant \
    --onefile \
    --windowed \
    --add-data="src:src" \
    --hidden-import=PyQt5 \
    --hidden-import=requests \
    --hidden-import=dotenv \
    --clean \
    --noconfirm \
    src/gui/modern_window.py

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "Build FAILED!"
    echo "========================================"
    exit 1
fi

echo ""
echo "========================================"
echo "Build SUCCESS!"
echo "========================================"
echo ""
echo "Executable location: dist/LOL_AI_Assistant"
echo ""
echo "You can now run the application!"
echo ""
