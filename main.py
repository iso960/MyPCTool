# MyPCTool: 메인 애플리케이션 진입점 - CustomTkinter 기반 PC 관리 도구
import customtkinter as ctk
from tabs.tab_rename import build as build_rename
from tabs.tab_installed import build as build_installed
from tabs.tab_process import build as build_process
from tabs.tab_office import build as build_office
from tabs.tab_sysinfo import build as build_sysinfo

# 앱 초기화
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MyPCToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MyPCTool")
        self.geometry("1000x700")
        
        # 탭뷰 생성
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        # 탭 5개 추가
        self.tab_rename = self.tabview.add("확장자 변경")
        self.tab_installed = self.tabview.add("설치 프로그램")
        self.tab_process = self.tabview.add("프로세스 목록")
        self.tab_office = self.tabview.add("Office 암호화")
        self.tab_sysinfo = self.tabview.add("시스템 정보")
        
        # 각 탭 빌드 함수 호출
        build_rename(self.tab_rename)
        build_installed(self.tab_installed)
        build_process(self.tab_process)
        build_office(self.tab_office)
        build_sysinfo(self.tab_sysinfo)

if __name__ == "__main__":
    app = MyPCToolApp()
    app.mainloop()
