"""
챔피언 데이터 테스트
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.champion_data import ChampionDatabase, ItemDatabase


def test_champion_database():
    """챔피언 데이터베이스 테스트"""
    print("=" * 60)
    print("챔피언 데이터베이스 테스트")
    print("=" * 60)

    db = ChampionDatabase()

    # 챔피언 가져오기
    print("\n1. 챔피언 정보 가져오기")
    ahri = db.get_champion("Ahri")
    print(f"✓ {ahri['name']} - {ahri['title']}")
    print(f"  로밍 점수: {ahri['roaming_score']}/10")

    # 스킬 정보
    print("\n2. 스킬 정보")
    skills = db.get_champion_skills("Zed")
    for key, skill in skills.items():
        print(f"  [{key}] {skill['name']}")

    # 상성 정보
    print("\n3. 상성 정보")
    matchup = db.get_matchup_info("Ahri", "Zed")
    print(f"  아리 vs 제드: {matchup}")

    # 로밍 강한 챔피언
    print("\n4. 로밍 강한 챔피언 TOP 3")
    roaming_champs = db.get_roaming_champions()
    for i, champ in enumerate(roaming_champs[:3], 1):
        print(f"  {i}. {champ['name']} - 점수: {champ['score']}/10")

    # 파워 스파이크
    print("\n5. 파워 스파이크")
    spikes = db.get_champion_power_spikes("Lee Sin")
    print(f"  리 신: 레벨 {', '.join(map(str, spikes))}")

    print("\n✓ 모든 테스트 통과!")


def test_item_database():
    """아이템 데이터베이스 테스트"""
    print("\n" + "=" * 60)
    print("아이템 데이터베이스 테스트")
    print("=" * 60)

    db = ItemDatabase()

    # 아이템 가져오기
    print("\n1. 아이템 정보")
    item = db.get_item("루덴의 메아리")
    print(f"✓ 루덴의 메아리")
    print(f"  가격: {item['cost']}G")
    print(f"  주문력: {item['stats']['ap']}")

    # 아이템 효율
    print("\n2. 아이템 효율")
    efficiency = db.get_item_efficiency("루덴의 메아리", "AP")
    print(f"  AP 챔피언 효율: {efficiency:.2f}")

    print("\n✓ 모든 테스트 통과!")


if __name__ == '__main__':
    test_champion_database()
    test_item_database()
    print("\n" + "=" * 60)
    print("✓ 모든 테스트 완료!")
    print("=" * 60)
