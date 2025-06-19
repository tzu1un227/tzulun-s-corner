import pyautogui
import threading
import keyboard
import time

clicking = False  # 是否正在連點
interval = 0.05   # 點擊間隔（秒）

def click_loop():
    while True:
        if clicking:
            pyautogui.click()
            time.sleep(interval)

def toggle_clicking():
    global clicking
    clicking = not clicking
    print("連點啟動" if clicking else "連點停止")

# 開啟點擊執行緒
threading.Thread(target=click_loop, daemon=True).start()

# 監聽 F8 鍵做啟動/停止
print("按下 F8 開啟或停止連點，按下 ESC 離開程式")
keyboard.add_hotkey('F8', toggle_clicking)
keyboard.wait('esc')
