"""
Riot Games API 클라이언트
매치 데이터, 챔피언 정보, 리플레이 데이터를 가져옵니다.
"""

import os
import requests
import time
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class RiotAPIClient:
    """Riot Games API와 상호작용하는 클라이언트"""

    BASE_URLS = {
        'kr': 'https://kr.api.riotgames.com',
        'asia': 'https://asia.api.riotgames.com'
    }

    def __init__(self, api_key: Optional[str] = None, region: str = 'kr'):
        """
        Args:
            api_key: Riot API 키 (없으면 환경변수에서 가져옴)
            region: 지역 (기본값: kr)
        """
        self.api_key = api_key or os.getenv('RIOT_API_KEY')
        self.region = region
        self.base_url = self.BASE_URLS.get(region, self.BASE_URLS['kr'])
        self.headers = {'X-Riot-Token': self.api_key}
        self.rate_limit_delay = 1.2  # API 제한을 피하기 위한 딜레이

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """API 요청을 수행합니다."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 실패: {e}")
            return {}

    def get_summoner_by_name(self, summoner_name: str) -> Dict:
        """소환사 이름으로 소환사 정보를 가져옵니다."""
        endpoint = f"/lol/summoner/v4/summoners/by-name/{summoner_name}"
        return self._make_request(endpoint)

    def get_summoner_by_puuid(self, puuid: str) -> Dict:
        """PUUID로 소환사 정보를 가져옵니다."""
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return self._make_request(endpoint)

    def get_challenger_players(self, queue: str = 'RANKED_SOLO_5x5') -> Dict:
        """챌린저 플레이어 목록을 가져옵니다."""
        endpoint = f"/lol/league/v4/challengerleagues/by-queue/{queue}"
        return self._make_request(endpoint)

    def get_match_history(self, puuid: str, count: int = 20) -> List[str]:
        """플레이어의 최근 매치 ID 목록을 가져옵니다."""
        # 아시아 서버 사용
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {'count': count}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"매치 히스토리 가져오기 실패: {e}")
            return []

    def get_match_details(self, match_id: str) -> Dict:
        """매치의 상세 정보를 가져옵니다."""
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"매치 상세정보 가져오기 실패: {e}")
            return {}

    def get_match_timeline(self, match_id: str) -> Dict:
        """매치의 타임라인 데이터를 가져옵니다 (로밍, 포지셔닝 분석용)."""
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"매치 타임라인 가져오기 실패: {e}")
            return {}
