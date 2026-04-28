# Office 파일 암호화 탭: .xlsx, .docx, .pptx 파일을 비밀번호로 암호화
import os
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import sys

def build(frame):
    """Office 파일 암호화 탭 UI 빌드"""
    
    # 선택된 파일 경로를 저장할 변수
    selected_file = {"path": None}
    
    # 파일 선택 프레임
    file_frame = ctk.CTkFrame(frame)
    file_frame.pack(fill="x", padx=20, pady=10)
    
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Office 파일 선택",
            filetypes=[
                ("Office 문서", "*.xlsx *.docx"),
                ("Excel", "*.xlsx"),
                ("Word", "*.docx"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            selected_file["path"] = file_path
            file_label.configure(text=f"선택: {Path(file_path).name}")
    
    select_btn = ctk.CTkButton(file_frame, text="파일 선택", command=select_file, width=120)
    select_btn.pack(side="left", padx=5)
    
    file_label = ctk.CTkLabel(file_frame, text="파일 미선택", text_color="gray")
    file_label.pack(side="left", padx=10, fill="x", expand=True)
    
    # 비밀번호 프레임
    password_frame = ctk.CTkFrame(frame)
    password_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(password_frame, text="비밀번호:").pack(side="left", padx=5)
    password_entry = ctk.CTkEntry(password_frame, placeholder_text="비밀번호 입력", show="*", width=300)
    password_entry.pack(side="left", padx=5, fill="x", expand=True)
    
    # 정보 레이블
    info_frame = ctk.CTkFrame(frame)
    info_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(
        info_frame,
        text="지원 형식: .xlsx (Excel), .docx (Word) | 암호화된 파일은 'locked_' 접두사로 저장됩니다.",
        text_color="gray",
        wraplength=700
    ).pack(side="left")
    
    # 실행 버튼 및 결과
    action_frame = ctk.CTkFrame(frame)
    action_frame.pack(fill="x", padx=20, pady=10)
    
    result_label = ctk.CTkLabel(action_frame, text="", text_color="lightgreen")
    result_label.pack(side="left", padx=5)
    
    def encrypt():
        file_path = selected_file["path"]
        password = password_entry.get()
        
        # 검증
        if not file_path:
            messagebox.showwarning("경고", "파일을 선택해주세요.")
            return
        
        if not password:
            messagebox.showwarning("경고", "비밀번호를 입력해주세요.")
            return
        
        # 지원 형식 확인
        supported_extensions = [".xlsx", ".docx"]
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in supported_extensions:
            messagebox.showerror("오류", f"지원하지 않는 형식입니다.\n지원 형식: {', '.join(supported_extensions)}")
            return
        
        try:
            import win32com.client
            
            # 출력 파일명 생성 (locked_ 접두사)
            file_name = Path(file_path).name
            output_name = f"locked_{file_name}"
            output_path = os.path.join(Path(file_path).parent, output_name)
            
            abs_file_path = os.path.abspath(file_path)
            abs_output_path = os.path.abspath(output_path)
            
            try:
                if file_ext == ".xlsx":
                    # Excel 암호화
                    excel = win32com.client.Dispatch("Excel.Application")
                    excel.Visible = False
                    excel.DisplayAlerts = False
                    try:
                        workbook = excel.Workbooks.Open(Filename=abs_file_path, ReadOnly=False)
                        # SaveAs 키워드 인자를 사용하여 암호 설정
                        workbook.SaveAs(Filename=abs_output_path,
                                        FileFormat=51,
                                        Password=password,
                                        WriteResPassword="",
                                        ReadOnlyRecommended=False,
                                        CreateBackup=False)
                        workbook.Close(SaveChanges=False)
                    finally:
                        excel.Quit()
                    
                elif file_ext == ".docx":
                    # Word 암호화
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = False
                    try:
                        doc = word.Documents.Open(FileName=abs_file_path, ReadOnly=False, ConfirmConversions=False)
                        # Word는 문서 객체의 Password 속성을 설정해야 열기 암호가 적용됩니다.
                        try:
                            doc.Password = password
                            doc.WritePassword = ""
                        except Exception:
                            pass
                        doc.SaveAs2(FileName=abs_output_path,
                                    FileFormat=16,
                                    Password=password,
                                    WritePassword="",
                                    ReadOnlyRecommended=False)
                        doc.Close(SaveChanges=False)
                    finally:
                        word.Quit()
                
                result_label.configure(text="암호화 완료")
                messagebox.showinfo(
                    "성공",
                    f"파일이 암호화되었습니다.\n저장경로: {output_path}"
                )
            except AttributeError as ae:
                messagebox.showerror(
                    "오류",
                    f"Office COM 객체 접근 오류 - Office가 제대로 설치되지 않았을 수 있습니다.\n오류: {str(ae)}"
                )
                result_label.configure(text="오류: Office 설정 필요")
            except Exception as office_err:
                messagebox.showerror(
                    "오류",
                    f"파일 암호화 실패:\n{str(office_err)}"
                )
                result_label.configure(text="오류: 암호화 실패")
        except ImportError:
            messagebox.showerror(
                "오류",
                "pywin32 모듈이 로드되지 않았습니다.\n"
                "터미널에서 다음을 실행해주세요:\n"
                "pip install --upgrade pywin32"
            )
            result_label.configure(text="오류: pywin32 필요")
    
    encrypt_btn = ctk.CTkButton(action_frame, text="암호화 실행", command=encrypt, width=150)
    encrypt_btn.pack(side="left", padx=5)
