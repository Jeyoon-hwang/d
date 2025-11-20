"""
리플레이 분석 엔진
챌린저 리플레이를 분석하여 로밍 타이밍, 포지셔닝, CS 패턴 등을 학습합니다.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RoamingEvent:
    """로밍 이벤트 정보"""
    timestamp: int  # 게임 시간 (초)
    from_lane: str  # 출발 라인
    to_lane: str  # 목적지 라인
    champion: str
    level: int
    success: bool  # 로밍 성공 여부 (킬/어시스트 획득)
    wave_state: str  # push, freeze, slow_push
    enemy_summs: List[str]  # 적 소환사 주문 상태
    vision_score: int


@dataclass
class PositioningData:
    """포지셔닝 데이터"""
    timestamp: int
    x: int
    y: int
    champion: str
    team: str
    game_phase: str  # early, mid, late
    nearby_allies: int
    nearby_enemies: int


class ReplayAnalyzer:
    """리플레이 분석기"""

    # 맵 좌표 상수
    MAP_SIZE = 14820
    LANE_ZONES = {
        'top': {'x': (0, 5000), 'y': (9820, 14820)},
        'mid': {'x': (5000, 9820), 'y': (5000, 9820)},
        'bot': {'x': (9820, 14820), 'y': (0, 5000)},
        'jungle': {'x': (3000, 11820), 'y': (3000, 11820)}
    }

    def __init__(self):
        """분석기 초기화"""
        self.roaming_patterns = []
        self.positioning_data = []
        self.cs_patterns = []

    def analyze_match_timeline(self, timeline_data: Dict) -> Dict:
        """
        매치 타임라인을 분석합니다.

        Args:
            timeline_data: Riot API에서 가져온 타임라인 데이터

        Returns:
            분석 결과 딕셔너리
        """
        if not timeline_data or 'info' not in timeline_data:
            return {}

        frames = timeline_data['info'].get('frames', [])

        roaming_events = self._detect_roaming(frames)
        positioning_analysis = self._analyze_positioning(frames)
        cs_analysis = self._analyze_cs_patterns(frames)
        objective_control = self._analyze_objectives(frames)

        return {
            'roaming': roaming_events,
            'positioning': positioning_analysis,
            'cs_patterns': cs_analysis,
            'objectives': objective_control
        }

    def _detect_roaming(self, frames: List[Dict]) -> List[RoamingEvent]:
        """
        로밍 이벤트를 감지합니다.

        로밍 조건:
        1. 라이너가 자신의 라인을 벗어남
        2. 다른 라인이나 정글로 이동
        3. 일정 시간(15초 이상) 체류
        """
        roaming_events = []

        for i, frame in enumerate(frames):
            if i == 0:
                continue

            timestamp = frame.get('timestamp', 0) // 1000  # 밀리초 -> 초
            participants = frame.get('participantFrames', {})

            for participant_id, data in participants.items():
                position = data.get('position', {})
                x, y = position.get('x', 0), position.get('y', 0)

                # 현재 존 파악
                current_zone = self._get_zone(x, y)

                # 이전 프레임과 비교하여 로밍 감지
                if i > 5:  # 최소 5분 후부터 분석
                    prev_positions = self._get_previous_positions(
                        frames, i, participant_id, 3
                    )

                    if self._is_roaming(prev_positions, current_zone):
                        champion_stats = data.get('championStats', {})

                        roaming_event = RoamingEvent(
                            timestamp=timestamp,
                            from_lane=prev_positions[0]['zone'],
                            to_lane=current_zone,
                            champion="Unknown",  # 매치 데이터에서 가져와야 함
                            level=champion_stats.get('level', 0),
                            success=False,  # 킬 이벤트와 연결 필요
                            wave_state="unknown",
                            enemy_summs=[],
                            vision_score=data.get('wardScore', 0)
                        )
                        roaming_events.append(roaming_event)

        return roaming_events

    def _get_zone(self, x: int, y: int) -> str:
        """좌표로부터 맵 존을 파악합니다."""
        for zone, coords in self.LANE_ZONES.items():
            if (coords['x'][0] <= x <= coords['x'][1] and
                    coords['y'][0] <= y <= coords['y'][1]):
                return zone
        return 'unknown'

    def _get_previous_positions(self, frames: List[Dict],
                                 current_idx: int,
                                 participant_id: str,
                                 count: int) -> List[Dict]:
        """이전 포지션들을 가져옵니다."""
        positions = []
        for i in range(max(0, current_idx - count), current_idx):
            frame = frames[i]
            participant = frame.get('participantFrames', {}).get(participant_id, {})
            pos = participant.get('position', {})

            if pos:
                x, y = pos.get('x', 0), pos.get('y', 0)
                positions.append({
                    'x': x,
                    'y': y,
                    'zone': self._get_zone(x, y)
                })

        return positions

    def _is_roaming(self, prev_positions: List[Dict], current_zone: str) -> bool:
        """로밍 여부를 판단합니다."""
        if not prev_positions:
            return False

        # 이전 존과 현재 존이 다르고, 일정 거리 이상 이동한 경우
        prev_zones = [pos['zone'] for pos in prev_positions]

        if len(set(prev_zones)) == 1 and prev_zones[0] != current_zone:
            # 같은 존에 있다가 다른 존으로 이동
            return True

        return False

    def _analyze_positioning(self, frames: List[Dict]) -> Dict:
        """포지셔닝을 분석합니다."""
        positioning_scores = {
            'early_game': [],
            'mid_game': [],
            'late_game': []
        }

        for frame in frames:
            timestamp = frame.get('timestamp', 0) // 1000
            game_phase = self._get_game_phase(timestamp)

            participants = frame.get('participantFrames', {})

            for participant_id, data in participants.items():
                position = data.get('position', {})
                x, y = position.get('x', 0), position.get('y', 0)

                # 안전한 포지셔닝 점수 계산
                safety_score = self._calculate_safety_score(
                    x, y, participants, participant_id
                )

                positioning_scores[game_phase].append(safety_score)

        return {
            phase: np.mean(scores) if scores else 0
            for phase, scores in positioning_scores.items()
        }

    def _get_game_phase(self, timestamp: int) -> str:
        """게임 페이즈를 반환합니다."""
        if timestamp < 900:  # 15분
            return 'early_game'
        elif timestamp < 1800:  # 30분
            return 'mid_game'
        else:
            return 'late_game'

    def _calculate_safety_score(self, x: int, y: int,
                                 participants: Dict,
                                 current_id: str) -> float:
        """
        안전도 점수를 계산합니다.
        아군과의 거리, 적과의 거리, 와드 등을 고려합니다.
        """
        # 간단한 안전도 계산
        # 실제로는 더 복잡한 알고리즘이 필요합니다

        current_pos = participants[current_id].get('position', {})
        current_x, current_y = current_pos.get('x', 0), current_pos.get('y', 0)

        ally_distances = []
        enemy_distances = []

        for pid, data in participants.items():
            if pid == current_id:
                continue

            pos = data.get('position', {})
            px, py = pos.get('x', 0), pos.get('y', 0)

            distance = np.sqrt((current_x - px) ** 2 + (current_y - py) ** 2)

            # 간단하게 ID로 팀 구분 (실제로는 매치 데이터 필요)
            if int(pid) <= 5:
                ally_distances.append(distance)
            else:
                enemy_distances.append(distance)

        # 아군과 가까울수록, 적과 멀수록 안전
        avg_ally_dist = np.mean(ally_distances) if ally_distances else 10000
        avg_enemy_dist = np.mean(enemy_distances) if enemy_distances else 0

        safety_score = (avg_enemy_dist / 1000) - (avg_ally_dist / 2000)

        return max(0, min(10, safety_score))

    def _analyze_cs_patterns(self, frames: List[Dict]) -> Dict:
        """CS 패턴을 분석합니다."""
        cs_data = {
            'per_minute': [],
            'efficiency': []
        }

        for i, frame in enumerate(frames):
            if i == 0:
                continue

            timestamp = frame.get('timestamp', 0) // 60000  # 분 단위

            participants = frame.get('participantFrames', {})

            for participant_id, data in participants.items():
                minions_killed = data.get('minionKills', 0)
                jungle_kills = data.get('jungleMinionsKilled', 0)

                total_cs = minions_killed + jungle_kills

                if timestamp > 0:
                    cs_per_min = total_cs / timestamp
                    cs_data['per_minute'].append(cs_per_min)

                    # 효율성: 이상적인 CS(분당 10개)와 비교
                    efficiency = (cs_per_min / 10) * 100
                    cs_data['efficiency'].append(min(100, efficiency))

        return {
            'avg_cs_per_min': np.mean(cs_data['per_minute']) if cs_data['per_minute'] else 0,
            'avg_efficiency': np.mean(cs_data['efficiency']) if cs_data['efficiency'] else 0
        }

    def _analyze_objectives(self, frames: List[Dict]) -> Dict:
        """오브젝트 관련 분석을 수행합니다."""
        objectives = {
            'dragons': [],
            'barons': [],
            'heralds': [],
            'towers': []
        }

        for frame in frames:
            events = frame.get('events', [])

            for event in events:
                event_type = event.get('type')

                if event_type == 'ELITE_MONSTER_KILL':
                    monster_type = event.get('monsterType')
                    timestamp = event.get('timestamp', 0) // 1000

                    if monster_type == 'DRAGON':
                        objectives['dragons'].append(timestamp)
                    elif monster_type == 'BARON_NASHOR':
                        objectives['barons'].append(timestamp)
                    elif monster_type == 'RIFTHERALD':
                        objectives['heralds'].append(timestamp)

                elif event_type == 'BUILDING_KILL':
                    building_type = event.get('buildingType')
                    if building_type == 'TOWER_BUILDING':
                        timestamp = event.get('timestamp', 0) // 1000
                        objectives['towers'].append(timestamp)

        return objectives

    def get_roaming_recommendations(self, game_state: Dict) -> List[str]:
        """
        현재 게임 상태를 기반으로 로밍 추천을 제공합니다.

        Args:
            game_state: 현재 게임 상태 정보

        Returns:
            로밍 추천 리스트
        """
        recommendations = []

        champion = game_state.get('champion')
        level = game_state.get('level', 1)
        wave_state = game_state.get('wave_state', 'unknown')
        enemy_summs = game_state.get('enemy_summoners', {})
        timestamp = game_state.get('timestamp', 0)

        # 1. 레벨 기반 추천
        if level >= 6:
            recommendations.append("✓ 레벨 6 달성 - 궁극기를 활용한 로밍 타이밍입니다!")

        # 2. 웨이브 상태 기반
        if wave_state == 'push':
            recommendations.append("✓ 웨이브가 푸시됨 - 로밍하기 좋은 타이밍입니다")
        elif wave_state == 'freeze':
            recommendations.append("✗ 웨이브가 프리즈됨 - 로밍보다 CS를 확보하세요")

        # 3. 적 소환사 주문 상태
        if not enemy_summs.get('flash', True):
            recommendations.append("✓ 적 플래시 없음 - 갱킹 성공률이 높습니다!")

        # 4. 시간대 기반
        if 360 <= timestamp <= 420:  # 6-7분
            recommendations.append("✓ 첫 드래곤 타이밍 - 바텀 로밍을 고려하세요")

        # 5. 챔피언 특성 기반
        if champion in ['Ahri', 'Zed', 'Talon', 'Twisted Fate']:
            recommendations.append(f"✓ {champion}는 로밍이 강한 챔피언입니다")

        return recommendations
