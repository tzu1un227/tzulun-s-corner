"""
1A2B 裁判評判助手 (Bulls and Cows Judge)
功能：
1. 讓出題者設定 4 位不重複謎底（支援遮蔽防偷看、隨機生成題目）。
2. 輸入他人回答的猜測數字，程式自動且精準計算出 ?A ?B。
3. 歷史紀錄表格即時更新，支援一鍵複製紀錄、重複猜測提示、獲勝提示音。
4. 同時支援視窗圖形介面 (Tkinter GUI，預設) 與 終端機命令列模式 (--cli)。
"""

import sys
import os
import random
import time
from datetime import datetime

# 嘗試啟用 Windows 高 DPI 縮放以保持清晰字體
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class Game1A2B:
    """1A2B 核心規則與判定邏輯"""

    @staticmethod
    def validate_number(s: str) -> tuple[bool, str]:
        """驗證是否為合格的 4 位不重複數字"""
        s = s.strip()
        if len(s) != 4:
            return False, f"必須是 4 位數字（您輸入了 {len(s)} 位）！"
        if not s.isdigit():
            return False, "只能包含數字 0~9，不能含有其他符號或英文字母！"
        if len(set(s)) != 4:
            seen = set()
            duplicates = [ch for ch in s if ch in seen or seen.add(ch)]
            return False, f"數字不能重複！重複的數字：{', '.join(set(duplicates))}"
        return True, ""

    @staticmethod
    def calculate_ab(secret: str, guess: str) -> tuple[int, int]:
        """計算 A 與 B 的數量"""
        a = sum(1 for s, g in zip(secret, guess) if s == g)
        b = len(set(secret) & set(guess)) - a
        return a, b

    @staticmethod
    def generate_random_secret() -> str:
        """隨機生成 4 位不重複數字"""
        digits = list("0123456789")
        random.shuffle(digits)
        return "".join(digits[:4])


