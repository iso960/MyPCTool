# 확장자 변경 탭: 폴더 내 파일의 확장자를 일괄 변경하는 기능
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

def build(frame):
    """확장자 변경 탭 UI 빌드"""
    
    # 선택된 폴더 경로를 저장할 변수
    selected_folder = {"path": None}
    
    # 상단 레이아웃
    top_frame = ctk.CTkFrame(frame)
    top_frame.pack(side="top", fill="x", padx=20, pady=10)
    
    # 폴더 선택 버튼
    def select_folder():
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            selected_folder["path"] = folder
            folder_label.configure(text=f"선택된 폴더: {folder}")
    
    select_btn = ctk.CTkButton(top_frame, text="폴더 선택", command=select_folder, width=120)
    select_btn.pack(side="left", padx=5)
    
    folder_label = ctk.CTkLabel(top_frame, text="폴더 미선택", text_color="gray")
    folder_label.pack(side="left", padx=10, fill="x", expand=True)
    
    # 입력 프레임
    input_frame = ctk.CTkFrame(frame)
    input_frame.pack(fill="x", padx=20, pady=10)
    
    # 변경 전 확장자
    ctk.CTkLabel(input_frame, text="변경 전 확장자:").grid(row=0, column=0, sticky="w", pady=5)
    before_ext = ctk.CTkEntry(input_frame, placeholder_text="예: txt")
    before_ext.grid(row=0, column=1, sticky="ew", padx=10)
    
    # 변경 후 확장자
    ctk.CTkLabel(input_frame, text="변경 후 확장자:").grid(row=1, column=0, sticky="w", pady=5)
    after_ext = ctk.CTkEntry(input_frame, placeholder_text="예: md")
    after_ext.grid(row=1, column=1, sticky="ew", padx=10)
    
    input_frame.columnconfigure(1, weight=1)
    
    # 하위 폴더 포함 여부
    checkbox_frame = ctk.CTkFrame(frame)
    checkbox_frame.pack(fill="x", padx=20, pady=10)
    
    include_subdirs = ctk.CTkCheckBox(checkbox_frame, text="하위 폴더 포함")
    include_subdirs.pack(side="left")
    include_subdirs.select()
    
    # 실행 버튼 및 결과 레이블
    action_frame = ctk.CTkFrame(frame)
    action_frame.pack(fill="x", padx=20, pady=10)
    
    result_label = ctk.CTkLabel(action_frame, text="", text_color="lightgreen")
    result_label.pack(side="left", padx=5)
    
    def execute():
        folder = selected_folder["path"]
        before = before_ext.get().strip().lstrip(".")
        after = after_ext.get().strip().lstrip(".")
        
        # 검증
        if not folder:
            messagebox.showwarning("경고", "폴더를 선택해주세요.")
            return
        if not before:
            messagebox.showwarning("경고", "변경 전 확장자를 입력해주세요.")
            return
        if not after:
            messagebox.showwarning("경고", "변경 후 확장자를 입력해주세요.")
            return
        
        try:
            count = 0
            include_sub = include_subdirs.get()
            
            if include_sub:
                # 하위 폴더 포함
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file.lower().endswith(f".{before.lower()}"):
                            old_path = os.path.join(root, file)
                            new_name = file.rsplit(".", 1)[0] + f".{after}"
                            new_path = os.path.join(root, new_name)
                            try:
                                os.rename(old_path, new_path)
                                count += 1
                            except Exception as e:
                                messagebox.showerror("오류", f"파일 변경 실패: {file}\n{str(e)}")
            else:
                # 선택된 폴더만
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    if os.path.isfile(file_path) and file.lower().endswith(f".{before.lower()}"):
                        new_name = file.rsplit(".", 1)[0] + f".{after}"
                        new_path = os.path.join(folder, new_name)
                        try:
                            os.rename(file_path, new_path)
                            count += 1
                        except Exception as e:
                            messagebox.showerror("오류", f"파일 변경 실패: {file}\n{str(e)}")
            
            result_label.configure(text=f"변경 완료: {count}개 파일")
            messagebox.showinfo("완료", f"{count}개 파일의 확장자가 변경되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"작업 중 오류 발생:\n{str(e)}")
            result_label.configure(text="오류 발생")
    
    execute_btn = ctk.CTkButton(action_frame, text="실행", command=execute, width=120)
    execute_btn.pack(side="left", padx=5)
