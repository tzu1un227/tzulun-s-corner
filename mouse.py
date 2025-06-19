import pyautogui
import threading
import keyboard
import time

clicking = False
interval = 0.05  # 點擊間隔（可調整速度）

def click_loop():
    while True:
        if clicking:
            pyautogui.click()
        time.sleep(interval)

def toggle_clicking():
    global clicking
    clicking = not clicking
    print("▶️ 連點中..." if clicking else "⏹️ 停止連點")

# 啟動點擊執行緒
threading.Thread(target=click_loop, daemon=True).start()

# 設定熱鍵（可在背景運作）
keyboard.add_hotkey('F8', toggle_clicking)

print("已啟動背景連點器\n🔘 F8 開關連點\n🔚 ESC 離開程式")
keyboard.wait('esc')