# ==========================================
# 圖形化介面 (Tkinter GUI)
# ==========================================
def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    try:
        import winsound
    except ImportError:
        winsound = None

    class GameApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("🎯 1A2B 裁判助手 - 自動精準判定防看錯")
            self.geometry("620x760")
            self.minsize(560, 680)
            self.configure(bg="#f1f5f9")

            # 狀態變數
            self.secret_code = ""
            self.is_secret_locked = False
            self.history = []  # list of dicts: {'round': int, 'guess': str, 'a': int, 'b': int, 'time': str}
            self.is_game_won = False

            # 設定主題樣式
            self.setup_styles()

            # 建立畫面元件
            self.create_widgets()

            # 綁定全域快捷鍵
            self.bind("<Control-n>", lambda e: self.new_game())

        def setup_styles(self):
            self.style = ttk.Style(self)
            self.style.theme_use("clam")

            # 字體設定
            self.font_title = ("Microsoft JhengHei UI", 16, "bold")
            self.font_subtitle = ("Microsoft JhengHei UI", 9)
            self.font_section = ("Microsoft JhengHei UI", 11, "bold")
            self.font_body = ("Microsoft JhengHei UI", 10)
            self.font_body_bold = ("Microsoft JhengHei UI", 10, "bold")
            self.font_big_input = ("Consolas", 18, "bold")
            self.font_result_badge = ("Microsoft JhengHei UI", 20, "bold")

            # 按鈕樣式
            self.style.configure(
                "Primary.TButton",
                font=self.font_body_bold,
                padding=6,
                background="#2563eb",
                foreground="#ffffff",
                borderwidth=0
            )
            self.style.map("Primary.TButton", background=[("active", "#1d4ed8")])

            self.style.configure(
                "Success.TButton",
                font=self.font_body_bold,
                padding=6,
                background="#10b981",
                foreground="#ffffff",
                borderwidth=0
            )
            self.style.map("Success.TButton", background=[("active", "#059669")])

            self.style.configure(
                "Secondary.TButton",
                font=self.font_body,
                padding=5,
                background="#e2e8f0",
                foreground="#1e293b",
                borderwidth=0
            )
            self.style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

            # 表格樣式
            self.style.configure(
                "Treeview",
                font=("Consolas", 11),
                rowheight=30,
                background="#ffffff",
                fieldbackground="#ffffff",
                foreground="#1e293b"
            )
            self.style.configure(
                "Treeview.Heading",
                font=self.font_body_bold,
                padding=5,
                background="#e2e8f0",
                foreground="#0f172a"
            )
            self.style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e3a8a")])

        def create_widgets(self):
            # 主容器
            main_container = tk.Frame(self, bg="#f1f5f9", padx=16, pady=14)
            main_container.pack(fill="both", expand=True)

            # 1. 頂部標題列
            header_frame = tk.Frame(main_container, bg="#f1f5f9")
            header_frame.pack(fill="x", pady=(0, 10))

            title_label = tk.Label(
                header_frame,
                text="🎯 1A2B 裁判評判助手",
                font=self.font_title,
                bg="#f1f5f9",
                fg="#0f172a"
            )
            title_label.pack(anchor="w")

            subtitle_label = tk.Label(
                header_frame,
                text="你設定謎底、輸入對手猜測，由程式精準判定幾 A 幾 B，免除人眼看錯的困擾！",
                font=self.font_subtitle,
                bg="#f1f5f9",
                fg="#64748b"
            )
            subtitle_label.pack(anchor="w")

            # 2. 謎底設定卡片
            secret_card = tk.LabelFrame(
                main_container,
                text="  第一步：設定謎底答案 (4 位不重複數字)  ",
                font=self.font_section,
                bg="#ffffff",
                fg="#1e293b",
                padx=14,
                pady=10,
                relief="groove",
                bd=1
            )
            secret_card.pack(fill="x", pady=(0, 10))

            secret_input_row = tk.Frame(secret_card, bg="#ffffff")
            secret_input_row.pack(fill="x", pady=2)

            tk.Label(secret_input_row, text="謎底：", font=self.font_body_bold, bg="#ffffff", fg="#334155").pack(side="left")

            self.secret_entry = tk.Entry(
                secret_input_row,
                font=self.font_big_input,
                width=8,
                show="*",
                justify="center",
                relief="solid",
                bd=1,
                bg="#f8fafc"
            )
            self.secret_entry.pack(side="left", padx=(0, 8))
            self.secret_entry.bind("<Return>", lambda e: self.set_secret())

            self.show_secret_var = tk.BooleanVar(value=False)
            self.show_secret_cb = tk.Checkbutton(
                secret_input_row,
                text="顯示明碼",
                font=self.font_body,
                variable=self.show_secret_var,
                command=self.toggle_show_secret,
                bg="#ffffff",
                activebackground="#ffffff",
                fg="#475569"
            )
            self.show_secret_cb.pack(side="left", padx=(0, 10))

            self.set_secret_btn = ttk.Button(
                secret_input_row,
                text="🔒 鎖定答案",
                style="Primary.TButton",
                command=self.set_secret
            )
            self.set_secret_btn.pack(side="left", padx=4)

            self.random_secret_btn = ttk.Button(
                secret_input_row,
                text="🎲 隨機產生",
                style="Secondary.TButton",
                command=self.generate_random_secret
            )
            self.random_secret_btn.pack(side="left", padx=4)

            self.unlock_secret_btn = ttk.Button(
                secret_input_row,
                text="🔓 修改答案",
                style="Secondary.TButton",
                command=self.unlock_secret,
                state="disabled"
            )
            self.unlock_secret_btn.pack(side="left", padx=4)

            # 謎底狀態提示
            self.secret_status_label = tk.Label(
                secret_card,
                text="⚠️ 尚未設定謎底，請先輸入 4 位不重複數字並點擊「鎖定答案」",
                font=self.font_body,
                bg="#ffffff",
                fg="#dc2626"
            )
            self.secret_status_label.pack(anchor="w", pady=(6, 0))

            # 3. 猜測輸入與即時判定卡片
            guess_card = tk.LabelFrame(
                main_container,
                text="  第二步：輸入別人猜測的答案並判定  ",
                font=self.font_section,
                bg="#ffffff",
                fg="#1e293b",
                padx=14,
                pady=10,
                relief="groove",
                bd=1
            )
            guess_card.pack(fill="x", pady=(0, 10))

            guess_input_row = tk.Frame(guess_card, bg="#ffffff")
            guess_input_row.pack(fill="x", pady=2)

            tk.Label(guess_input_row, text="輸入猜測：", font=self.font_body_bold, bg="#ffffff", fg="#334155").pack(side="left")

            self.guess_entry = tk.Entry(
                guess_input_row,
                font=self.font_big_input,
                width=10,
                justify="center",
                relief="solid",
                bd=1,
                bg="#f8fafc",
                state="disabled"
            )
            self.guess_entry.pack(side="left", padx=(0, 10))
            self.guess_entry.bind("<Return>", lambda e: self.submit_guess())

            self.submit_guess_btn = ttk.Button(
                guess_input_row,
                text="判定 (Enter ↵)",
                style="Success.TButton",
                command=self.submit_guess,
                state="disabled"
            )
            self.submit_guess_btn.pack(side="left", padx=4)

            self.guess_tip_label = tk.Label(
                guess_input_row,
                text="💡 輸入 4 位數字後按 Enter 即可快速送出",
                font=self.font_subtitle,
                bg="#ffffff",
                fg="#64748b"
            )
            self.guess_tip_label.pack(side="left", padx=8)

            # 即時判定結果大看板
            self.result_banner_frame = tk.Frame(guess_card, bg="#f8fafc", relief="solid", bd=1, padx=12, pady=10)
            self.result_banner_frame.pack(fill="x", pady=(8, 2))

            self.result_text_label = tk.Label(
                self.result_banner_frame,
                text="等待輸入猜測中...",
                font=self.font_result_badge,
                bg="#f8fafc",
                fg="#475569"
            )
            self.result_text_label.pack()

            self.result_subtext_label = tk.Label(
                self.result_banner_frame,
                text="鎖定謎底後即可開始判定對手猜測",
                font=self.font_body,
                bg="#f8fafc",
                fg="#64748b"
            )
            self.result_subtext_label.pack(pady=(2, 0))

            # 4. 歷史紀錄表格卡片
            history_card = tk.LabelFrame(
                main_container,
                text="  歷史猜測紀錄清單  ",
                font=self.font_section,
                bg="#ffffff",
                fg="#1e293b",
                padx=12,
                pady=8,
                relief="groove",
                bd=1
            )
            history_card.pack(fill="both", expand=True)

            # 表格控制工具列
            history_toolbar = tk.Frame(history_card, bg="#ffffff")
            history_toolbar.pack(fill="x", pady=(0, 6))

            self.round_count_label = tk.Label(
                history_toolbar,
                text="目前已猜測：0 次",
                font=self.font_body_bold,
                bg="#ffffff",
                fg="#1e293b"
            )
            self.round_count_label.pack(side="left")

            ttk.Button(
                history_toolbar,
                text="📋 複製全部紀錄",
                style="Secondary.TButton",
                command=self.copy_history_to_clipboard
            ).pack(side="right", padx=(4, 0))

            ttk.Button(
                history_toolbar,
                text="🔄 清空本局紀錄",
                style="Secondary.TButton",
                command=self.clear_history
            ).pack(side="right", padx=(4, 0))

            ttk.Button(
                history_toolbar,
                text="🆕 開啟新局",
                style="Secondary.TButton",
                command=self.new_game
            ).pack(side="right", padx=(4, 0))

            # Treeview 表格 + Scrollbar
            table_container = tk.Frame(history_card, bg="#ffffff")
            table_container.pack(fill="both", expand=True)

            columns = ("round", "guess", "result", "status", "time")
            self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

            self.tree.heading("round", text="輪次")
            self.tree.heading("guess", text="猜測數字")
            self.tree.heading("result", text="判定結果")
            self.tree.heading("status", text="說明")
            self.tree.heading("time", text="時間")

            self.tree.column("round", width=60, anchor="center")
            self.tree.column("guess", width=120, anchor="center")
            self.tree.column("result", width=130, anchor="center")
            self.tree.column("status", width=110, anchor="center")
            self.tree.column("time", width=90, anchor="center")

            # 滾動條
            scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)

            self.tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # 表格標籤顏色
            self.tree.tag_configure("win", background="#dcfce7", foreground="#166534")
            self.tree.tag_configure("even", background="#f8fafc")
            self.tree.tag_configure("odd", background="#ffffff")

            # 預設焦點放到謎底輸入框
            self.secret_entry.focus()

        # ==================== 事件處理 ====================

        def toggle_show_secret(self):
            if self.show_secret_var.get():
                self.secret_entry.configure(show="")
            else:
                self.secret_entry.configure(show="*")

        def generate_random_secret(self):
            if self.is_secret_locked:
                if not messagebox.askyesno("更換謎底", "目前遊戲已鎖定謎底，確定要隨機產生新題目嗎？\n這將會重置目前的猜測紀錄！"):
                    return
                self.clear_history()

            code = Game1A2B.generate_random_secret()
            self.secret_entry.delete(0, tk.END)
            self.secret_entry.insert(0, code)
            self.set_secret()

        def set_secret(self):
            raw_secret = self.secret_entry.get().strip()
            valid, err_msg = Game1A2B.validate_number(raw_secret)
            if not valid:
                messagebox.showwarning("謎底格式錯誤", f"無法設定謎底：\n{err_msg}")
                self.secret_entry.focus()
                return

            self.secret_code = raw_secret
            self.is_secret_locked = True

            # 更新 UI 狀態
            self.secret_entry.configure(state="disabled")
            self.set_secret_btn.configure(state="disabled")
            self.unlock_secret_btn.configure(state="normal")
            display_str = self.secret_code if self.show_secret_var.get() else "****"
            self.secret_status_label.configure(
                text=f"✅ 謎底已成功鎖定 [{display_str}]，請在下方輸入對手猜測進行判定！",
                fg="#16a34a"
            )

            # 啟用猜測輸入區
            self.guess_entry.configure(state="normal")
            self.submit_guess_btn.configure(state="normal")
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus()

            self.update_result_banner("等待輸入猜測...", "請在上方輸入 4 位猜測數字後按 Enter", "#f8fafc", "#475569")

        def unlock_secret(self):
            if self.history and not self.is_game_won:
                if not messagebox.askyesno("修改謎底確認", "目前已記錄猜測歷程，修改謎底可能導致先前的判定不正確。\n確定要解鎖並修改謎底嗎？"):
                    return

            self.is_secret_locked = False
            self.secret_entry.configure(state="normal")
            self.set_secret_btn.configure(state="normal")
            self.unlock_secret_btn.configure(state="disabled")
            self.secret_status_label.configure(
                text="✏️ 請修改謎底後，點擊「鎖定答案」以重新啟用判定",
                fg="#ea580c"
            )

            self.guess_entry.configure(state="disabled")
            self.submit_guess_btn.configure(state="disabled")
            self.secret_entry.focus()

        def submit_guess(self):
            if not self.is_secret_locked:
                messagebox.showwarning("提示", "請先設定並鎖定謎底答案！")
                self.secret_entry.focus()
                return

            guess = self.guess_entry.get().strip()
            valid, err_msg = Game1A2B.validate_number(guess)
            if not valid:
                messagebox.showwarning("猜測格式錯誤", f"無法判定此數字：\n{err_msg}")
                self.guess_entry.select_range(0, tk.END)
                self.guess_entry.focus()
                return

            # 檢查是否重複猜過
            past_rounds = [item['round'] for item in self.history if item['guess'] == guess]
            note = ""
            if past_rounds:
                note = f"第 {past_rounds[0]} 輪已猜過"

            # 計算幾 A 幾 B
            a, b = Game1A2B.calculate_ab(self.secret_code, guess)
            round_no = len(self.history) + 1
            now_str = datetime.now().strftime("%H:%M:%S")

            record = {
                'round': round_no,
                'guess': guess,
                'a': a,
                'b': b,
                'time': now_str,
                'note': note
            }
            self.history.append(record)

            # 新增至表格
            tag = "win" if a == 4 else ("even" if round_no % 2 == 0 else "odd")
            status_text = "🎉 答對了！" if a == 4 else (note if note else "—")
            self.tree.insert(
                "",
                "end",
                values=(f"第 {round_no} 次", guess, f"{a}A {b}B", status_text, now_str),
                tags=(tag,)
            )

            # 自動捲動到最底
            children = self.tree.get_children()
            if children:
                self.tree.see(children[-1])

            # 更新次數
            self.round_count_label.configure(text=f"目前已猜測：{round_no} 次")

            # 更新判定看板
            if a == 4:
                self.is_game_won = True
                self.update_result_banner(
                    f"🎉 4A 0B 答對了！",
                    f"恭喜對手在第 {round_no} 次成功猜中謎底 [{self.secret_code}]！",
                    "#dcfce7",
                    "#15803d"
                )
                # 播放慶祝音效
                if winsound:
                    try:
                        winsound.MessageBeep(winsound.MB_ICONASTERISK)
                    except Exception:
                        pass
                messagebox.showinfo("答對了！", f"🎉 太棒了！在第 {round_no} 次猜出 4A 0B 成功過關！")
            else:
                extra_warning = f" (⚠️ 注意：{note})" if note else ""
                self.update_result_banner(
                    f"👉 {a} A  {b} B",
                    f"第 {round_no} 次猜測 [{guess}] 判定結果{extra_warning}",
                    "#eff6ff",
                    "#1d4ed8"
                )

            # 清空猜測輸入框，方便下一次快速輸入
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus()

        def update_result_banner(self, main_text: str, sub_text: str, bg_color: str, fg_color: str):
            self.result_banner_frame.configure(bg=bg_color)
            self.result_text_label.configure(text=main_text, bg=bg_color, fg=fg_color)
            self.result_subtext_label.configure(text=sub_text, bg=bg_color)

        def clear_history(self):
            if not self.history:
                return
            if messagebox.askyesno("清空紀錄確認", "確定要清空本局的所有猜測紀錄嗎？（謎底仍會保留）"):
                self.history.clear()
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.round_count_label.configure(text="目前已猜測：0 次")
                self.is_game_won = False
                self.update_result_banner("紀錄已清空", "請繼續輸入猜測數字開始判定", "#f8fafc", "#475569")
                self.guess_entry.focus()

        def new_game(self):
            if self.history or self.is_secret_locked:
                if not messagebox.askyesno("開新局確認", "確定要開啟全新一局嗎？這將會重置謎底與所有紀錄！"):
                    return

            self.history.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.round_count_label.configure(text="目前已猜測：0 次")
            self.is_secret_locked = False
            self.is_game_won = False
            self.secret_code = ""

            self.secret_entry.configure(state="normal")
            self.secret_entry.delete(0, tk.END)
            self.set_secret_btn.configure(state="normal")
            self.unlock_secret_btn.configure(state="disabled")
            self.secret_status_label.configure(
                text="⚠️ 尚未設定謎底，請先輸入 4 位不重複數字並點擊「鎖定答案」",
                fg="#dc2626"
            )

            self.guess_entry.delete(0, tk.END)
            self.guess_entry.configure(state="disabled")
            self.submit_guess_btn.configure(state="disabled")

            self.update_result_banner("新遊戲已就緒", "請先於上方設定 4 位謎底答案", "#f8fafc", "#475569")
            self.secret_entry.focus()

        def copy_history_to_clipboard(self):
            if not self.history:
                messagebox.showinfo("提示", "目前尚無猜測紀錄可複製！")
                return

            lines = ["【1A2B 猜測歷程紀錄】"]
            secret_disp = self.secret_code if self.show_secret_var.get() else "****"
            lines.append(f"謎底：{secret_disp}")
            lines.append("-" * 32)
            lines.append("輪次\t猜測\t結果\t狀態\t時間")
            for h in self.history:
                note_str = f"({h['note']})" if h.get('note') else ("WIN" if h['a'] == 4 else "")
                lines.append(f"第 {h['round']} 次\t{h['guess']}\t{h['a']}A{h['b']}B\t{note_str}\t{h['time']}")
            lines.append("-" * 32)
            lines.append(f"總猜測次數：{len(self.history)} 次")

            clipboard_text = "\n".join(lines)
            self.clipboard_clear()
            self.clipboard_append(clipboard_text)
            messagebox.showinfo("複製成功", "猜測紀錄已成功複製到剪貼簿！可直接貼到 LINE、記事本或聊天室。")

    app = GameApp()
    app.mainloop()


