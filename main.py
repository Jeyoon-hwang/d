#!/usr/bin/env python3
"""
LOL AI Assistant - 메인 실행 파일
리그 오브 레전드 AI 분석 시스템을 실행합니다.
"""

import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("LOL AI Assistant 시작 중...")
print("=" * 60)

try:
    print("PyQt5 로딩 중...")
    from PyQt5.QtWidgets import QApplication
    print("✓ PyQt5 로드 완료")

    print("모듈 로딩 중...")
    from src.gui.modern_window import ModernLOLAssistant
    print("✓ 모듈 로드 완료")

    print("애플리케이션 시작...")
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    print("메인 윈도우 생성 중...")
    window = ModernLOLAssistant()

    print("윈도우 표시 중...")
    window.show()

    print("✓ LOL AI Assistant 실행 완료!")
    print("=" * 60)

    sys.exit(app.exec_())

except ImportError as e:
    print(f"\n✗ 모듈 Import 오류: {e}")
    print("\n필요한 패키지를 설치하세요:")
    print("  pip install PyQt5 requests python-dotenv")
    input("\nEnter를 눌러 종료...")
    sys.exit(1)

except Exception as e:
    print(f"\n✗ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    input("\nEnter를 눌러 종료...")
    sys.exit(1)
