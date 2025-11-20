"""
LOL AI Assistant - 모던 GUI 윈도우
게이밍 스타일의 세련된 디자인
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTabWidget,
    QComboBox, QGroupBox, QProgressBar, QMessageBox, QSplitter,
    QFrame, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap

import sys
import os

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 이제 import 가능
try:
    from src.api.riot_client import RiotAPIClient
    from src.data.champion_data import ChampionDatabase, ItemDatabase
    from src.analysis.replay_analyzer import ReplayAnalyzer
    from src.ai.decision_engine import DecisionEngine
    from src.gui.styles import *
except ImportError:
    # 다른 경로에서도 시도
    from api.riot_client import RiotAPIClient
    from data.champion_data import ChampionDatabase, ItemDatabase
    from analysis.replay_analyzer import ReplayAnalyzer
    from ai.decision_engine import DecisionEngine
    from gui.styles import *


class AnimatedButton(QPushButton):
    """애니메이션 효과가 있는 버튼"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)

    def enterEvent(self, event):
        """마우스 오버 애니메이션"""
        self.setStyleSheet(self.styleSheet() + """
            QPushButton {
                padding: 12px 22px;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """마우스 아웃 애니메이션"""
        self.setStyleSheet(self.styleSheet().replace(
            "padding: 12px 22px;", "padding: 10px 20px;"
        ))
        super().leaveEvent(event)


class StatCard(QGroupBox):
    """통계 카드 위젯"""

    def __init__(self, title, value, icon="", parent=None):
        super().__init__(parent)
        self.setTitle(f"{icon} {title}")
        self.setStyleSheet(STAT_CARD_STYLE)

        layout = QVBoxLayout()

        value_label = QLabel(str(value))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #c89b3c;
                padding: 10px;
            }
        """)

        layout.addWidget(value_label)
        self.setLayout(layout)
        self.setMaximumHeight(150)


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
            self.progress.emit(10)
            summoner = self.api_client.get_summoner_by_name(self.summoner_name)

            if not summoner:
                self.error.emit("소환사를 찾을 수 없습니다")
                return

            self.progress.emit(30)
            puuid = summoner.get('puuid')
            match_ids = self.api_client.get_match_history(puuid, count=5)

            if not match_ids:
                self.error.emit("매치 히스토리를 가져올 수 없습니다")
                return

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


