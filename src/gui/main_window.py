"""
LOL AI Assistant - 메인 GUI 윈도우
PyQt5 기반 데스크톱 애플리케이션
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTabWidget,
    QComboBox, QGroupBox, QTableWidget, QTableWidgetItem,
    QProgressBar, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from typing import Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.riot_client import RiotAPIClient
from data.champion_data import ChampionDatabase, ItemDatabase
from analysis.replay_analyzer import ReplayAnalyzer
from ai.decision_engine import DecisionEngine


class AnalysisThread(QThread):
    """백그라운드 분석 스레드"""
    progress = pyqtSignal(int)
    result = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, api_client, analyzer, summoner_name):
        super().__init__()
        self.api_client = api_client
        self.analyzer = analyzer
        self.summoner_name = summoner_name

    def run(self):
        """분석 실행"""
        try:
            # 1. 소환사 정보 가져오기
            self.progress.emit(10)
            summoner = self.api_client.get_summoner_by_name(self.summoner_name)

            if not summoner:
                self.error.emit("소환사를 찾을 수 없습니다")
                return

            # 2. 매치 히스토리 가져오기
            self.progress.emit(30)
            puuid = summoner.get('puuid')
            match_ids = self.api_client.get_match_history(puuid, count=5)

            if not match_ids:
                self.error.emit("매치 히스토리를 가져올 수 없습니다")
                return

            # 3. 매치 분석
            all_analysis = []
            for i, match_id in enumerate(match_ids):
                self.progress.emit(40 + (i * 10))

                match_details = self.api_client.get_match_details(match_id)
                timeline = self.api_client.get_match_timeline(match_id)

                if timeline:
                    analysis = self.analyzer.analyze_match_timeline(timeline)
                    all_analysis.append(analysis)

            self.progress.emit(100)
            self.result.emit({
                'summoner': summoner,
                'match_count': len(match_ids),
                'analysis': all_analysis
            })

        except Exception as e:
            self.error.emit(f"분석 중 오류: {str(e)}")


class LOLAIAssistant(QMainWindow):
    """LOL AI Assistant 메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.api_client = RiotAPIClient()
        self.champion_db = ChampionDatabase()
        self.item_db = ItemDatabase()
        self.analyzer = ReplayAnalyzer()
        self.decision_engine = DecisionEngine()

        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("LOL AI Assistant - 챌린저급 AI 분석 시스템")
        self.setGeometry(100, 100, 1400, 900)

        # 다크 테마 적용
        self.set_dark_theme()

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 제목
        title = QLabel("🎮 LOL AI Assistant - 챌린저급 분석 시스템")
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 탭 위젯
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # 각 탭 생성
        self.create_analysis_tab()
        self.create_champion_tab()
        self.create_realtime_tab()
        self.create_settings_tab()

        # 상태바
        self.statusBar().showMessage('준비됨')

    def set_dark_theme(self):
        """다크 테마 설정"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        QApplication.setPalette(dark_palette)

    def create_analysis_tab(self):
        """리플레이 분석 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 소환사 검색 그룹
        search_group = QGroupBox("📊 소환사 분석")
        search_layout = QHBoxLayout()
        search_group.setLayout(search_layout)

        self.summoner_input = QLineEdit()
        self.summoner_input.setPlaceholderText("소환사명을 입력하세요...")
        self.summoner_input.setFont(QFont('Arial', 12))
        search_layout.addWidget(QLabel("소환사명:"))
        search_layout.addWidget(self.summoner_input)

        self.analyze_btn = QPushButton("🔍 분석 시작")
        self.analyze_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.analyze_btn.clicked.connect(self.analyze_summoner)
        search_layout.addWidget(self.analyze_btn)

        layout.addWidget(search_group)

        # 진행바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 결과 표시 영역
        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        self.analysis_result.setFont(QFont('Consolas', 11))
        layout.addWidget(self.analysis_result)

        self.tabs.addTab(tab, "리플레이 분석")

    def create_champion_tab(self):
        """챔피언 정보 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 챔피언 선택
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("챔피언 선택:"))

        self.champion_combo = QComboBox()
        self.champion_combo.addItems(self.champion_db.champions.keys())
        self.champion_combo.currentTextChanged.connect(self.show_champion_info)
        select_layout.addWidget(self.champion_combo)

        layout.addLayout(select_layout)

        # 챔피언 정보 표시
        self.champion_info = QTextEdit()
        self.champion_info.setReadOnly(True)
        self.champion_info.setFont(QFont('Consolas', 11))
        layout.addWidget(self.champion_info)

        # 로밍 강한 챔피언 표시
        roaming_group = QGroupBox("🚀 로밍에 강한 챔피언")
        roaming_layout = QVBoxLayout()
        roaming_group.setLayout(roaming_layout)

        roaming_champs = self.champion_db.get_roaming_champions()
        roaming_text = "\n".join([
            f"{i+1}. {champ['name']} - 로밍 점수: {champ['score']}/10"
            for i, champ in enumerate(roaming_champs)
        ])

        roaming_label = QLabel(roaming_text)
        roaming_label.setFont(QFont('Arial', 11))
        roaming_layout.addWidget(roaming_label)

        layout.addWidget(roaming_group)

        self.tabs.addTab(tab, "챔피언 정보")

        # 초기 챔피언 정보 표시
        if self.champion_combo.count() > 0:
            self.show_champion_info(self.champion_combo.currentText())

    def create_realtime_tab(self):
        """실시간 조언 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 게임 상태 입력
        state_group = QGroupBox("⚡ 게임 상태 입력")
        state_layout = QVBoxLayout()
        state_group.setLayout(state_layout)

        # 챔피언 선택
        champ_layout = QHBoxLayout()
        champ_layout.addWidget(QLabel("내 챔피언:"))
        self.my_champion = QComboBox()
        self.my_champion.addItems(self.champion_db.champions.keys())
        champ_layout.addWidget(self.my_champion)
        state_layout.addLayout(champ_layout)

        # 게임 시간
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("게임 시간 (분):"))
        self.game_time = QLineEdit()
        self.game_time.setPlaceholderText("예: 10")
        time_layout.addWidget(self.game_time)
        state_layout.addLayout(time_layout)

        # 레벨
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("내 레벨:"))
        self.my_level = QLineEdit()
        self.my_level.setPlaceholderText("예: 6")
        level_layout.addWidget(self.my_level)
        state_layout.addLayout(level_layout)

        # 분석 버튼
        advice_btn = QPushButton("🎯 실시간 조언 받기")
        advice_btn.setFont(QFont('Arial', 12, QFont.Bold))
        advice_btn.clicked.connect(self.get_realtime_advice)
        state_layout.addWidget(advice_btn)

        layout.addWidget(state_group)

        # 조언 표시
        self.advice_display = QTextEdit()
        self.advice_display.setReadOnly(True)
        self.advice_display.setFont(QFont('Consolas', 11))
        layout.addWidget(self.advice_display)

        self.tabs.addTab(tab, "실시간 조언")

    def create_settings_tab(self):
        """설정 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        settings_group = QGroupBox("⚙️ 설정")
        settings_layout = QVBoxLayout()
        settings_group.setLayout(settings_layout)

        # API 키 설정
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("Riot API 키:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("API 키를 입력하세요...")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.api_key_input)
        settings_layout.addLayout(api_layout)

        # 저장 버튼
        save_btn = QPushButton("💾 설정 저장")
        save_btn.clicked.connect(self.save_settings)
        settings_layout.addWidget(save_btn)

        layout.addWidget(settings_group)

        # 정보
        info_text = """
        <h2>📖 사용 방법</h2>
        <p><b>1. 리플레이 분석:</b> 소환사명을 입력하여 최근 게임을 분석합니다.</p>
        <p><b>2. 챔피언 정보:</b> 각 챔피언의 스킬, 상성, 파워스파이크를 확인합니다.</p>
        <p><b>3. 실시간 조언:</b> 현재 게임 상황에 맞는 최적의 행동을 추천받습니다.</p>
        <p><b>4. 로밍 AI:</b> 언제 로밍해야 하는지 AI가 분석합니다.</p>

        <h2>🔑 API 키 발급</h2>
        <p>1. <a href="https://developer.riotgames.com/">Riot Developer Portal</a> 방문</p>
        <p>2. 로그인 후 API 키 발급</p>
        <p>3. 발급받은 키를 위 설정에 입력</p>

        <h2>ℹ️ 주요 기능</h2>
        <ul>
            <li>✓ 챌린저 리플레이 분석</li>
            <li>✓ 로밍 타이밍 AI 추천</li>
            <li>✓ 맵 인식 및 포지셔닝 분석</li>
            <li>✓ CS 패턴 분석</li>
            <li>✓ 챔피언 상성 정보</li>
            <li>✓ 실시간 전략 조언</li>
        </ul>
        """

        info_display = QTextEdit()
        info_display.setReadOnly(True)
        info_display.setHtml(info_text)
        layout.addWidget(info_display)

        self.tabs.addTab(tab, "설정 및 정보")

    def analyze_summoner(self):
        """소환사 분석 시작"""
        summoner_name = self.summoner_input.text().strip()

        if not summoner_name:
            QMessageBox.warning(self, "입력 오류", "소환사명을 입력하세요!")
            return

        # 진행바 표시
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.analyze_btn.setEnabled(False)
        self.statusBar().showMessage('분석 중...')

        # 백그라운드 스레드에서 분석
        self.analysis_thread = AnalysisThread(
            self.api_client, self.analyzer, summoner_name
        )
        self.analysis_thread.progress.connect(self.progress_bar.setValue)
        self.analysis_thread.result.connect(self.show_analysis_result)
        self.analysis_thread.error.connect(self.show_error)
        self.analysis_thread.start()

    def show_analysis_result(self, result):
        """분석 결과 표시"""
        summoner = result['summoner']
        analysis = result['analysis']

        output = f"""
