# 🎮 LOL AI Assistant - 챌린저급 분석 시스템

리그 오브 레전드(League of Legends)를 위한 AI 기반 분석 및 조언 시스템입니다.
챌린저 리플레이를 분석하여 최적의 플레이 방법을 학습하고, 실시간으로 게임 조언을 제공합니다.

## ✨ 주요 기능

### 🔍 리플레이 분석
- **챌린저 리플레이 분석**: 고랭크 플레이어의 게임을 분석하여 패턴 학습
- **로밍 타이밍 AI**: 언제 로밍해야 하는지 AI가 분석하고 추천
- **포지셔닝 분석**: 맵에서의 안전한 위치와 위험 구역 파악
- **CS 패턴 분석**: 파밍 효율성 및 개선 포인트 제시

### 🎯 실시간 조언
- **맵 인식**: 현재 게임 상황에서 적의 위치 예측
- **판단력 지원**: 공격/후퇴 타이밍 결정 지원
- **오브젝트 타이밍**: 드래곤, 바론, 전령 등의 최적 타이밍 알림
- **웨이브 관리**: 푸시/프리즈 등 웨이브 컨트롤 조언

### ⚔️ 챔피언 정보
- **스킬 상세 정보**: 모든 스킬의 쿨다운, 데미지, 효과
- **상성 분석**: 유리한/불리한 매치업 정보
- **파워 스파이크**: 강력해지는 레벨 및 아이템 타이밍
- **아이템 빌드**: 각 챔피언의 최적 아이템 빌드

### 📊 통계 및 분석
- **개인 통계**: 소환사별 상세 통계
- **강점/약점 분석**: 플레이 스타일 분석 및 개선점 제시
- **시야 점수**: 와드 설치 패턴 분석
- **팀플레이 평가**: 아군과의 협력 점수

## 🚀 시작하기

### 필수 요구사항

- Python 3.8 이상
- Riot Games API 키 (무료)

### 설치

1. **저장소 클론**
```bash
git clone https://github.com/yourusername/lol-ai-assistant.git
cd lol-ai-assistant
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **환경 변수 설정**
```bash
cp .env.example .env
# .env 파일을 편집하여 Riot API 키 입력
```

4. **API 키 발급**
   - [Riot Developer Portal](https://developer.riotgames.com/) 방문
   - 로그인 후 API 키 발급
   - `.env` 파일에 키 입력

### 실행

**방법 1: EXE 파일 (Windows)**
```bash
# EXE 파일 빌드
build_exe.bat

# 실행
dist\LOL_AI_Assistant.exe
```

**방법 2: Python 스크립트**
```bash
python main.py
```

**방법 3: 설치 프로그램**
```bash
# Inno Setup으로 설치 프로그램 생성
# installer.iss 파일을 Inno Setup Compiler로 컴파일
```

## 📖 사용 방법

### 1. 리플레이 분석

1. **리플레이 분석** 탭 선택
2. 소환사명 입력
3. **분석 시작** 클릭
4. 결과 확인:
   - 로밍 패턴
   - 포지셔닝 점수
   - CS 효율성
   - 개선 포인트

### 2. 챔피언 정보 확인

1. **챔피언 정보** 탭 선택
2. 드롭다운에서 챔피언 선택
3. 상세 정보 확인:
   - 스킬 정보
   - 파워 스파이크
   - 코어 아이템
   - 상성 정보

### 3. 실시간 조언 받기

1. **실시간 조언** 탭 선택
2. 게임 정보 입력:
   - 내 챔피언
   - 게임 시간
   - 현재 레벨
3. **조언 받기** 클릭
4. AI 추천 행동 확인:
   - 우선순위별 행동
   - 로밍 타이밍
   - 오브젝트 우선순위

## 🏗️ 프로젝트 구조

```
lol-ai-assistant/
├── main.py                      # 메인 실행 파일
├── requirements.txt             # Python 의존성
├── requirements-build.txt       # 빌드용 의존성
├── .env.example                # 환경 변수 예시
├── README.md                   # 프로젝트 문서
├── USAGE.md                    # 사용 가이드
├── BUILD_GUIDE.md              # 빌드 가이드
│
├── build_exe.py                # EXE 빌드 스크립트
├── build_exe.bat               # Windows 빌드 스크립트
├── build_exe.sh                # Linux/Mac 빌드 스크립트
├── installer.iss               # Inno Setup 설치 스크립트
│
├── src/                        # 소스 코드
│   ├── api/                   # Riot API 클라이언트
│   │   └── riot_client.py
│   │
│   ├── data/                  # 데이터 관리
│   │   └── champion_data.py
│   │
│   ├── analysis/              # 리플레이 분석
│   │   └── replay_analyzer.py
│   │
│   ├── ai/                    # AI 의사결정
│   │   └── decision_engine.py
│   │
│   ├── gui/                   # GUI 인터페이스
│   │   ├── main_window.py    # 기본 GUI
│   │   ├── modern_window.py  # 모던 게이밍 GUI ⭐
│   │   └── styles.py         # 스타일시트
│   │
│   └── utils/                 # 유틸리티
│       └── logger.py
│
├── data/                       # 데이터 저장
│   ├── champions/             # 챔피언 데이터
│   ├── replays/               # 리플레이 데이터
│   └── models/                # AI 모델
│
└── tests/                     # 테스트 코드
```

## 🧠 AI 시스템 작동 원리

### 로밍 AI

로밍 타이밍을 결정하는 요소:

1. **레벨 체크**: 파워 스파이크 달성 여부
2. **웨이브 상태**: 푸시 완료 여부
3. **적 위치**: 적의 소환사 주문 쿨다운
4. **오브젝트 타이밍**: 드래곤/전령 스폰 시간
5. **챔피언 특성**: 로밍 강한 챔피언 여부

### 의사결정 엔진

게임 상황을 종합적으로 분석:

1. **게임 페이즈**: 초반/중반/후반 구분
2. **파워 레벨**: 나와 적의 상대적 강함
3. **맵 인식**: 시야 확보 및 적 위치 파악
4. **리소스 관리**: CS, 골드, 경험치
5. **오브젝트 우선순위**: 타이밍별 중요도

## 📊 분석 지표

### 포지셔닝 점수 (1-10)
- **8-10**: 매우 안전한 위치
- **5-7**: 적정 포지션
- **3-4**: 위험한 위치
- **1-2**: 매우 위험

### CS 효율성
- **90-100%**: 챌린저급
- **80-89%**: 다이아급
- **70-79%**: 플레티넘급
- **60-69%**: 골드급
- **60% 미만**: 개선 필요

### 로밍 점수 (1-10)
챔피언별 로밍 능력 평가:
- **9-10**: 탁월한 로밍 (제드, 아리, 탈론)
- **7-8**: 우수한 로밍 (르블랑, 카타리나)
- **5-6**: 평균적 로밍
- **1-4**: 로밍 약함

## 🎓 학습 리소스

### 게임 이해도 향상
- 각 챔피언의 스킬 및 쿨다운 숙지
- 아이템 효과 및 빌드 패스 이해
- 맵 구조 및 정글 동선 파악
- 오브젝트 중요도 및 타이밍 학습

### 기계적 실력
- 정확한 마우스 클릭 연습
- 스킬 콤보 반복 연습
- 막타(CS) 타이밍 연습
- 카이팅 및 포지셔닝 연습

### 맵 인식
- 미니맵 주기적 확인 습관
- 적 정글러 동선 예측
- 와드 효율적 배치
- 위험 신호 감지

## 🔧 설정 및 커스터마이징

### API 설정

`.env` 파일에서 설정 가능:

```env
RIOT_API_KEY=your_api_key_here
RIOT_REGION=kr
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### 지원 지역
- kr (한국)
- na1 (북미)
- euw1 (유럽 서부)
- eun1 (유럽 북동)
- jp1 (일본)

