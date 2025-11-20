"""
LOL AI Assistant - 스타일시트
게이밍 스타일의 모던한 디자인
"""

# 메인 다크 테마 (LOL 스타일)
MAIN_STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #0a1428, stop:1 #1a2332);
}

QWidget {
    background-color: transparent;
    color: #f0e6d2;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* 탭 위젯 스타일 */
QTabWidget::pane {
    border: 2px solid #c89b3c;
    border-radius: 8px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #0a0e27, stop:1 #1a1e2e);
    padding: 5px;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #1a1e2e, stop:1 #0a0e27);
    border: 2px solid #463714;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 12px 25px;
    margin-right: 5px;
    color: #a09b8c;
    font-size: 13px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #c89b3c, stop:1 #785a28);
    color: #0a0e27;
    border: 2px solid #c89b3c;
}

QTabBar::tab:hover:!selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #785a28, stop:1 #463714);
    color: #f0e6d2;
}

/* 그룹박스 스타일 */
QGroupBox {
    border: 2px solid #785a28;
    border-radius: 10px;
    margin-top: 15px;
    padding-top: 20px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(26, 30, 46, 180),
                                stop:1 rgba(10, 14, 39, 180));
    font-weight: bold;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 15px;
    color: #c89b3c;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #785a28, stop:1 #c89b3c);
    border-radius: 5px;
    margin-left: 10px;
}

/* 버튼 스타일 */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #c89b3c, stop:1 #785a28);
    border: 2px solid #463714;
    border-radius: 8px;
    padding: 10px 20px;
    color: #0a0e27;
    font-size: 13px;
    font-weight: bold;
    min-height: 35px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #f0e6d2, stop:1 #c89b3c);
    border: 2px solid #c89b3c;
    color: #0a0e27;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #785a28, stop:1 #463714);
    border: 2px solid #c89b3c;
    color: #f0e6d2;
}

QPushButton:disabled {
    background: #3c3c41;
    border: 2px solid #2c2c31;
    color: #5b5a56;
}

/* 입력 필드 스타일 */
QLineEdit, QComboBox {
    background: #0a0e27;
    border: 2px solid #463714;
    border-radius: 6px;
    padding: 8px 12px;
    color: #f0e6d2;
    font-size: 12px;
    min-height: 30px;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #c89b3c;
    background: #1a1e2e;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid #c89b3c;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background: #0a0e27;
    border: 2px solid #c89b3c;
    selection-background-color: #785a28;
    selection-color: #f0e6d2;
    color: #f0e6d2;
}

/* 텍스트 영역 스타일 */
QTextEdit {
    background: #0a0e27;
    border: 2px solid #463714;
    border-radius: 8px;
    padding: 10px;
    color: #f0e6d2;
    font-size: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
}

QTextEdit:focus {
    border: 2px solid #785a28;
}

/* 프로그레스바 스타일 */
QProgressBar {
    border: 2px solid #463714;
    border-radius: 8px;
    background: #0a0e27;
    text-align: center;
    color: #f0e6d2;
    font-weight: bold;
    min-height: 25px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #c89b3c, stop:0.5 #f0e6d2, stop:1 #c89b3c);
    border-radius: 6px;
}

/* 레이블 스타일 */
QLabel {
    color: #f0e6d2;
    background: transparent;
    font-size: 12px;
}

/* 스크롤바 스타일 */
QScrollBar:vertical {
    border: none;
    background: #0a0e27;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #785a28;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #c89b3c;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #0a0e27;
    height: 12px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #785a28;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background: #c89b3c;
}

/* 상태바 스타일 */
QStatusBar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #0a0e27, stop:1 #1a1e2e);
    border-top: 2px solid #785a28;
    color: #c89b3c;
    font-weight: bold;
}

/* 툴팁 스타일 */
QToolTip {
    background: #1a1e2e;
    border: 2px solid #c89b3c;
    border-radius: 5px;
    padding: 5px;
    color: #f0e6d2;
    font-size: 11px;
}
"""

# 타이틀 레이블 스타일
TITLE_STYLE = """
QLabel {
    color: #c89b3c;
    font-size: 24px;
    font-weight: bold;
    padding: 15px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 transparent,
                                stop:0.5 rgba(200, 155, 60, 50),
                                stop:1 transparent);
    border-radius: 10px;
}
"""

# 섹션 타이틀 스타일
SECTION_TITLE_STYLE = """
QLabel {
    color: #f0e6d2;
    font-size: 16px;
    font-weight: bold;
    padding: 8px;
}
"""

# 성공 버튼 스타일
SUCCESS_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00d084, stop:1 #00a368);
    border: 2px solid #008c5a;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    font-size: 13px;
    font-weight: bold;
    min-height: 35px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00f5a0, stop:1 #00d084);
    border: 2px solid #00d084;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #008c5a, stop:1 #006b45);
}
"""

# 경고 버튼 스타일
WARNING_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #e84057, stop:1 #c73249);
    border: 2px solid #a0283c;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    font-size: 13px;
    font-weight: bold;
    min-height: 35px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ff5066, stop:1 #e84057);
    border: 2px solid #e84057;
}
"""

# 정보 패널 스타일
INFO_PANEL_STYLE = """
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(200, 155, 60, 30),
                                stop:1 rgba(120, 90, 40, 30));
    border: 2px solid #c89b3c;
    border-radius: 10px;
    padding: 15px;
}
"""

# 통계 카드 스타일
STAT_CARD_STYLE = """
QGroupBox {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 rgba(10, 14, 39, 200),
                                stop:1 rgba(26, 30, 46, 200));
    border: 2px solid #785a28;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
}

QGroupBox::title {
    color: #c89b3c;
    font-size: 16px;
    font-weight: bold;
    padding: 8px 15px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #785a28, stop:1 #c89b3c);
    border-radius: 6px;
}
"""
