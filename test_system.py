#!/usr/bin/env python3
"""
간단한 테스트 실행 파일
문제 진단용
"""

print("=" * 60)
print("LOL AI Assistant - 시스템 체크")
print("=" * 60)

# 1. Python 버전 확인
import sys
print(f"\n1. Python 버전: {sys.version}")

# 2. 현재 경로 확인
import os
print(f"2. 현재 경로: {os.getcwd()}")

# 3. 필요한 모듈 확인
print("\n3. 필요한 모듈 확인:")

modules_to_check = [
    ('PyQt5', 'PyQt5'),
    ('requests', 'requests'),
    ('dotenv', 'python-dotenv')
]

all_ok = True
for module_name, pip_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"   ✓ {pip_name}")
    except ImportError:
        print(f"   ✗ {pip_name} - 설치 필요!")
        all_ok = False

# 4. 프로젝트 구조 확인
print("\n4. 프로젝트 구조 확인:")
required_paths = [
    'src',
    'src/gui',
    'src/api',
    'src/data',
    'src/ai',
    'src/gui/modern_window.py'
]

for path in required_paths:
    if os.path.exists(path):
        print(f"   ✓ {path}")
    else:
        print(f"   ✗ {path} - 없음!")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✓ 모든 체크 통과!")
    print("\n이제 실행하세요:")
    print("  python main.py")
else:
    print("✗ 문제 발견!")
    print("\n해결 방법:")
    print("  pip install PyQt5 requests python-dotenv")

print("=" * 60)
input("\nEnter를 눌러 종료...")
