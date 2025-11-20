# 🔨 LOL AI Assistant - 빌드 가이드

## EXE 파일 만들기

### 방법 1: 자동 빌드 스크립트 사용 (권장)

#### Windows
```bash
# 1. 빌드 스크립트 실행
build_exe.bat

# 2. dist 폴더에서 LOL_AI_Assistant.exe 확인
```

#### Linux/Mac
```bash
# 1. 실행 권한 부여
chmod +x build_exe.sh

# 2. 빌드 스크립트 실행
./build_exe.sh

# 3. dist 폴더에서 실행 파일 확인
```

### 방법 2: Python 스크립트 사용

```bash
# 1. 빌드용 의존성 설치
pip install -r requirements-build.txt

# 2. 빌드 스크립트 실행
python build_exe.py

# 3. dist/LOL_AI_Assistant.exe 생성 확인
```

### 방법 3: PyInstaller 직접 사용

```bash
# Windows
pyinstaller --name=LOL_AI_Assistant --onefile --windowed --add-data="src;src" src/gui/modern_window.py

# Linux/Mac
pyinstaller --name=LOL_AI_Assistant --onefile --windowed --add-data="src:src" src/gui/modern_window.py
```

## 설치 프로그램 만들기

### Inno Setup 사용 (Windows)

1. **Inno Setup 다운로드 및 설치**
   - https://jrsoftware.org/isdl.php

2. **EXE 파일 먼저 빌드**
   ```bash
   build_exe.bat
   ```

3. **Inno Setup 실행**
   - Inno Setup Compiler 실행
   - `installer.iss` 파일 열기
   - Build → Compile 클릭

4. **설치 프로그램 확인**
   - `installer_output/LOL_AI_Assistant_Setup_v1.0.0.exe` 생성됨

### NSIS 사용 (대안)

```nsis
# installer.nsi
!define APP_NAME "LOL AI Assistant"
!define APP_VERSION "1.0.0"

Name "${APP_NAME}"
OutFile "LOL_AI_Assistant_Setup.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"

Section "Install"
    SetOutPath "$INSTDIR"
    File "dist\LOL_AI_Assistant.exe"
    File "README.md"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\LOL_AI_Assistant.exe"
SectionEnd
```

## 빌드 문제 해결

### PyQt5 관련 오류
```bash
pip uninstall PyQt5 PyQt5-sip
pip install PyQt5==5.15.10
```

### 모듈 찾기 오류
```bash
# hidden-import 추가
pyinstaller --hidden-import=PyQt5 --hidden-import=requests ...
```

### DLL 누락 오류 (Windows)
```bash
# Visual C++ Redistributable 설치 필요
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

## 빌드 최적화

### 파일 크기 줄이기

1. **UPX 압축 사용**
```bash
# UPX 다운로드: https://upx.github.io/
pyinstaller --upx-dir=C:\path\to\upx ...
```

2. **불필요한 라이브러리 제외**
```bash
pyinstaller --exclude-module=matplotlib --exclude-module=pandas ...
```

### 빌드 속도 향상

```bash
# 캐시 활용
pyinstaller --clean --noconfirm ...
```

## 배포 체크리스트

- [ ] EXE 파일이 정상 실행되는가?
- [ ] API 키 설정이 작동하는가?
- [ ] 모든 탭이 정상 작동하는가?
- [ ] 에러 메시지가 표시되는가?
- [ ] 아이콘이 제대로 표시되는가?
- [ ] 프로그램이 완전히 종료되는가?
- [ ] README.md가 포함되어 있는가?
- [ ] 설치 프로그램이 정상 작동하는가?
- [ ] 언인스톨이 정상 작동하는가?

## 코드 서명 (선택사항)

### Windows

```bash
# 인증서가 있는 경우
signtool sign /f mycert.pfx /p password /t http://timestamp.digicert.com dist\LOL_AI_Assistant.exe
```

### Mac

```bash
# Apple Developer 인증서 필요
codesign --force --deep --sign "Developer ID Application: Your Name" dist/LOL_AI_Assistant
```

## 자동 업데이트 (선택사항)

### GitHub Releases 사용

```python
import requests

def check_update():
    response = requests.get(
        "https://api.github.com/repos/yourusername/lol-ai-assistant/releases/latest"
    )
    latest_version = response.json()["tag_name"]
    # 버전 비교 로직
```

## 빌드 환경

### 권장 환경
- Python 3.8 - 3.11
- Windows 10/11 또는 Ubuntu 20.04+
- 최소 4GB RAM
- 1GB 디스크 공간

### 의존성 버전 고정
```bash
# 현재 환경의 의존성 내보내기
pip freeze > requirements-freeze.txt

# 재현 가능한 빌드를 위해 사용
pip install -r requirements-freeze.txt
```

## CI/CD 자동 빌드

### GitHub Actions

```yaml
name: Build EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements-build.txt
      - run: python build_exe.py
      - uses: actions/upload-artifact@v2
        with:
          name: LOL_AI_Assistant
          path: dist/LOL_AI_Assistant.exe
```

## 라이선스 및 주의사항

- EXE 파일에 LICENSE 파일 포함
- Riot Games ToS 준수 안내 포함
- 오픈소스 라이선스 고지

---

문제가 발생하면 GitHub Issues에 보고해주세요!