╔══════════════════════════════════════════════════════════════╗
║  📊 소환사 분석 결과
╚══════════════════════════════════════════════════════════════╝

소환사: {summoner.get('name', 'Unknown')}
레벨: {summoner.get('summonerLevel', 'N/A')}
분석한 게임 수: {result['match_count']}

{'─' * 60}
"""

        # 각 게임 분석 결과
        for i, match_analysis in enumerate(analysis):
            output += f"\n📋 게임 #{i+1} 분석\n"

            if 'roaming' in match_analysis:
                roaming = match_analysis['roaming']
                output += f"  로밍 이벤트: {len(roaming)}회\n"

            if 'positioning' in match_analysis:
                pos = match_analysis['positioning']
                output += f"  포지셔닝 점수:\n"
                output += f"    - 초반: {pos.get('early_game', 0):.2f}/10\n"
                output += f"    - 중반: {pos.get('mid_game', 0):.2f}/10\n"
                output += f"    - 후반: {pos.get('late_game', 0):.2f}/10\n"

            if 'cs_patterns' in match_analysis:
                cs = match_analysis['cs_patterns']
                output += f"  CS 효율:\n"
                output += f"    - 분당 CS: {cs.get('avg_cs_per_min', 0):.2f}\n"
                output += f"    - 효율성: {cs.get('avg_efficiency', 0):.2f}%\n"

            output += f"\n{'─' * 60}\n"

        # 종합 추천
        output += "\n\n💡 개선 포인트:\n"
        output += "  1. 로밍 타이밍을 더 활용하세요\n"
        output += "  2. 초반 CS 확보에 집중하세요\n"
        output += "  3. 맵 인식을 통한 안전한 포지셔닝\n"
        output += "  4. 오브젝트 타이밍에 맞춰 움직이세요\n"

        self.analysis_result.setText(output)
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.statusBar().showMessage('분석 완료!')

    def show_error(self, error_msg):
        """에러 표시"""
        QMessageBox.critical(self, "오류", error_msg)
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.statusBar().showMessage('오류 발생')

    def show_champion_info(self, champion_name):
        """챔피언 정보 표시"""
        champion = self.champion_db.get_champion(champion_name)

        if not champion:
            return

        output = f"""
