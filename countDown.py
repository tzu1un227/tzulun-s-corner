import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, timedelta
import winsound
import sys

class CountdownTimer:
    def __init__(self, name, total_seconds, callback=None):
        self.name = name
        self.total_seconds = total_seconds
        self.remaining_seconds = total_seconds
        self.is_running = False
        self.is_paused = False
        self.thread = None
        self.callback = callback
        
    def start(self):
        if not self.is_running and self.remaining_seconds > 0:
            self.is_running = True
            self.is_paused = False
            self.thread = threading.Thread(target=self._countdown, daemon=True)
            self.thread.start()
    
    def pause(self):
        self.is_paused = True
        
    def resume(self):
        if self.is_paused:
            self.is_paused = False
    
    def stop(self):
        self.is_running = False
        self.is_paused = False
        self.remaining_seconds = self.total_seconds
        
    def _countdown(self):
        while self.is_running and self.remaining_seconds > 0:
            if not self.is_paused:
                self.remaining_seconds -= 1
                if self.callback:
                    self.callback(self)
            time.sleep(1)
        
        if self.remaining_seconds <= 0 and self.is_running:
            self.is_running = False
            self._time_up()
    
    def _time_up(self):
        # 播放系統提示音
        try:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            print(f"計時器 '{self.name}' 時間到!")
        
        if self.callback:
            self.callback(self, finished=True)
    
    def get_time_string(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多重倒數計時器")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.timers = []
        self.timer_frames = []
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # 標題
        title_label = tk.Label(self.root, text="多重倒數計時器", 
                              font=('Arial', 16, 'bold'), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        # 新增計時器區域
        add_frame = tk.Frame(self.root, bg='#f0f0f0')
        add_frame.pack(pady=10, padx=20, fill='x')
        
        # 計時器名稱
        tk.Label(add_frame, text="計時器名稱:", bg='#f0f0f0').grid(row=0, column=0, padx=5, sticky='w')
        self.name_entry = tk.Entry(add_frame, width=15)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        # 時間輸入
        tk.Label(add_frame, text="小時:", bg='#f0f0f0').grid(row=0, column=2, padx=5, sticky='w')
        self.hours_var = tk.StringVar(value="0")
        self.hours_spin = tk.Spinbox(add_frame, from_=0, to=23, width=5, 
                                    textvariable=self.hours_var, wrap=True)
        self.hours_spin.grid(row=0, column=3, padx=2)
        
        tk.Label(add_frame, text="分鐘:", bg='#f0f0f0').grid(row=0, column=4, padx=5, sticky='w')
        self.minutes_var = tk.StringVar(value="5")
        self.minutes_spin = tk.Spinbox(add_frame, from_=0, to=59, width=5, 
                                      textvariable=self.minutes_var, wrap=True)
        self.minutes_spin.grid(row=0, column=5, padx=2)
        
        tk.Label(add_frame, text="秒:", bg='#f0f0f0').grid(row=0, column=6, padx=5, sticky='w')
        self.seconds_var = tk.StringVar(value="0")
        self.seconds_spin = tk.Spinbox(add_frame, from_=0, to=59, width=5, 
                                      textvariable=self.seconds_var, wrap=True)
        self.seconds_spin.grid(row=0, column=7, padx=2)
        
        # 新增按鈕
        add_btn = tk.Button(add_frame, text="新增計時器", 
                           command=self.add_timer,
                           bg='#4CAF50', fg='white', 
                           font=('Arial', 10, 'bold'))
        add_btn.grid(row=0, column=8, padx=10)
        
        # 分隔線
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=10)
        
        # 計時器顯示區域（使用滾動框）
        self.canvas = tk.Canvas(self.root, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        self.scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
    def add_timer(self):
        name = self.name_entry.get().strip()
        if not name:
            name = f"計時器 {len(self.timers) + 1}"
        
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds <= 0:
                messagebox.showerror("錯誤", "請設定大於0的時間!")
                return
                
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的時間!")
            return
        
        # 檢查名稱是否重複
        existing_names = [timer.name for timer in self.timers]
        original_name = name
        counter = 1
        while name in existing_names:
            name = f"{original_name} ({counter})"
            counter += 1
        
        timer = CountdownTimer(name, total_seconds, self.timer_callback)
        self.timers.append(timer)
        self.create_timer_ui(timer)
        
        # 清空輸入框
        self.name_entry.delete(0, tk.END)
        
        # 重置 Spinbox 值
        self.hours_var.set("0")
        self.minutes_var.set("5")
        self.seconds_var.set("0")
        
    def create_timer_ui(self, timer):
        # 創建單個計時器的UI框架
        frame = tk.Frame(self.scrollable_frame, bg='white', relief='raised', bd=2)
        frame.pack(fill='x', padx=10, pady=5)
        
        # 計時器名稱和時間顯示
        info_frame = tk.Frame(frame, bg='white')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        name_label = tk.Label(info_frame, text=timer.name, 
                             font=('Arial', 12, 'bold'), 
                             bg='white', fg='#333')
        name_label.pack(side='left')
        
        time_label = tk.Label(info_frame, text=timer.get_time_string(), 
                             font=('Arial', 14, 'bold'), 
                             bg='white', fg='#2196F3')
        time_label.pack(side='right')
        
        # 控制按鈕
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        start_btn = tk.Button(btn_frame, text="開始", 
                             command=lambda: self.start_timer(timer),
                             bg='#4CAF50', fg='white', width=8)
        start_btn.pack(side='left', padx=2)
        
        pause_btn = tk.Button(btn_frame, text="暫停", 
                             command=lambda: self.pause_timer(timer),
                             bg='#FF9800', fg='white', width=8)
        pause_btn.pack(side='left', padx=2)
        
        resume_btn = tk.Button(btn_frame, text="繼續", 
                              command=lambda: self.resume_timer(timer),
                              bg='#2196F3', fg='white', width=8)
        resume_btn.pack(side='left', padx=2)
        
        stop_btn = tk.Button(btn_frame, text="停止", 
                            command=lambda: self.stop_timer(timer),
                            bg='#f44336', fg='white', width=8)
        stop_btn.pack(side='left', padx=2)
        
        delete_btn = tk.Button(btn_frame, text="刪除", 
                              command=lambda: self.delete_timer(timer),
                              bg='#9E9E9E', fg='white', width=8)
        delete_btn.pack(side='right', padx=2)
        
        # 狀態指示器
        status_label = tk.Label(frame, text="待機", 
                               font=('Arial', 10), 
                               bg='white', fg='#666')
        status_label.pack(pady=(0, 5))
        
        # 儲存UI元素引用
        timer_ui = {
            'frame': frame,
            'time_label': time_label,
            'status_label': status_label,
            'timer': timer
        }
        
        self.timer_frames.append(timer_ui)
        
    def start_timer(self, timer):
        timer.start()
        
    def pause_timer(self, timer):
        timer.pause()
        
    def resume_timer(self, timer):
        timer.resume()
        
    def stop_timer(self, timer):
        timer.stop()
        
    def delete_timer(self, timer):
        timer.stop()
        self.timers.remove(timer)
        
        # 移除UI
        for timer_ui in self.timer_frames:
            if timer_ui['timer'] == timer:
                timer_ui['frame'].destroy()
                self.timer_frames.remove(timer_ui)
                break
    
    def timer_callback(self, timer, finished=False):
        if finished:
            # 顯示完成對話框
            self.root.after(0, lambda: messagebox.showinfo("時間到!", f"計時器 '{timer.name}' 倒數完成!"))
    
    def update_display(self):
        # 更新所有計時器的顯示
        for timer_ui in self.timer_frames:
            timer = timer_ui['timer']
            timer_ui['time_label'].config(text=timer.get_time_string())
            
            # 更新狀態
            if timer.is_running:
                if timer.is_paused:
                    status = "已暫停"
                    color = '#FF9800'
                else:
                    status = "運行中"
                    color = '#4CAF50'
            else:
                if timer.remaining_seconds <= 0:
                    status = "已完成"
                    color = '#f44336'
                else:
                    status = "待機"
                    color = '#666'
            
            timer_ui['status_label'].config(text=status, fg=color)
            
            # 時間快到時改變顏色
            if timer.remaining_seconds <= 10 and timer.is_running and not timer.is_paused:
                timer_ui['time_label'].config(fg='#f44336')
            elif timer.remaining_seconds <= 60 and timer.is_running and not timer.is_paused:
                timer_ui['time_label'].config(fg='#FF9800')
            else:
                timer_ui['time_label'].config(fg='#2196F3')
        
        # 每秒更新一次
        self.root.after(1000, self.update_display)

def main():
    root = tk.Tk()
    app = CountdownApp(root)
    
    def on_closing():
        # 停止所有計時器
        for timer in app.timers:
            timer.stop()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()