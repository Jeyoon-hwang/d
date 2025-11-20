#!/usr/bin/env python3
"""
LOL AI Assistant - 메인 실행 파일
리그 오브 레전드 AI 분석 시스템을 실행합니다.
"""

import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 모던 GUI 사용
from src.gui.modern_window import main

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🎮 LOL AI Assistant - 챌린저급 분석 시스템           ║
    ║                                                              ║
    ║  리그 오브 레전드를 위한 AI 기반 분석 및 조언 시스템        ║
    ║                                                              ║
    ║  주요 기능:                                                  ║
    ║  • 챌린저 리플레이 분석                                     ║
    ║  • 로밍 타이밍 AI                                           ║
    ║  • 실시간 게임 조언                                         ║
    ║  • 챔피언 정보 및 상성                                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    print("✓ 모던 게이밍 UI로 애플리케이션을 시작합니다...\n")

    try:
        main()
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