╔══════════════════════════════════════════════════════════════╗
║  ⚔️ {champion['name']} - {champion['title']}
╚══════════════════════════════════════════════════════════════╝

포지션: {', '.join(champion['roles'])}
난이도: {champion['difficulty']}/10

📈 능력치:
  로밍 점수: {champion.get('roaming_score', 0)}/10
  웨이브 클리어: {champion.get('wave_clear', 0)}/10
  폭딜: {champion.get('burst_damage', 0)}/10
  기동성: {champion.get('mobility', 0)}/10
  CC: {champion.get('cc_score', 0)}/10

{'─' * 60}

🎯 스킬 정보:
"""

        for key, skill in champion['skills'].items():
            output += f"\n[{key}] {skill['name']}\n"
            output += f"  - {skill['description']}\n"
            if 'cooldown' in skill:
                output += f"  - 쿨다운: {skill['cooldown']}\n"

        output += f"\n{'─' * 60}\n"
        output += f"\n⚡ 파워 스파이크 레벨: {', '.join(map(str, champion.get('power_spikes', [])))}\n"
        output += f"\n🛡️ 코어 아이템:\n"
        for item in champion.get('core_items', []):
            output += f"  • {item}\n"

        # 상성 정보
        matchup = self.champion_db.matchups.get(champion_name, {})
        if matchup:
            output += f"\n{'─' * 60}\n"
            output += "\n🎭 챔피언 상성:\n"
            output += f"\n  ✓ 유리한 상대:\n"
            for enemy in matchup.get('strong_against', []):
                output += f"    • {enemy}\n"

            output += f"\n  ✗ 불리한 상대:\n"
            for enemy in matchup.get('weak_against', []):
                output += f"    • {enemy}\n"

        self.champion_info.setText(output)

    def get_realtime_advice(self):
        """실시간 조언 제공"""
        try:
            champion = self.my_champion.currentText()
            game_time = int(self.game_time.text() or 0) * 60  # 분 -> 초
            level = int(self.my_level.text() or 1)

            # 간단한 게임 상태 생성
            game_state = {
                'timestamp': game_time,
                'player': {
                    'champion': champion,
                    'level': level,
                    'cs': level * 10,  # 가정
                    'position': {'x': 7000, 'y': 7000},
                    'vision_score': game_time // 60,
                    'health': 80,
                    'max_health': 100,
                    'items': []
                },
                'allies': [],
                'enemies': [],
                'lane_enemy': {
                    'level': level,
                    'health': 70,
                    'max_health': 100,
                    'items': []
                },
                'objectives': {
                    'dragon_alive': True,
                    'baron_alive': game_time >= 1200,
                    'herald_alive': game_time <= 840
                }
            }

            # AI 분석
            analysis = self.decision_engine.analyze_game_state(game_state)

            # 로밍 추천
            roaming_recs = self.analyzer.get_roaming_recommendations({
                'champion': champion,
                'level': level,
                'wave_state': 'push',
                'enemy_summoners': {},
                'timestamp': game_time
            })

            # 결과 표시
            output = f"""
