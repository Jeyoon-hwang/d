"""
AI 의사결정 엔진 테스트
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai.decision_engine import DecisionEngine


def test_decision_engine():
    """의사결정 엔진 테스트"""
    print("=" * 60)
    print("AI 의사결정 엔진 테스트")
    print("=" * 60)

    engine = DecisionEngine()

    # 테스트 게임 상태 (초반)
    print("\n[시나리오 1] 초반 게임 (6분, 레벨 5)")
    game_state = {
        'timestamp': 360,  # 6분
        'player': {
            'champion': 'Ahri',
            'level': 5,
            'cs': 40,
            'position': {'x': 7000, 'y': 7000},
            'vision_score': 4,
            'health': 80,
            'max_health': 100,
            'items': []
        },
        'allies': [],
        'enemies': [],
        'lane_enemy': {
            'level': 5,
            'health': 60,
            'max_health': 100,
            'items': []
        },
        'objectives': {
            'dragon_alive': True,
            'baron_alive': False,
            'herald_alive': True
        }
    }

    analysis = engine.analyze_game_state(game_state)

    print(f"게임 페이즈: {analysis['phase']}")
    print(f"\n웨이브 상태: {analysis['wave_state']['recommendation']}")
    print(f"맵 포지션: {analysis['map_position']['recommendation']}")
    print(f"파워 레벨: {analysis['power_level']['recommendation']}")

    print("\n추천 행동:")
    for i, action in enumerate(analysis['recommended_actions'], 1):
        print(f"  {i}. {action['action']} (우선순위: {action['priority']}/10)")
        print(f"     → {action['reason']}")

    # 테스트 게임 상태 (중반)
    print("\n\n[시나리오 2] 중반 게임 (18분, 레벨 11)")
    game_state['timestamp'] = 1080  # 18분
    game_state['player']['level'] = 11
    game_state['player']['cs'] = 150
    game_state['objectives']['baron_alive'] = False

    analysis = engine.analyze_game_state(game_state)

    print(f"게임 페이즈: {analysis['phase']}")
    print("\n추천 행동:")
    for i, action in enumerate(analysis['recommended_actions'], 1):
        print(f"  {i}. {action['action']} (우선순위: {action['priority']}/10)")
        print(f"     → {action['reason']}")

    print("\n✓ 테스트 완료!")


if __name__ == '__main__':
    test_decision_engine()
