# MyPCTool — Claude Code 프롬프트

## 역할
너는 Python GUI 애플리케이션 전문 개발자야.
아래 명세를 보고 완성된 코드를 작성해줘.

---

## 프로젝트 개요

- **프로젝트명**: MyPCTool
- **목적**: PC 관리 기능을 하나로 묶은 GUI 도구
- **언어**: Python 3.10+
- **GUI 라이브러리**: CustomTkinter
- **타겟 OS**: Windows

---

## 파일 구조

아래 구조로 파일을 분리해서 작성해줘.

```
MyPCTool/
├── main.py
├── tabs/
│   ├── __init__.py
│   ├── tab_rename.py
│   ├── tab_installed.py
│   ├── tab_process.py
│   ├── tab_office.py
│   └── tab_sysinfo.py
└── requirements.txt
```

---

## UI 구조

- `main.py`에서 `CTk()` 앱을 생성하고, `CTkTabview`로 5개 탭을 구성한다.
- 탭 이름: `확장자 변경` / `설치 프로그램` / `프로세스 목록` / `Office 암호화` / `시스템 정보`
- 각 탭의 내용은 `tabs/` 폴더의 각 파일에서 함수로 구현하고, `main.py`에서 `탭 프레임`을 넘겨받아 위젯을 배치한다.
- 전체 테마: `dark`, 색상 테마: `blue`

---

## 기능 명세

### ① 탭: 확장자 변경 (`tab_rename.py`)
- 폴더 선택 버튼 → `filedialog.askdirectory()`로 경로 선택
- 입력창 2개: `변경 전 확장자` (예: txt), `변경 후 확장자` (예: md)
- `실행` 버튼 클릭 시 해당 폴더 내 파일을 순회하며 확장자 일괄 변경
  - 하위 폴더 포함 여부는 체크박스로 선택 가능
- 변경된 파일 수를 결과 레이블로 표시
- 예외처리: 폴더 미선택, 확장자 미입력 시 경고 메시지박스

### ② 탭: 설치 프로그램 목록 (`tab_installed.py`)
- `winreg`로 아래 두 경로에서 설치 프로그램 목록을 읽어온다:
  - `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`
  - `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall`
- `CTkScrollableFrame` 안에 `CTkTextbox`로 목록 출력 (프로그램명 / 버전 / 설치날짜)
- `목록 불러오기` 버튼, `CSV로 저장` 버튼
- CSV 저장 시 `filedialog.asksaveasfilename()`으로 경로 지정

### ③ 탭: 프로세스 목록 (`tab_process.py`)
- `psutil.process_iter()`로 실행 중인 프로세스 목록 조회
- `CTkScrollableFrame` 안에 표 형태(헤더 + 데이터 행)로 표시: PID / 프로세스명 / CPU(%) / 메모리(MB)
- `새로고침` 버튼으로 목록 갱신
- 목록은 메모리 사용량 기준 내림차순 정렬

### ④ 탭: Office 파일 암호화 (`tab_office.py`)
- 지원 형식: `.xlsx`, `.docx`, `.pptx`
- 파일 선택 버튼 → `filedialog.askopenfilename()`
- 비밀번호 입력창 (show="*")
- `암호화 실행` 버튼 클릭 시 `msoffcrypto-tool`로 암호화
  - 암호화된 파일은 원본 파일명 앞에 `locked_` 접두사 붙여 같은 폴더에 저장
- 성공/실패 메시지박스로 결과 안내
- 예외처리: 파일 미선택, 비밀번호 미입력, 지원하지 않는 형식

### ⑤ 탭: 시스템 정보 (`tab_sysinfo.py`)
- `psutil`로 아래 항목을 표시:
  - CPU 사용률 (%) — `CTkProgressBar` + 텍스트
  - 메모리 사용률 (%) + 사용량/전체 (GB) — `CTkProgressBar` + 텍스트
  - 디스크 사용률 (C 드라이브) — `CTkProgressBar` + 텍스트
  - OS 정보, 컴퓨터 이름, Python 버전
- `자동 새로고침` 토글 스위치: ON이면 2초마다 `after()`로 자동 갱신
- `수동 새로고침` 버튼도 별도 제공

---

## 공통 요구사항

- 모든 탭은 각자의 파일(`tabs/tab_*.py`)에 `def build(frame):` 형태의 함수로 구현
- `main.py`에서 각 탭 프레임을 만들고 `build(frame)` 호출하는 방식
- 예외는 `try/except`로 처리하고 `CTkMessagebox` 또는 `tkinter.messagebox`로 사용자에게 안내
- 코드 상단에 각 파일의 역할을 한 줄 주석으로 명시

---

## requirements.txt 내용

```
customtkinter
psutil
msoffcrypto-tool
```

---

## 최종 요청

위 명세대로 `main.py`부터 `tabs/` 내 5개 파일까지 전체 코드를 작성해줘.
각 파일을 명확히 구분해서 출력하고, 실행 방법도 마지막에 간단히 안내해줘.