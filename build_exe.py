"""
LOL AI Assistant EXE 빌드 스크립트
PyInstaller를 사용하여 Windows 실행 파일을 생성합니다.
"""

import PyInstaller.__main__
import os
import sys

# 프로젝트 루트 경로
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 빌드 옵션
PyInstaller.__main__.run([
    'src/gui/modern_window.py',  # 메인 스크립트

    # 출력 설정
    '--name=LOL_AI_Assistant',
    '--onefile',  # 단일 EXE 파일
    '--windowed',  # GUI 앱 (콘솔 숨김)

    # 아이콘 (있을 경우)
    # '--icon=resources/icon.ico',

    # 추가 데이터 파일
    '--add-data=src;src',

    # 숨김 imports
    '--hidden-import=PyQt5',
    '--hidden-import=requests',
    '--hidden-import=dotenv',

    # 출력 디렉토리
    '--distpath=dist',
    '--workpath=build',
    '--specpath=.',

    # 최적화
    '--clean',
    '--noconfirm',

    # 디버그 정보
    # '--debug=all',  # 문제 발생 시 활성화
])

print("\n" + "="*60)
print("✓ EXE 파일 빌드 완료!")
print("="*60)
print(f"\n실행 파일 위치: {os.path.join(ROOT_DIR, 'dist', 'LOL_AI_Assistant.exe')}")
print("\n사용 방법:")
print("1. dist/LOL_AI_Assistant.exe 파일을 실행하세요")
print("2. Riot API 키를 설정하세요")
print("3. 소환사를 분석하거나 실시간 조언을 받으세요!")
print("\n" + "="*60)
