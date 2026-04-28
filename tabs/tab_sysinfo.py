# 시스템 정보 탭: CPU, 메모리, 디스크 사용률 및 OS 정보 표시
import psutil
import platform
import socket
import sys
import customtkinter as ctk

def build(frame):
    """시스템 정보 탭 UI 빌드"""
    
    # 정보를 갱신할 변수
    update_handler = {"id": None}
    auto_refresh = {"enabled": False}
    
    # 상단 정보 프레임
    info_frame = ctk.CTkFrame(frame)
    info_frame.pack(fill="x", padx=20, pady=10)
    
    # OS 정보
    os_name = platform.system() + " " + platform.release()
    computer_name = socket.gethostname()
    python_version = f"Python {sys.version.split()[0]}"
    
    ctk.CTkLabel(info_frame, text=f"OS: {os_name}", text_color="lightblue").pack(anchor="w", pady=2)
    ctk.CTkLabel(info_frame, text=f"컴퓨터명: {computer_name}", text_color="lightblue").pack(anchor="w", pady=2)
    ctk.CTkLabel(info_frame, text=f"Python: {python_version}", text_color="lightblue").pack(anchor="w", pady=2)
    
    # 구분선
    ctk.CTkFrame(frame, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)
    
    # CPU 사용률
    cpu_frame = ctk.CTkFrame(frame)
    cpu_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(cpu_frame, text="CPU 사용률:", text_color="white").pack(anchor="w", pady=5)
    cpu_progress = ctk.CTkProgressBar(cpu_frame, height=20)
    cpu_progress.pack(fill="x", pady=5)
    cpu_label = ctk.CTkLabel(cpu_frame, text="0%", text_color="white")
    cpu_label.pack(anchor="w", pady=5)
    
    # 메모리 사용률
    memory_frame = ctk.CTkFrame(frame)
    memory_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(memory_frame, text="메모리 사용률:", text_color="white").pack(anchor="w", pady=5)
    memory_progress = ctk.CTkProgressBar(memory_frame, height=20)
    memory_progress.pack(fill="x", pady=5)
    memory_label = ctk.CTkLabel(memory_frame, text="0%", text_color="white")
    memory_label.pack(anchor="w", pady=5)
    
    # 디스크 사용률 (C 드라이브)
    disk_frame = ctk.CTkFrame(frame)
    disk_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(disk_frame, text="디스크 사용률 (C:):", text_color="white").pack(anchor="w", pady=5)
    disk_progress = ctk.CTkProgressBar(disk_frame, height=20)
    disk_progress.pack(fill="x", pady=5)
    disk_label = ctk.CTkLabel(disk_frame, text="0%", text_color="white")
    disk_label.pack(anchor="w", pady=5)
    
    def update_info():
        """시스템 정보 업데이트"""
        try:
            # CPU 사용률
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_progress.set(cpu_percent / 100)
            cpu_label.configure(text=f"{cpu_percent}%")
            
            # 메모리 사용률
            memory_info = psutil.virtual_memory()
            memory_percent = memory_info.percent
            memory_used = memory_info.used / (1024 ** 3)  # GB
            memory_total = memory_info.total / (1024 ** 3)  # GB
            memory_progress.set(memory_percent / 100)
            memory_label.configure(text=f"{memory_percent}% ({memory_used:.1f}GB / {memory_total:.1f}GB)")
            
            # 디스크 사용률 (C 드라이브)
            try:
                disk_info = psutil.disk_usage("C:\\")
                disk_percent = disk_info.percent
                disk_used = disk_info.used / (1024 ** 3)  # GB
                disk_total = disk_info.total / (1024 ** 3)  # GB
                disk_progress.set(disk_percent / 100)
                disk_label.configure(text=f"{disk_percent}% ({disk_used:.1f}GB / {disk_total:.1f}GB)")
            except:
                disk_label.configure(text="정보 불가")
            
            # 자동 새로고침이 활성화된 경우
            if auto_refresh["enabled"]:
                update_handler["id"] = frame.after(2000, update_info)
        except Exception as e:
            print(f"시스템 정보 업데이트 오류: {str(e)}")
    
    # 버튼 프레임
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(fill="x", padx=20, pady=10)
    
    # 자동 새로고침 토글
    def toggle_auto_refresh():
        if auto_refresh_switch.get() == 1:
            auto_refresh["enabled"] = True
            update_info()
        else:
            auto_refresh["enabled"] = False
            if update_handler["id"]:
                frame.after_cancel(update_handler["id"])
                update_handler["id"] = None
    
    auto_refresh_switch = ctk.CTkSwitch(
        button_frame,
        text="자동 새로고침",
        command=toggle_auto_refresh,
        onvalue=1,
        offvalue=0
    )
    auto_refresh_switch.pack(side="left", padx=5)
    
    # 수동 새로고침 버튼
    def manual_refresh():
        if update_handler["id"]:
            frame.after_cancel(update_handler["id"])
            update_handler["id"] = None
            auto_refresh["enabled"] = False
            auto_refresh_switch.deselect()
        update_info()
    
    manual_refresh_btn = ctk.CTkButton(
        button_frame,
        text="수동 새로고침",
        command=manual_refresh,
        width=150
    )
    manual_refresh_btn.pack(side="left", padx=5)
    
    # 초기 정보 로드
    update_info()
