; LOL AI Assistant 설치 프로그램 스크립트
; Inno Setup 사용

#define MyAppName "LOL AI Assistant"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "LOL AI Team"
#define MyAppURL "https://github.com/yourusername/lol-ai-assistant"
#define MyAppExeName "LOL_AI_Assistant.exe"

[Setup]
; 앱 기본 정보
AppId={{LOL-AI-ASSISTANT-2024}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; 설치 경로
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; 출력 설정
OutputDir=installer_output
OutputBaseFilename=LOL_AI_Assistant_Setup_v{#MyAppVersion}
SetupIconFile=resources\icon.ico
Compression=lzma
SolidCompression=yes

; 권한
PrivilegesRequired=admin

; UI 설정
WizardStyle=modern
DisableProgramGroupPage=yes

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 실행 파일
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; 추가 파일들 (필요시)
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
var
  WelcomeLabel: TLabel;
begin
  WelcomeLabel := TLabel.Create(WizardForm);
  WelcomeLabel.Parent := WizardForm.WelcomePage;
  WelcomeLabel.Caption :=
    'LOL AI Assistant에 오신 것을 환영합니다!' + #13#10 + #13#10 +
    '이 프로그램은 리그 오브 레전드를 위한' + #13#10 +
    'AI 기반 분석 및 조언 시스템입니다.' + #13#10 + #13#10 +
    '주요 기능:' + #13#10 +
    '• 챌린저 리플레이 분석' + #13#10 +
    '• 로밍 타이밍 AI 추천' + #13#10 +
    '• 실시간 게임 조언' + #13#10 +
    '• 챔피언 정보 및 상성 분석';
  WelcomeLabel.Left := 0;
  WelcomeLabel.Top := 170;
  WelcomeLabel.Width := WizardForm.WelcomePage.Width;
end;