## 🤝 기여하기

기여를 환영합니다! 다음 방법으로 기여할 수 있습니다:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ 주의사항

### Riot Games ToS
- 이 도구는 **분석 및 학습 목적**으로만 사용하세요
- **자동화된 게임 플레이**는 Riot Games ToS 위반입니다
- API 사용 제한을 준수하세요

### 개인정보
- API 키는 절대 공유하지 마세요
- `.env` 파일은 `.gitignore`에 포함되어 있습니다

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙏 감사의 말

- Riot Games - API 제공
- 리그 오브 레전드 커뮤니티
- 오픈소스 기여자들

## 📞 연락처

질문이나 제안사항이 있으시면:
- GitHub Issues 생성
- 이메일: support@lol-ai-assistant.com

## 💻 데스크톱 앱 기능

### 🎨 모던 게이밍 UI
- LOL 스타일의 골드 & 다크 테마
- 애니메이션 효과가 있는 버튼
- 반응형 레이아웃
- 5개의 탭 인터페이스:
  - 🏠 **대시보드**: 시스템 개요 및 빠른 액션
  - 📊 **리플레이 분석**: 소환사 게임 분석
  - ⚔️ **챔피언 정보**: 스킬, 상성, 빌드
  - 🎯 **실시간 조언**: AI 기반 전략 추천
  - ⚙️ **설정**: API 키 및 정보

### 📦 배포 형식
- **.exe 파일**: 단일 실행 파일 (PyInstaller)
- **설치 프로그램**: Inno Setup 기반 인스톨러
- **휴대용 버전**: 설치 없이 실행 가능

## 🔨 EXE 파일 빌드

### 빠른 빌드
```bash
# Windows
build_exe.bat

# Linux/Mac
chmod +x build_exe.sh
./build_exe.sh
```

### 설치 프로그램 생성
1. EXE 파일 먼저 빌드
2. [Inno Setup](https://jrsoftware.org/isdl.php) 설치
3. `installer.iss` 파일을 Inno Setup Compiler로 열기
4. Build → Compile 클릭

자세한 내용은 [BUILD_GUIDE.md](BUILD_GUIDE.md)를 참고하세요.

## 🔄 업데이트 로그

### v1.0.0 (2024-01-20)
- ✨ 초기 릴리스
- 🔍 리플레이 분석 기능
- 🎯 실시간 조언 시스템
- ⚔️ 챔피언 데이터베이스
- 📊 통계 분석 도구
- 🖥️ 모던 게이밍 GUI 데스크톱 애플리케이션
- 📦 EXE 파일 및 설치 프로그램 지원

---

**Made with ❤️ for League of Legends players**

챌린저 랭크를 향해 함께 성장합시다! 🚀