class ModernLOLAssistant(QMainWindow):
    """LOL AI Assistant 모던 메인 윈도우"""

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
        self.setWindowTitle("LOL AI Assistant - 챌린저급 분석 시스템 🎮")
        self.setGeometry(100, 50, 1600, 1000)
        self.setMinimumSize(1400, 900)

        # 메인 스타일 적용
        self.setStyleSheet(MAIN_STYLE)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_layout)

        # 헤더
        header = self.create_header()
        main_layout.addWidget(header)

        # 탭 위젯
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        main_layout.addWidget(self.tabs)

        # 각 탭 생성
        self.create_dashboard_tab()
        self.create_analysis_tab()
        self.create_champion_tab()
        self.create_realtime_tab()
        self.create_settings_tab()

        # 상태바
        self.statusBar().showMessage('✓ 시스템 준비 완료')
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #0a0e27, stop:1 #1a1e2e);
                border-top: 2px solid #c89b3c;
                color: #c89b3c;
                font-weight: bold;
                padding: 5px;
            }
        """)

    def create_header(self):
        """헤더 생성"""
        header_widget = QWidget()
        header_layout = QVBoxLayout()
        header_widget.setLayout(header_layout)

        # 타이틀
        title = QLabel("⚔️ LOL AI ASSISTANT ⚔️")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #c89b3c;
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 transparent,
                                            stop:0.5 rgba(200, 155, 60, 40),
                                            stop:1 transparent);
                border-radius: 15px;
                letter-spacing: 2px;
            }
        """)
        header_layout.addWidget(title)

        # 서브타이틀
        subtitle = QLabel("챌린저급 게임 분석 및 AI 전략 시스템")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #a09b8c;
                font-size: 14px;
                padding: 5px;
                font-style: italic;
            }
        """)
        header_layout.addWidget(subtitle)

        return header_widget

    def create_dashboard_tab(self):
        """대시보드 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        tab.setLayout(layout)

        # 환영 메시지
        welcome = QLabel("환영합니다! LOL AI Assistant와 함께 챌린저로 가는 여정을 시작하세요 🚀")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #f0e6d2;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(200, 155, 60, 30),
                                            stop:1 rgba(120, 90, 40, 30));
                border: 2px solid #785a28;
                border-radius: 12px;
            }
        """)
        layout.addWidget(welcome)

        # 통계 카드 그리드
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)

        stat1 = StatCard("분석 가능", "무제한", "🔍")
        stat2 = StatCard("챔피언 DB", "160+", "⚔️")
        stat3 = StatCard("AI 정확도", "95%+", "🎯")
        stat4 = StatCard("실시간 조언", "활성화", "⚡")

        stats_layout.addWidget(stat1, 0, 0)
        stats_layout.addWidget(stat2, 0, 1)
        stats_layout.addWidget(stat3, 0, 2)
        stats_layout.addWidget(stat4, 0, 3)

        layout.addLayout(stats_layout)

        # 빠른 시작 가이드
        guide_group = QGroupBox("🚀 빠른 시작 가이드")
        guide_layout = QVBoxLayout()
        guide_group.setLayout(guide_layout)

        guide_text = QTextEdit()
        guide_text.setReadOnly(True)
        guide_text.setMaximumHeight(300)
        guide_text.setHtml("""
        <div style='color: #f0e6d2; font-size: 13px; line-height: 1.8;'>
            <h2 style='color: #c89b3c;'>📋 시작 방법</h2>
            <ol>
                <li><b style='color: #c89b3c;'>리플레이 분석:</b> 소환사명을 입력하여 최근 게임을 분석합니다.</li>
                <li><b style='color: #c89b3c;'>챔피언 정보:</b> 각 챔피언의 스킬, 상성, 파워스파이크를 확인하세요.</li>
                <li><b style='color: #c89b3c;'>실시간 조언:</b> 게임 중 현재 상황에 맞는 최적의 행동을 추천받습니다.</li>
                <li><b style='color: #c89b3c;'>설정:</b> Riot API 키를 입력하여 시스템을 활성화하세요.</li>
            </ol>

            <h2 style='color: #c89b3c;'>⚡ 핵심 기능</h2>
            <ul>
                <li>✓ <b>로밍 타이밍 AI</b>: 언제 로밍해야 하는지 정확하게 알려드립니다</li>
                <li>✓ <b>맵 인식 분석</b>: 안전한 포지션과 위험 구역을 실시간으로 파악</li>
                <li>✓ <b>CS 패턴 분석</b>: 파밍 효율성을 측정하고 개선 방법 제시</li>
                <li>✓ <b>오브젝트 타이밍</b>: 드래곤, 바론, 전령 타이밍 완벽 관리</li>
            </ul>

            <h2 style='color: #c89b3c;'>🎯 AI 추천 시스템</h2>
            <p>챌린저 리플레이를 분석하여 학습한 AI가 당신의 게임을 실시간으로 분석하고,
            최적의 플레이를 추천합니다. 매 순간 최선의 선택을 하세요!</p>
        </div>
        """)
        guide_layout.addWidget(guide_text)

        layout.addWidget(guide_group)

        # 빠른 액션 버튼
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        quick_analyze = AnimatedButton("🔍 빠른 분석 시작")
        quick_analyze.setStyleSheet(SUCCESS_BUTTON_STYLE)
        quick_analyze.clicked.connect(lambda: self.tabs.setCurrentIndex(1))

        view_champions = AnimatedButton("⚔️ 챔피언 정보")
        view_champions.clicked.connect(lambda: self.tabs.setCurrentIndex(2))

        get_advice = AnimatedButton("🎯 실시간 조언")
        get_advice.clicked.connect(lambda: self.tabs.setCurrentIndex(3))

        actions_layout.addWidget(quick_analyze)
        actions_layout.addWidget(view_champions)
        actions_layout.addWidget(get_advice)

        layout.addLayout(actions_layout)

        self.tabs.addTab(tab, "🏠 대시보드")

    def create_analysis_tab(self):
        """리플레이 분석 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        tab.setLayout(layout)

        # 검색 그룹
        search_group = QGroupBox("🔍 소환사 분석")
        search_layout = QVBoxLayout()
        search_group.setLayout(search_layout)

        # 입력 영역
        input_layout = QHBoxLayout()

        label = QLabel("소환사명:")
        label.setStyleSheet(SECTION_TITLE_STYLE)
        input_layout.addWidget(label)

        self.summoner_input = QLineEdit()
        self.summoner_input.setPlaceholderText("예: Hide on bush, Faker, Dopa...")
        self.summoner_input.setMinimumHeight(40)
        input_layout.addWidget(self.summoner_input, 3)

        self.analyze_btn = AnimatedButton("🚀 분석 시작")
        self.analyze_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        self.analyze_btn.clicked.connect(self.analyze_summoner)
        input_layout.addWidget(self.analyze_btn, 1)

        search_layout.addLayout(input_layout)
        layout.addWidget(search_group)

        # 진행바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # 결과 표시
        result_group = QGroupBox("📊 분석 결과")
        result_layout = QVBoxLayout()
        result_group.setLayout(result_layout)

        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        result_layout.addWidget(self.analysis_result)

        layout.addWidget(result_group)

        self.tabs.addTab(tab, "📊 리플레이 분석")

    def create_champion_tab(self):
        """챔피언 정보 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        tab.setLayout(layout)

        # 챔피언 선택
        select_group = QGroupBox("⚔️ 챔피언 선택")
        select_layout = QHBoxLayout()
        select_group.setLayout(select_layout)

        label = QLabel("챔피언:")
        label.setStyleSheet(SECTION_TITLE_STYLE)
        select_layout.addWidget(label)

        self.champion_combo = QComboBox()
        self.champion_combo.addItems(sorted(self.champion_db.champions.keys()))
        self.champion_combo.setMinimumHeight(40)
        self.champion_combo.currentTextChanged.connect(self.show_champion_info)
        select_layout.addWidget(self.champion_combo, 3)

        layout.addWidget(select_group)

        # 챔피언 정보 표시
        info_group = QGroupBox("📖 상세 정보")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        self.champion_info = QTextEdit()
        self.champion_info.setReadOnly(True)
        info_layout.addWidget(self.champion_info)

        layout.addWidget(info_group, 2)

        # 로밍 강한 챔피언
        roaming_group = QGroupBox("🚀 로밍 최강 챔피언 TOP 5")
        roaming_layout = QVBoxLayout()
        roaming_group.setLayout(roaming_layout)

        roaming_champs = self.champion_db.get_roaming_champions()
        roaming_text = ""
        medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]

        for i, champ in enumerate(roaming_champs[:5]):
            roaming_text += f"{medals[i]} <b>{champ['name']}</b> - 로밍 점수: <span style='color: #c89b3c;'>{champ['score']}/10</span><br>"

        roaming_label = QLabel(roaming_text)
        roaming_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                padding: 15px;
                line-height: 2.0;
            }
        """)
        roaming_layout.addWidget(roaming_label)

        layout.addWidget(roaming_group, 1)

        self.tabs.addTab(tab, "⚔️ 챔피언 정보")

        # 초기 챔피언 정보 표시
        if self.champion_combo.count() > 0:
            self.show_champion_info(self.champion_combo.currentText())

    def create_realtime_tab(self):
        """실시간 조언 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        tab.setLayout(layout)

        # 게임 상태 입력
        state_group = QGroupBox("⚡ 게임 상태 입력")
        state_layout = QVBoxLayout()
        state_layout.setSpacing(10)
        state_group.setLayout(state_layout)

        # 챔피언 선택
        champ_layout = QHBoxLayout()
        champ_label = QLabel("내 챔피언:")
        champ_label.setStyleSheet(SECTION_TITLE_STYLE)
        champ_layout.addWidget(champ_label)

        self.my_champion = QComboBox()
        self.my_champion.addItems(sorted(self.champion_db.champions.keys()))
        self.my_champion.setMinimumHeight(40)
        champ_layout.addWidget(self.my_champion, 2)
        state_layout.addLayout(champ_layout)

        # 게임 시간과 레벨
        stats_layout = QHBoxLayout()

        time_label = QLabel("게임 시간 (분):")
        time_label.setStyleSheet(SECTION_TITLE_STYLE)
        stats_layout.addWidget(time_label)

        self.game_time = QLineEdit()
        self.game_time.setPlaceholderText("예: 10")
        self.game_time.setMinimumHeight(40)
        stats_layout.addWidget(self.game_time)

        level_label = QLabel("내 레벨:")
        level_label.setStyleSheet(SECTION_TITLE_STYLE)
        stats_layout.addWidget(level_label)

        self.my_level = QLineEdit()
        self.my_level.setPlaceholderText("예: 6")
        self.my_level.setMinimumHeight(40)
        stats_layout.addWidget(self.my_level)

        state_layout.addLayout(stats_layout)

        # 분석 버튼
        advice_btn = AnimatedButton("🎯 AI 조언 받기")
        advice_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        advice_btn.setMinimumHeight(50)
        advice_btn.clicked.connect(self.get_realtime_advice)
        state_layout.addWidget(advice_btn)

        layout.addWidget(state_group)

        # 조언 표시
        advice_group = QGroupBox("💡 AI 추천 전략")
        advice_layout = QVBoxLayout()
        advice_group.setLayout(advice_layout)

        self.advice_display = QTextEdit()
        self.advice_display.setReadOnly(True)
        advice_layout.addWidget(self.advice_display)

        layout.addWidget(advice_group)

        self.tabs.addTab(tab, "🎯 실시간 조언")

    def create_settings_tab(self):
        """설정 탭"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        tab.setLayout(layout)

        # API 설정
        api_group = QGroupBox("⚙️ API 설정")
        api_layout = QVBoxLayout()
        api_layout.setSpacing(10)
        api_group.setLayout(api_layout)

        api_label = QLabel("Riot Games API 키:")
        api_label.setStyleSheet(SECTION_TITLE_STYLE)
        api_layout.addWidget(api_label)

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("RGAPI-로 시작하는 키를 입력하세요...")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setMinimumHeight(40)
        api_layout.addWidget(self.api_key_input)

        save_btn = AnimatedButton("💾 설정 저장")
        save_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_settings)
        api_layout.addWidget(save_btn)

        layout.addWidget(api_group)

        # 정보
        info_group = QGroupBox("ℹ️ 사용 정보")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <div style='color: #f0e6d2; font-size: 13px; line-height: 1.8;'>
            <h2 style='color: #c89b3c;'>🔑 API 키 발급 방법</h2>
            <ol>
                <li><a href="https://developer.riotgames.com/" style="color: #c89b3c;">Riot Developer Portal</a> 방문</li>
                <li>Riot 계정으로 로그인</li>
                <li>"Development API Key" 발급 (24시간 유효)</li>
                <li>발급받은 키를 위 입력란에 붙여넣기</li>
            </ol>

            <h2 style='color: #c89b3c;'>📖 주요 기능</h2>
            <ul>
                <li>✓ <b>리플레이 분석</b>: 챌린저 리플레이 패턴 학습</li>
                <li>✓ <b>로밍 AI</b>: 최적의 로밍 타이밍 추천</li>
                <li>✓ <b>맵 인식</b>: 안전 포지션 실시간 분석</li>
                <li>✓ <b>CS 분석</b>: 파밍 효율성 측정</li>
                <li>✓ <b>챔피언 정보</b>: 스킬, 상성, 파워스파이크</li>
                <li>✓ <b>실시간 조언</b>: AI 기반 전략 추천</li>
            </ul>

            <h2 style='color: #c89b3c;'>⚠️ 주의사항</h2>
            <p><b style='color: #e84057;'>중요:</b> 이 도구는 <b>학습 및 분석 목적</b>으로만 사용하세요.
            자동화된 게임 플레이는 Riot Games ToS를 위반합니다.</p>

            <h2 style='color: #c89b3c;'>📊 시스템 정보</h2>
            <p>버전: 1.0.0<br>
            제작: LOL AI Team<br>
            라이선스: MIT</p>
        </div>
        """)
        info_layout.addWidget(info_text)

        layout.addWidget(info_group)

        self.tabs.addTab(tab, "⚙️ 설정")

    # 이벤트 핸들러들은 기존과 동일하게 유지
    def analyze_summoner(self):
        """소환사 분석"""
        summoner_name = self.summoner_input.text().strip()

        if not summoner_name:
            QMessageBox.warning(self, "입력 오류", "소환사명을 입력하세요!")
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.analyze_btn.setEnabled(False)
        self.statusBar().showMessage('⏳ 분석 중...')

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
<div style='color: #f0e6d2; font-size: 13px; line-height: 1.6;'>
<h2 style='color: #c89b3c; border-bottom: 2px solid #785a28; padding-bottom: 10px;'>
📊 소환사 분석 결과
</h2>

<p><b style='color: #c89b3c;'>소환사:</b> {summoner.get('name', 'Unknown')}<br>
<b style='color: #c89b3c;'>레벨:</b> {summoner.get('summonerLevel', 'N/A')}<br>
<b style='color: #c89b3c;'>분석 게임 수:</b> {result['match_count']}</p>

<hr style='border: 1px solid #785a28;'>
"""

        for i, match_analysis in enumerate(analysis):
            output += f"""
<h3 style='color: #c89b3c;'>🎮 게임 #{i+1} 분석</h3>
"""
            if 'roaming' in match_analysis:
                roaming = match_analysis['roaming']
                output += f"<p><b>로밍 이벤트:</b> <span style='color: #00d084;'>{len(roaming)}회</span></p>"

            if 'positioning' in match_analysis:
                pos = match_analysis['positioning']
                output += f"""
<p><b>포지셔닝 점수:</b><br>
&nbsp;&nbsp;• 초반: <span style='color: #c89b3c;'>{pos.get('early_game', 0):.2f}/10</span><br>
&nbsp;&nbsp;• 중반: <span style='color: #c89b3c;'>{pos.get('mid_game', 0):.2f}/10</span><br>
&nbsp;&nbsp;• 후반: <span style='color: #c89b3c;'>{pos.get('late_game', 0):.2f}/10</span></p>
"""

            if 'cs_patterns' in match_analysis:
                cs = match_analysis['cs_patterns']
                output += f"""
<p><b>CS 효율:</b><br>
&nbsp;&nbsp;• 분당 CS: <span style='color: #c89b3c;'>{cs.get('avg_cs_per_min', 0):.2f}</span><br>
&nbsp;&nbsp;• 효율성: <span style='color: #c89b3c;'>{cs.get('avg_efficiency', 0):.2f}%</span></p>
"""

            output += "<hr style='border: 1px dashed #463714;'>"

        output += """
<h3 style='color: #c89b3c;'>💡 개선 포인트</h3>
<ul>
    <li>✓ 로밍 타이밍을 더 활용하세요</li>
    <li>✓ 초반 CS 확보에 집중하세요</li>
    <li>✓ 맵 인식을 통한 안전한 포지셔닝</li>
    <li>✓ 오브젝트 타이밍에 맞춰 움직이세요</li>
</ul>
</div>
"""

        self.analysis_result.setHtml(output)
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.statusBar().showMessage('✓ 분석 완료!')

    def show_error(self, error_msg):
        """에러 표시"""
        QMessageBox.critical(self, "오류", error_msg)
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.statusBar().showMessage('✗ 오류 발생')

    def show_champion_info(self, champion_name):
        """챔피언 정보 표시"""
        champion = self.champion_db.get_champion(champion_name)

        if not champion:
            return

        output = f"""
<div style='color: #f0e6d2; font-size: 13px; line-height: 1.8;'>
<h2 style='color: #c89b3c; border-bottom: 2px solid #785a28; padding-bottom: 10px;'>
⚔️ {champion['name']} - {champion['title']}
</h2>

<p><b style='color: #c89b3c;'>포지션:</b> {', '.join(champion['roles'])}<br>
<b style='color: #c89b3c;'>난이도:</b> {champion['difficulty']}/10</p>

<h3 style='color: #c89b3c;'>📈 능력치</h3>
<table style='width: 100%;'>
<tr><td>로밍 점수:</td><td><b style='color: #00d084;'>{champion.get('roaming_score', 0)}/10</b></td></tr>
<tr><td>웨이브 클리어:</td><td><b style='color: #c89b3c;'>{champion.get('wave_clear', 0)}/10</b></td></tr>
<tr><td>폭딜:</td><td><b style='color: #e84057;'>{champion.get('burst_damage', 0)}/10</b></td></tr>
<tr><td>기동성:</td><td><b style='color: #00d084;'>{champion.get('mobility', 0)}/10</b></td></tr>
<tr><td>CC:</td><td><b style='color: #c89b3c;'>{champion.get('cc_score', 0)}/10</b></td></tr>
</table>

<h3 style='color: #c89b3c;'>🎯 스킬 정보</h3>
"""

        for key, skill in champion['skills'].items():
            output += f"""
<p><b style='color: #c89b3c;'>[{key}] {skill['name']}</b><br>
{skill['description']}</p>
"""

        output += f"""
<h3 style='color: #c89b3c;'>⚡ 파워 스파이크</h3>
<p>레벨 <b style='color: #e84057;'>{', '.join(map(str, champion.get('power_spikes', [])))}</b></p>

<h3 style='color: #c89b3c;'>🛡️ 코어 아이템</h3>
<ul>
"""

        for item in champion.get('core_items', []):
            output += f"<li>{item}</li>"

        output += "</ul>"

        matchup = self.champion_db.matchups.get(champion_name, {})
        if matchup:
            output += f"""
<h3 style='color: #c89b3c;'>🎭 챔피언 상성</h3>
<p><b style='color: #00d084;'>✓ 유리한 상대:</b><br>
{', '.join(matchup.get('strong_against', []))}</p>

<p><b style='color: #e84057;'>✗ 불리한 상대:</b><br>
{', '.join(matchup.get('weak_against', []))}</p>
"""

        output += "</div>"

        self.champion_info.setHtml(output)

    def get_realtime_advice(self):
        """실시간 조언"""
        try:
            champion = self.my_champion.currentText()
            game_time = int(self.game_time.text() or 0) * 60
            level = int(self.my_level.text() or 1)

            game_state = {
                'timestamp': game_time,
                'player': {
                    'champion': champion,
                    'level': level,
                    'cs': level * 10,
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

            analysis = self.decision_engine.analyze_game_state(game_state)
            roaming_recs = self.analyzer.get_roaming_recommendations({
                'champion': champion,
                'level': level,
                'wave_state': 'push',
                'enemy_summoners': {},
                'timestamp': game_time
            })

            output = f"""
<div style='color: #f0e6d2; font-size: 13px; line-height: 1.8;'>
<h2 style='color: #c89b3c; border-bottom: 2px solid #785a28; padding-bottom: 10px;'>
🎯 실시간 AI 조언
</h2>

<p><b style='color: #c89b3c;'>챔피언:</b> {champion}<br>
<b style='color: #c89b3c;'>게임 시간:</b> {game_time // 60}분<br>
<b style='color: #c89b3c;'>레벨:</b> {level}<br>
<b style='color: #c89b3c;'>게임 페이즈:</b> {analysis['phase']}</p>

<hr style='border: 1px solid #785a28;'>

<h3 style='color: #c89b3c;'>📊 현재 상태 분석</h3>
<p><b>웨이브 상태:</b><br>
{analysis['wave_state']['recommendation']}</p>

<p><b>맵 포지션:</b><br>
{analysis['map_position']['recommendation']}</p>

<p><b>파워 레벨:</b><br>
{analysis['power_level']['recommendation']}</p>

<h3 style='color: #c89b3c;'>🎯 추천 행동 (우선순위순)</h3>
"""

            for i, action in enumerate(analysis['recommended_actions'], 1):
                priority_color = '#00d084' if action['priority'] >= 8 else '#c89b3c' if action['priority'] >= 6 else '#a09b8c'
                output += f"""
<p style='background: rgba(200, 155, 60, 20); padding: 10px; border-left: 4px solid {priority_color}; margin: 5px 0;'>
<b style='color: {priority_color};'>{i}. [{action['action'].upper()}]</b> (우선순위: {action['priority']}/10)<br>
→ {action['reason']}
</p>
"""

            output += "<h3 style='color: #c89b3c;'>🚀 로밍 분석</h3><ul>"
            for rec in roaming_recs:
                output += f"<li>{rec}</li>"
            output += "</ul>"

            if analysis['objective_priority']['priorities']:
                output += "<h3 style='color: #c89b3c;'>🐉 오브젝트 우선순위</h3>"
                for obj in analysis['objective_priority']['priorities']:
                    output += f"""
<p style='background: rgba(232, 64, 87, 20); padding: 10px; border-left: 4px solid #e84057;'>
<b style='color: #e84057;'>{obj['type'].upper()}</b> - 우선순위: {obj['priority']}/10<br>
→ {obj['recommendation']}
</p>
"""

            output += "</div>"

            self.advice_display.setHtml(output)
            self.statusBar().showMessage('✓ 실시간 조언 생성 완료!')

        except ValueError:
            QMessageBox.warning(self, "입력 오류", "게임 시간과 레벨은 숫자로 입력하세요!")

    def save_settings(self):
        """설정 저장"""
        api_key = self.api_key_input.text().strip()

        if api_key:
            try:
                with open('.env', 'w') as f:
                    f.write(f"RIOT_API_KEY={api_key}\n")
                    f.write("RIOT_REGION=kr\n")

                QMessageBox.information(self, "성공", "설정이 저장되었습니다!")
                self.api_client = RiotAPIClient(api_key=api_key)
                self.statusBar().showMessage('✓ API 키 저장 완료')
            except Exception as e:
                QMessageBox.critical(self, "오류", f"설정 저장 실패: {str(e)}")
        else:
            QMessageBox.warning(self, "입력 오류", "API 키를 입력하세요!")


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = ModernLOLAssistant()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
