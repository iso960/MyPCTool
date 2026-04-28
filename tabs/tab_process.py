# 프로세스 목록 탭: 현재 실행 중인 프로세스를 표 형태로 표시하고 관리
import psutil
import customtkinter as ctk
from tkinter import messagebox

def build(frame):
    """프로세스 목록 탭 UI 빌드"""
    
    # 버튼 프레임
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(side="top", fill="x", padx=10, pady=10)
    
    # 스크롤 가능한 프레임
    scrollable_frame = ctk.CTkScrollableFrame(frame)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def refresh_processes():
        """프로세스 목록 새로고침"""
        # 기존 위젯 제거
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            # 헤더 행
            header_frame = ctk.CTkFrame(scrollable_frame, fg_color="#2C3E50")
            header_frame.pack(fill="x", padx=5, pady=5)
            
            ctk.CTkLabel(header_frame, text="PID", width=80, anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(header_frame, text="프로세스명", width=250, anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(header_frame, text="CPU (%)", width=80, anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(header_frame, text="메모리 (MB)", width=100, anchor="w").pack(side="left", padx=5, pady=5)
            
            # 프로세스 데이터 수집
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    cputime = proc.cpu_percent(interval=0.01)
                    meminfo = proc.memory_info()
                    memory_mb = meminfo.rss / 1024 / 1024
                    
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': cputime,
                        'memory': memory_mb
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # 메모리 기준 내림차순 정렬
            processes.sort(key=lambda x: x['memory'], reverse=True)
            
            # 데이터 행 표시
            for i, proc in enumerate(processes[:100]):  # 상위 100개만 표시
                row_frame = ctk.CTkFrame(
                    scrollable_frame,
                    fg_color="#34495E" if i % 2 == 0 else "#2C3E50"
                )
                row_frame.pack(fill="x", padx=5, pady=2)
                
                ctk.CTkLabel(
                    row_frame,
                    text=str(proc['pid']),
                    width=80,
                    anchor="w"
                ).pack(side="left", padx=5, pady=3)
                
                ctk.CTkLabel(
                    row_frame,
                    text=proc['name'][:30],
                    width=250,
                    anchor="w"
                ).pack(side="left", padx=5, pady=3)
                
                ctk.CTkLabel(
                    row_frame,
                    text=f"{proc['cpu']:.1f}",
                    width=80,
                    anchor="w"
                ).pack(side="left", padx=5, pady=3)
                
                ctk.CTkLabel(
                    row_frame,
                    text=f"{proc['memory']:.1f}",
                    width=100,
                    anchor="w"
                ).pack(side="left", padx=5, pady=3)
            
            messagebox.showinfo("완료", f"총 {len(processes)}개의 프로세스가 표시되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"프로세스 목록 조회 실패:\n{str(e)}")
    
    # 새로고침 버튼
    refresh_btn = ctk.CTkButton(button_frame, text="새로고침", command=refresh_processes, width=150)
    refresh_btn.pack(side="left", padx=5)
    
    # 초기 로드
    refresh_processes()
