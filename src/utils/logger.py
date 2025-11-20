"""
로깅 유틸리티
애플리케이션 로그를 관리합니다.
"""

import logging
import os
from datetime import datetime


def setup_logger(name: str = 'LOLAIAssistant', level=logging.INFO):
    """
    로거를 설정합니다.

    Args:
        name: 로거 이름
        level: 로그 레벨

    Returns:
        설정된 로거
    """
    # 로그 디렉토리 생성
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일명 (날짜별)
    log_file = os.path.join(
        log_dir,
        f'lol_ai_{datetime.now().strftime("%Y%m%d")}.log'
    )

    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 이미 핸들러가 있으면 제거
    if logger.handlers:
        logger.handlers.clear()

    # 파일 핸들러
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
