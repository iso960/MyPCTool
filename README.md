# MyPCTool

MyPCTool은 Windows에서 CustomTkinter 기반 GUI로 동작하는 PC 관리 도구입니다. `확장자 변경`, `설치 프로그램 목록`, `프로세스 목록`, `Office 파일 암호화`, `시스템 정보` 탭을 제공합니다.

## 주요 기능

- **확장자 변경**: 선택된 폴더 및 하위 폴더 내 파일의 확장자를 일괄 변경
- **설치 프로그램 목록**: Windows 레지스트리에서 설치된 프로그램 목록 조회 후 CSV 저장
- **프로세스 목록**: `psutil`을 이용해 실행 중인 프로세스를 메모리 사용량 기준으로 정렬하여 표시
- **Office 파일 암호화**: `.xlsx` 및 `.docx` 파일을 선택하고 비밀번호를 적용하여 `locked_` 접두사가 붙은 새 파일로 저장
- **시스템 정보**: CPU, 메모리, 디스크 사용률 및 OS/컴퓨터 이름/Python 버전 표시, 자동 새로고침 지원

## 파일 구조

```text
MyPCTool/
├── main.py
├── requirements.txt
├── README.md
└── tabs/
    ├── __init__.py
    ├── tab_rename.py
    ├── tab_installed.py
    ├── tab_process.py
    ├── tab_office.py
    └── tab_sysinfo.py
```

## 설치 및 실행

Windows 환경에서 다음을 실행하세요.

```bash
python -m pip install -r requirements.txt
python main.py
```

## 요구사항

- Python 3.10 이상
- Windows
- Microsoft Office 설치 (Excel/Word)
- `customtkinter`
- `psutil`
- `pywin32`

## 참고

- Office 암호화 기능은 현재 `.xlsx`와 `.docx`만 지원합니다.
- `tab_office.py`는 Word 암호화 시 `Document.Password` 속성 및 `SaveAs2` 호출을 사용합니다.
- 시스템 정보 탭은 Windows 11을 올바르게 감지하도록 레지스트리 기반 OS 판별을 수행합니다.
