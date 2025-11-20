# LOL AI Assistant - Installation & Setup

## 방법 1: 가장 쉬운 방법 (Python으로 바로 실행)

### 1단계: 필수 프로그램 설치
- Python 3.8 이상 다운로드: https://www.python.org/downloads/
- 설치 시 "Add Python to PATH" 체크!

### 2단계: 프로젝트 다운로드
```cmd
git clone https://github.com/yourusername/lol-ai-assistant.git
cd lol-ai-assistant
```

또는 ZIP 파일 다운로드 후 압축 해제

### 3단계: 필요한 패키지 설치
```cmd
pip install PyQt5 requests python-dotenv
```

### 4단계: 실행!
```cmd
python main.py
```

## 방법 2: EXE 파일 만들기

### 1단계: PyInstaller 설치
```cmd
pip install pyinstaller
```

### 2단계: EXE 빌드
```cmd
python build_exe.py
```

### 3단계: 실행
```cmd
dist\LOL_AI_Assistant.exe
```

## 방법 3: 이미 빌드된 EXE 다운로드 (가장 쉬움!)

1. [Releases 페이지](https://github.com/yourusername/lol-ai-assistant/releases) 방문
2. 최신 버전의 `LOL_AI_Assistant.exe` 다운로드
3. 더블클릭하여 실행!

## 첫 실행 시 설정

### Riot API 키 발급받기
1. https://developer.riotgames.com/ 방문
2. 로그인 (리그 오브 레전드 계정으로)
3. "REGENERATE API KEY" 클릭
4. 키 복사 (RGAPI-로 시작)
5. 앱의 "설정" 탭에서 키 붙여넣기
6. "설정 저장" 클릭

## 사용 방법

### 1. 소환사 분석
- "리플레이 분석" 탭 클릭
- 소환사명 입력 (예: Faker, Hide on bush)
- "분석 시작" 클릭
- 결과 확인!

### 2. 챔피언 정보
- "챔피언 정보" 탭 클릭
- 드롭다운에서 챔피언 선택
- 스킬, 상성, 빌드 확인

### 3. 실시간 조언
- "실시간 조언" 탭 클릭
- 챔피언, 게임 시간, 레벨 입력
- "AI 조언 받기" 클릭
- 최적의 행동 확인!

## 문제 해결

### "python is not recognized"
- Python 재설치 시 "Add to PATH" 체크
- 또는 시스템 환경 변수에 Python 경로 추가

### "pip is not recognized"
```cmd
python -m ensurepip --upgrade
```

### "No module named 'PyQt5'"
```cmd
pip install PyQt5
```

### Windows Defender 경고
- 정상입니다! 새로운 EXE 파일이라 경고가 뜰 수 있습니다
- "추가 정보" → "실행" 클릭

### 실행이 안 됨
1. Visual C++ Redistributable 설치:
   https://aka.ms/vs/17/release/vc_redist.x64.exe
2. 관리자 권한으로 실행
3. 바이러스 백신 예외 처리

## 추가 도움말

- 상세 빌드 가이드: BUILD_GUIDE.md
- 사용 설명서: USAGE.md
- GitHub Issues: 문제 보고

## 시스템 요구사항

- Windows 10/11 (64비트)
- Python 3.8 이상
- 4GB RAM 이상
- 인터넷 연결 (API 사용)

---

**질문이 있으신가요?**
GitHub Issues에 올려주세요!
