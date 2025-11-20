"""
AI 의사결정 엔진
게임 상황을 분석하고 최적의 행동을 추천합니다.
맵 인식, 판단력, 전략 결정 등을 처리합니다.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum


class GamePhase(Enum):
    """게임 페이즈"""
    EARLY = "early"  # 0-15분
    MID = "mid"  # 15-30분
    LATE = "late"  # 30분+


class Action(Enum):
    """가능한 행동"""
    FARM = "farm"  # 파밍
    ROAM = "roam"  # 로밍
    TRADE = "trade"  # 딜교환
    RECALL = "recall"  # 귀환
    OBJECTIVE = "objective"  # 오브젝트
    PUSH = "push"  # 푸시
    FREEZE = "freeze"  # 프리즈
    GANK = "gank"  # 갱킹
    TEAMFIGHT = "teamfight"  # 한타
    SPLIT_PUSH = "split_push"  # 스플릿 푸시


class DecisionEngine:
    """AI 의사결정 엔진"""

    def __init__(self):
        """의사결정 엔진 초기화"""
        self.action_weights = self._initialize_weights()

    def _initialize_weights(self) -> Dict:
        """행동별 가중치 초기화"""
        return {
            'farm': {
                'cs_deficit': 0.3,
                'gold_deficit': 0.2,
                'item_timing': 0.2,
                'wave_state': 0.3
            },
            'roam': {
                'level_advantage': 0.25,
                'wave_clear': 0.2,
                'enemy_position': 0.25,
                'objective_timing': 0.3
            },
            'trade': {
                'health_advantage': 0.3,
                'cooldown_advantage': 0.3,
                'minion_advantage': 0.2,
                'level_advantage': 0.2
            },
            'objective': {
                'team_position': 0.3,
                'vision_control': 0.25,
                'enemy_position': 0.25,
                'timing': 0.2
            }
        }

    def analyze_game_state(self, game_state: Dict) -> Dict:
        """
        현재 게임 상태를 분석합니다.

        Args:
            game_state: 게임 상태 정보
                - timestamp: 게임 시간
                - player: 플레이어 정보
                - allies: 아군 정보
                - enemies: 적군 정보
                - objectives: 오브젝트 상태

        Returns:
            분석 결과 및 추천 행동
        """
        timestamp = game_state.get('timestamp', 0)
        phase = self._get_game_phase(timestamp)

        # 여러 요소 분석
        wave_analysis = self._analyze_wave_state(game_state)
        position_analysis = self._analyze_map_position(game_state)
        power_analysis = self._analyze_power_level(game_state)
        objective_analysis = self._analyze_objective_timing(game_state)
        vision_analysis = self._analyze_vision(game_state)

        # 최적의 행동 결정
        recommended_actions = self._decide_action(
            phase, wave_analysis, position_analysis,
            power_analysis, objective_analysis, vision_analysis
        )

        return {
            'phase': phase.value,
            'recommended_actions': recommended_actions,
            'wave_state': wave_analysis,
            'map_position': position_analysis,
            'power_level': power_analysis,
            'objective_priority': objective_analysis,
            'vision_score': vision_analysis
        }

    def _get_game_phase(self, timestamp: int) -> GamePhase:
        """게임 페이즈 반환"""
        if timestamp < 900:  # 15분
            return GamePhase.EARLY
        elif timestamp < 1800:  # 30분
            return GamePhase.MID
        else:
            return GamePhase.LATE

    def _analyze_wave_state(self, game_state: Dict) -> Dict:
        """웨이브 상태 분석"""
        player = game_state.get('player', {})
        lane = player.get('lane', 'mid')

        # 간단한 웨이브 상태 분석
        # 실제로는 미니언 위치, 개수 등을 분석해야 함

        cs = player.get('cs', 0)
        timestamp = game_state.get('timestamp', 0) // 60  # 분

        ideal_cs = timestamp * 10  # 분당 10 CS
        cs_deficit = ideal_cs - cs

        return {
            'state': 'neutral',  # push, freeze, slow_push, neutral
            'cs_deficit': cs_deficit,
            'should_push': cs_deficit < -10,
            'should_freeze': cs_deficit > 10,
            'recommendation': self._get_wave_recommendation(cs_deficit)
        }

    def _get_wave_recommendation(self, cs_deficit: float) -> str:
        """웨이브 관리 추천"""
        if cs_deficit > 15:
            return "CS가 부족합니다! 파밍에 집중하세요"
        elif cs_deficit > 10:
            return "웨이브를 프리즈하여 안전하게 CS를 확보하세요"
        elif cs_deficit < -10:
            return "CS가 앞서고 있습니다. 푸시 후 로밍을 고려하세요"
        else:
            return "웨이브 관리가 양호합니다"

    def _analyze_map_position(self, game_state: Dict) -> Dict:
        """맵 포지션 분석 (맵 인식)"""
        player = game_state.get('player', {})
        allies = game_state.get('allies', [])
        enemies = game_state.get('enemies', [])

        player_pos = player.get('position', {'x': 0, 'y': 0})

        # 가시성 있는 적의 수
        visible_enemies = [e for e in enemies if e.get('visible', False)]

        # 주변 아군의 수
        nearby_allies = self._count_nearby_units(
            player_pos, [a.get('position', {}) for a in allies], 3000
        )

        # 위험도 계산
        danger_level = len(visible_enemies) - nearby_allies

        return {
            'visible_enemies': len(visible_enemies),
            'nearby_allies': nearby_allies,
            'danger_level': danger_level,
            'is_safe': danger_level < 0,
            'recommendation': self._get_position_recommendation(danger_level)
        }

    def _count_nearby_units(self, pos: Dict, other_positions: List[Dict],
                            range_: int) -> int:
        """주변 유닛 수 계산"""
        count = 0
        px, py = pos.get('x', 0), pos.get('y', 0)

        for other_pos in other_positions:
            ox, oy = other_pos.get('x', 0), other_pos.get('y', 0)
            distance = np.sqrt((px - ox) ** 2 + (py - oy) ** 2)

            if distance <= range_:
                count += 1

        return count

    def _get_position_recommendation(self, danger_level: int) -> str:
        """포지셔닝 추천"""
        if danger_level >= 2:
            return "⚠️ 위험! 적이 많습니다. 후퇴하세요"
        elif danger_level == 1:
            return "⚠️ 주의! 아군 지원 없이 싸우지 마세요"
        elif danger_level == 0:
            return "적정 상황입니다"
        else:
            return "✓ 안전합니다. 공격적인 플레이 가능"

    def _analyze_power_level(self, game_state: Dict) -> Dict:
        """파워 레벨 분석"""
        player = game_state.get('player', {})
        lane_enemy = game_state.get('lane_enemy', {})

        player_level = player.get('level', 1)
        enemy_level = lane_enemy.get('level', 1)
        level_diff = player_level - enemy_level

        player_items = player.get('items', [])
        enemy_items = lane_enemy.get('items', [])

        item_advantage = len(player_items) - len(enemy_items)

        player_health_pct = player.get('health', 100) / player.get('max_health', 100)
        enemy_health_pct = lane_enemy.get('health', 100) / lane_enemy.get('max_health', 100)

        health_advantage = player_health_pct - enemy_health_pct

        # 종합 파워 점수
        power_score = (level_diff * 2) + item_advantage + (health_advantage * 5)

        return {
            'level_diff': level_diff,
            'item_advantage': item_advantage,
            'health_advantage': health_advantage,
            'power_score': power_score,
            'can_trade': power_score > 1,
            'can_all_in': power_score > 3,
            'recommendation': self._get_power_recommendation(power_score)
        }

    def _get_power_recommendation(self, power_score: float) -> str:
        """파워 레벨 기반 추천"""
        if power_score > 3:
            return "✓ 올인 가능! 적극적으로 킬을 노리세요"
        elif power_score > 1:
            return "✓ 딜교환 유리. 스킬을 활용하여 견제하세요"
        elif power_score > -1:
            return "균형 상태. 신중하게 플레이하세요"
        elif power_score > -3:
            return "⚠️ 불리한 상황. 안전하게 플레이하세요"
        else:
            return "⚠️ 매우 불리! 타워 밑에서 CS만 먹으세요"

    def _analyze_objective_timing(self, game_state: Dict) -> Dict:
        """오브젝트 타이밍 분석"""
        timestamp = game_state.get('timestamp', 0)
        objectives = game_state.get('objectives', {})

        dragon_alive = objectives.get('dragon_alive', True)
        baron_alive = objectives.get('baron_alive', True)
        herald_alive = objectives.get('herald_alive', True)

        priorities = []

        # 드래곤 타이밍 (5분마다)
        if dragon_alive and timestamp >= 300 and timestamp % 300 < 60:
            priorities.append({
                'type': 'dragon',
                'priority': 8,
                'timing': 'now',
                'recommendation': '드래곤 타이밍입니다! 바텀으로 모이세요'
            })

        # 전령 타이밍 (6-14분)
        if herald_alive and 360 <= timestamp <= 840:
            priorities.append({
                'type': 'herald',
                'priority': 6,
                'timing': 'soon',
                'recommendation': '전령을 확보하여 타워를 밀 수 있습니다'
            })

        # 바론 타이밍 (20분 이후)
        if baron_alive and timestamp >= 1200:
            priorities.append({
                'type': 'baron',
                'priority': 10,
                'timing': 'available',
                'recommendation': '바론을 노릴 수 있습니다. 시야를 확보하세요'
            })

        return {
            'priorities': sorted(priorities, key=lambda x: x['priority'], reverse=True),
            'next_objective': priorities[0] if priorities else None
        }

    def _analyze_vision(self, game_state: Dict) -> Dict:
        """시야 분석"""
        player = game_state.get('player', {})
        vision_score = player.get('vision_score', 0)
        timestamp = game_state.get('timestamp', 0) // 60  # 분

        ideal_vision = timestamp * 1.5  # 분당 1.5 시야 점수
        vision_deficit = ideal_vision - vision_score

        return {
            'vision_score': vision_score,
            'vision_deficit': vision_deficit,
            'needs_more_wards': vision_deficit > 5,
            'recommendation': self._get_vision_recommendation(vision_deficit)
        }

    def _get_vision_recommendation(self, vision_deficit: float) -> str:
        """시야 점수 기반 추천"""
        if vision_deficit > 10:
            return "⚠️ 시야가 매우 부족합니다! 와드를 더 설치하세요"
        elif vision_deficit > 5:
            return "시야 점수가 낮습니다. 와드를 설치하세요"
        elif vision_deficit < -5:
            return "✓ 훌륭한 시야 관리입니다!"
        else:
            return "적정한 시야 점수입니다"

    def _decide_action(self, phase: GamePhase, wave: Dict, position: Dict,
                       power: Dict, objective: Dict, vision: Dict) -> List[Dict]:
        """최적의 행동 결정"""
        actions = []

        # 1. 위험도 확인
        if position['danger_level'] >= 2:
            actions.append({
                'action': Action.RECALL.value,
                'priority': 10,
                'reason': '위험한 상황 - 후퇴 필요'
            })
            return actions

        # 2. 오브젝트 우선순위
        if objective['next_objective']:
            obj = objective['next_objective']
            if obj['priority'] >= 8:
                actions.append({
                    'action': Action.OBJECTIVE.value,
                    'priority': obj['priority'],
                    'reason': obj['recommendation']
                })

        # 3. 파워 레벨 기반 행동
        if power['can_all_in']:
            actions.append({
                'action': Action.TRADE.value,
                'priority': 8,
                'reason': '올인 가능한 상황'
            })
        elif power['can_trade']:
            actions.append({
                'action': Action.TRADE.value,
                'priority': 6,
                'reason': '딜교환 유리'
            })

        # 4. 웨이브 상태 기반
        if wave['should_push']:
            actions.append({
                'action': Action.PUSH.value,
                'priority': 5,
                'reason': '웨이브 푸시 후 로밍'
            })
        elif wave['should_freeze']:
            actions.append({
                'action': Action.FREEZE.value,
                'priority': 7,
                'reason': 'CS 부족 - 프리즈로 안전 파밍'
            })

        # 5. 페이즈별 행동
        if phase == GamePhase.EARLY:
            if wave['cs_deficit'] > 10:
                actions.append({
                    'action': Action.FARM.value,
                    'priority': 9,
                    'reason': '초반 CS 확보 중요'
                })
        elif phase == GamePhase.MID:
            actions.append({
                'action': Action.ROAM.value,
                'priority': 7,
                'reason': '중반 로밍으로 영향력 확대'
            })
        elif phase == GamePhase.LATE:
            actions.append({
                'action': Action.TEAMFIGHT.value,
                'priority': 9,
                'reason': '후반 한타 중요'
            })

        # 6. 시야 부족 시
        if vision['needs_more_wards']:
            actions.append({
                'action': 'ward',
                'priority': 6,
                'reason': '시야 확보 필요'
            })

        # 우선순위 정렬
        actions.sort(key=lambda x: x['priority'], reverse=True)

        return actions[:3]  # 상위 3개 행동 반환