# ==========================================
# 終端機命令列模式 (CLI)
# ==========================================
def run_cli():
    """在終端機內進行互動評判"""
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 50)
    print("       🎯 1A2B 裁判評判助手 (命令列 CLI 模式)")
    print("=" * 50)
    print("說明：由您輸入謎底答案，隨後輸入對手的猜測，自動精準評判幾A幾B。")
    print("-" * 50)

    # 1. 輸入謎底
    while True:
        prompt = "請輸入 4 位不重複謎底數字 (輸入 r 可隨機出題): "
        secret = input(prompt).strip()
        if secret.lower() == "r":
            secret = Game1A2B.generate_random_secret()
            print(f"🎲 已為您隨機產生謎底：{secret}")
            confirm = input("確認使用此謎底？(Y/n): ").strip().lower()
            if confirm not in ("", "y", "yes"):
                continue
        valid, msg = Game1A2B.validate_number(secret)
        if valid:
            break
        print(f"❌ 錯誤：{msg}\n")

    # 清空畫面防止偷看
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 50)
    print("  ✅ 謎底已設定完成！遊戲開始！")
    print("  (輸入 q 可退出，輸入 r 可查看已猜紀錄，輸入 s 可重溫答案)")
    print("=" * 50)

    history = []
    round_no = 0

    while True:
        round_no += 1
        guess = input(f"\n[第 {round_no} 輪] 請輸入猜測數字 > ").strip()

        if guess.lower() == "q":
            print("\n遊戲已提前結束。")
            print(f"謎底答案是：{secret}")
            break
        elif guess.lower() == "s":
            round_no -= 1
            print(f"🔒 謎底答案為：{secret}")
            continue
        elif guess.lower() == "r":
            round_no -= 1
            if not history:
                print("尚無猜測紀錄。")
            else:
                print("\n--- 歷史紀錄 ---")
                for item in history:
                    print(f"第 {item['round']} 次: {item['guess']} -> {item['a']}A {item['b']}B")
                print("----------------")
            continue

        valid, msg = Game1A2B.validate_number(guess)
        if not valid:
            print(f"❌ 輸入無效：{msg}")
            round_no -= 1
            continue

        # 檢查是否重複猜過
        prev_rounds = [item['round'] for item in history if item['guess'] == guess]
        if prev_rounds:
            print(f"⚠️ 注意：此數字在第 {prev_rounds[0]} 輪已經猜過囉！")

        a, b = Game1A2B.calculate_ab(secret, guess)
        history.append({'round': round_no, 'guess': guess, 'a': a, 'b': b})

        print(f"👉 判定結果：【 {a} A  {b} B 】")

        if a == 4:
            print("\n" + "★" * 50)
            print(f"🎉 恭喜！答對了！4A 0B！在第 {round_no} 輪成功猜中！")
            print(f"謎底是：{secret}")
            print("★" * 50)
            break


# ==========================================
# 程式入口點
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--cli", "-c", "cli"):
        run_cli()
    else:
        # 預設啟動視窗圖形介面 (GUI)
        run_gui()
