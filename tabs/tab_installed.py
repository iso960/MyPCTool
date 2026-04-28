# 설치 프로그램 탭: Windows 레지스트리에서 설치된 프로그램 목록 조회 및 저장
import winreg
import csv
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime

def build(frame):
    """설치 프로그램 탭 UI 빌드"""
    
    # 프로그램 목록 저장할 변수
    programs_list = []
    
    # 버튼 프레임
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(side="top", fill="x", padx=10, pady=10)
    
    # 스크롤 가능한 프레임과 텍스트박스
    scrollable_frame = ctk.CTkScrollableFrame(frame)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    textbox = ctk.CTkTextbox(scrollable_frame, height=400)
    textbox.pack(fill="both", expand=True)
    
    def load_programs():
        """레지스트리에서 설치 프로그램 목록 로드"""
        nonlocal programs_list
        programs_list = []
        textbox.delete("1.0", "end")
        
        try:
            textbox.insert("end", "설치 프로그램 목록 불러오는 중...\n\n")
            frame.update()
            
            # 두 경로에서 모두 읽기
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, 
                 r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, 
                 r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            
            for hkey, subkey in registry_paths:
                try:
                    reg_key = winreg.OpenKey(hkey, subkey)
                    for i in range(winreg.QueryInfoKey(reg_key)[0]):
                        try:
                            keyname = winreg.EnumKey(reg_key, i)
                            sub_key = winreg.OpenKey(hkey, subkey + "\\" + keyname)
                            
                            try:
                                name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                            except:
                                name = "N/A"
                            
                            try:
                                version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                            except:
                                version = "N/A"
                            
                            try:
                                install_date = winreg.QueryValueEx(sub_key, "InstallDate")[0]
                            except:
                                install_date = "N/A"
                            
                            if name and name != "N/A":
                                programs_list.append({
                                    "name": name,
                                    "version": version,
                                    "install_date": install_date
                                })
                            
                            winreg.CloseKey(sub_key)
                        except:
                            pass
                    winreg.CloseKey(reg_key)
                except:
                    pass
            
            # 중복 제거 (프로그램명 기준)
            unique_programs = {}
            for prog in programs_list:
                if prog["name"] not in unique_programs:
                    unique_programs[prog["name"]] = prog
            programs_list = list(unique_programs.values())
            
            # 목록 표시
            textbox.delete("1.0", "end")
            textbox.insert("end", "프로그램명 / 버전 / 설치날짜\n")
            textbox.insert("end", "=" * 100 + "\n\n")
            
            for prog in sorted(programs_list, key=lambda x: x["name"]):
                line = f"{prog['name']}\n  버전: {prog['version']}, 설치일: {prog['install_date']}\n\n"
                textbox.insert("end", line)
            
            textbox.insert("end", f"\n총 {len(programs_list)}개 프로그램")
            textbox.configure(state="disabled")
            messagebox.showinfo("완료", f"총 {len(programs_list)}개의 프로그램을 불러왔습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"프로그램 목록 로드 실패:\n{str(e)}")
            textbox.insert("end", f"오류: {str(e)}")
    
    def save_csv():
        """CSV 파일로 저장"""
        if not programs_list:
            messagebox.showwarning("경고", "먼저 설치 프로그램 목록을 불러와주세요.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"installed_programs_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["프로그램명", "버전", "설치날짜"])
                for prog in sorted(programs_list, key=lambda x: x["name"]):
                    writer.writerow([prog["name"], prog["version"], prog["install_date"]])
            
            messagebox.showinfo("성공", f"CSV 파일이 저장되었습니다:\n{file_path}")
        except Exception as e:
            messagebox.showerror("오류", f"CSV 저장 실패:\n{str(e)}")
    
    # 버튼 배치
    load_btn = ctk.CTkButton(button_frame, text="목록 불러오기", command=load_programs, width=150)
    load_btn.pack(side="left", padx=5)
    
    save_btn = ctk.CTkButton(button_frame, text="CSV로 저장", command=save_csv, width=150)
    save_btn.pack(side="left", padx=5)