╔══════════════════════════════════════════════════════════════╗
║  🎯 실시간 AI 조언
╚══════════════════════════════════════════════════════════════╝

챔피언: {champion}
게임 시간: {game_time // 60}분
레벨: {level}
게임 페이즈: {analysis['phase']}

{'─' * 60}

📊 현재 상태 분석:

웨이브 상태:
  {analysis['wave_state']['recommendation']}

맵 포지션:
  {analysis['map_position']['recommendation']}

파워 레벨:
  {analysis['power_level']['recommendation']}

시야 점수:
  {analysis['vision_score']['recommendation']}

{'─' * 60}

🎯 추천 행동 (우선순위순):
"""

            for i, action in enumerate(analysis['recommended_actions'], 1):
                output += f"\n{i}. [{action['action'].upper()}] (우선순위: {action['priority']}/10)\n"
                output += f"   → {action['reason']}\n"

            output += f"\n{'─' * 60}\n"
            output += "\n🚀 로밍 분석:\n"
            for rec in roaming_recs:
                output += f"  {rec}\n"

            # 오브젝트 우선순위
            if analysis['objective_priority']['priorities']:
                output += f"\n{'─' * 60}\n"
                output += "\n🐉 오브젝트 우선순위:\n"
                for obj in analysis['objective_priority']['priorities']:
                    output += f"  • {obj['type'].upper()} - 우선순위: {obj['priority']}/10\n"
                    output += f"    → {obj['recommendation']}\n"

            self.advice_display.setText(output)
            self.statusBar().showMessage('실시간 조언 생성 완료!')

        except ValueError:
            QMessageBox.warning(self, "입력 오류", "게임 시간과 레벨은 숫자로 입력하세요!")

    def save_settings(self):
        """설정 저장"""
        api_key = self.api_key_input.text().strip()

        if api_key:
            # .env 파일에 저장
            try:
                with open('.env', 'w') as f:
                    f.write(f"RIOT_API_KEY={api_key}\n")
                    f.write("RIOT_REGION=kr\n")

                QMessageBox.information(self, "성공", "설정이 저장되었습니다!")
                self.api_client = RiotAPIClient(api_key=api_key)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"설정 저장 실패: {str(e)}")
        else:
            QMessageBox.warning(self, "입력 오류", "API 키를 입력하세요!")


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 모던한 스타일

    window = LOLAIAssistant()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
