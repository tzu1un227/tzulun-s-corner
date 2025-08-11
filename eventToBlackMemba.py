import requests
import json
import hashlib
import hmac
import base64
from datetime import datetime
import time

class LineMessageSimulator:
    def __init__(self, webhook_url, channel_secret=None):
        """
        初始化 LINE 訊息模擬器
        
        Args:
            webhook_url (str): 你的 LINE Bot webhook URL
            channel_secret (str): LINE Channel Secret (如果需要簽名驗證)
        """
        self.webhook_url = webhook_url
        self.channel_secret = channel_secret
        
    def create_signature(self, body):
        """
        建立 LINE 簽名 (如果伺服器有驗證簽名)
        """
        if not self.channel_secret:
            return None
            
        signature = hmac.new(
            self.channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return base64.b64encode(signature).decode('utf-8')
    
    def send_text_message(self, user_id="test_user_001", message_text="Hello from simulator!"):
        """
        發送文字訊息到 LINE Bot
        
        Args:
            user_id (str): 模擬的使用者 ID
            message_text (str): 要發送的文字訊息
        """
        
        # 建立 LINE webhook 格式的 payload
        timestamp = int(time.time() * 1000)
        
        payload = {
            "destination": "your_bot_basic_id",
            "events": [
                {
                    "type": "message",
                    "mode": "active",
                    "timestamp": timestamp,
                    "source": {
                        "type": "user",
                        "userId": user_id
                    },
                    "webhookEventId": f"webhook_event_{timestamp}",
                    "deliveryContext": {
                        "isRedelivery": False
                    },
                    "message": {
                        "id": f"message_{timestamp}",
                        "type": "text",
                        "quoteToken": f"quote_{timestamp}",
                        "text": message_text
                    },
                    "replyToken": f"reply_token_{timestamp}"
                }
            ]
        }
        
        # 轉換為 JSON 字串
        body = json.dumps(payload, separators=(',', ':'))
        
        # 準備 headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'LineBotSdk/1.0'
        }
        
        # 如果有 channel secret，加上簽名
        if self.channel_secret:
            signature = self.create_signature(body)
            headers['X-Line-Signature'] = signature
        
        try:
            # 發送請求到你的伺服器
            response = requests.post(
                self.webhook_url, 
                data=body, 
                headers=headers,
                timeout=30
            )
            
            print(f"✅ 訊息發送成功!")
            print(f"📤 發送內容: {message_text}")
            print(f"👤 使用者ID: {user_id}")
            print(f"🌐 伺服器回應: {response.status_code}")
            print(f"📋 回應內容: {response.text if response.text else '無內容'}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 發送失敗: {e}")
            return None
    
    def send_multiple_messages(self, messages, user_id="test_user_001", delay=1):
        """
        發送多個訊息
        
        Args:
            messages (list): 訊息列表
            user_id (str): 使用者 ID
            delay (int): 每個訊息間隔秒數
        """
        print(f"🚀 開始發送 {len(messages)} 個訊息...")
        
        for i, message in enumerate(messages, 1):
            print(f"\n--- 第 {i} 個訊息 ---")
            self.send_text_message(user_id, message)
            
            if i < len(messages):  # 不是最後一個訊息才需要等待
                print(f"⏳ 等待 {delay} 秒...")
                time.sleep(delay)
        
        print(f"\n🎉 所有訊息發送完成!")

    def send_stress_test(self, count=10, user_id="stress_test_user", message_template="壓力測試訊息 #{count}", delay=0.5):
        """
        壓力測試 - 連續發送大量訊息
        
        Args:
            count (int): 要發送的訊息數量
            user_id (str): 使用者 ID
            message_template (str): 訊息模板，{count} 會被替換為序號
            delay (float): 每個訊息間隔秒數
        """
        print(f"🚨 開始壓力測試: 發送 {count} 個訊息，間隔 {delay} 秒")
        print(f"👤 使用者ID: {user_id}")
        print(f"📤 訊息模板: {message_template}")
        print("=" * 50)
        
        success_count = 0
        failed_count = 0
        start_time = time.time()
        
        for i in range(1, count + 1):
            message = message_template.replace("{count}", str(i))
            print(f"\n🔥 [{i}/{count}] 發送中...")
            
            response = self.send_text_message(user_id, message)
            
            if response and response.status_code == 200:
                success_count += 1
            else:
                failed_count += 1
            
            # 不是最後一個訊息才需要等待
            if i < count:
                time.sleep(delay)
    
        end_time = time.time()
        total_time = end_time - start_time
    
        # 統計結果
        print("\n" + "="*50)
        print("📊 壓力測試結果統計")
        print("="*50)
        print(f"✅ 成功發送: {success_count} 個")
        print(f"❌ 發送失敗: {failed_count} 個")
        print(f"📈 成功率: {success_count/count*100:.1f}%")
        print(f"⏱️ 總耗時: {total_time:.2f} 秒")
        print(f"📊 平均每個訊息: {total_time/count:.2f} 秒")
        print(f"🚀 每秒發送量: {count/total_time:.2f} 個/秒")
        print("="*50)

# ==============================================
# 全域設定變數 - 請在這裡修改你的設定
# ==============================================

# LINE Bot 伺服器設定
WEBHOOK_URL = "https://irl-svr.ee.yzu.edu.tw:5013/bot1/callback"  # 請替換成你的實際 URL
CHANNEL_SECRET = "dcec13a765291ac6495ef28147ce21d4"  # 如果需要簽名驗證，請替換成你的 Channel Secret

# 測試使用者設定
DEFAULT_USER_ID = "U6d82c4b234135c5f0a2af724e81cf089"
SINGLE_TEST_USER_ID = "U6d82c4b234135c5f0a2af724e81cf089"
MULTIPLE_TEST_USER_ID = "U6d82c4b234135c5f0a2af724e81cf089"

# 測試訊息內容
SINGLE_TEST_MESSAGE = "你好！這是單一測試訊息"

MULTIPLE_TEST_MESSAGES = [
    "第一個測試訊息",
    "第二個測試訊息", 
    "這是第三個訊息",
    "最後一個測試訊息"
]

# 多個訊息間隔時間（秒）
MESSAGE_DELAY = 2

# 壓力測試設定
STRESS_TEST_MESSAGE = "壓力測試訊息 #{count}"
STRESS_TEST_COUNT = 10  # 預設發送次數
STRESS_TEST_DELAY = 0.5  # 壓力測試間隔時間（秒）

# ==============================================

def display_menu():
    """顯示選單"""
    print("=" * 50)
    print("📱 LINE Bot 訊息模擬器")
    print("=" * 50)
    print("1. 發送單一測試訊息")
    print("2. 發送多個測試訊息")
    print("3. 自訂單一訊息")
    print("4. 壓力測試模式 🚨")
    print("5. 顯示當前設定")
    print("0. 退出程式")
    print("=" * 50)

def display_settings():
    """顯示當前設定"""
    print("\n📋 當前設定:")
    print(f"🌐 Webhook URL: {WEBHOOK_URL}")
    print(f"🔐 Channel Secret: {'已設定' if CHANNEL_SECRET else '未設定'}")
    print(f"👤 預設使用者ID: {DEFAULT_USER_ID}")
    print(f"📤 單一測試訊息: {SINGLE_TEST_MESSAGE}")
    print(f"📤 多個測試訊息數量: {len(MULTIPLE_TEST_MESSAGES)} 個")
    print(f"⏱️ 訊息間隔: {MESSAGE_DELAY} 秒")
    print(f"🚨 壓力測試預設次數: {STRESS_TEST_COUNT} 個")
    print(f"⚡ 壓力測試間隔: {STRESS_TEST_DELAY} 秒")

def test_single_message(simulator):
    """測試單一訊息"""
    print("\n=== 📤 測試單一訊息 ===")
    simulator.send_text_message(
        user_id=SINGLE_TEST_USER_ID,
        message_text=SINGLE_TEST_MESSAGE
    )

def test_multiple_messages(simulator):
    """測試多個訊息"""
    print("\n=== 📤 測試多個訊息 ===")
    simulator.send_multiple_messages(
        messages=MULTIPLE_TEST_MESSAGES,
        user_id=MULTIPLE_TEST_USER_ID,
        delay=MESSAGE_DELAY
    )

def custom_single_message(simulator):
    """自訂單一訊息"""
    print("\n=== 📝 自訂單一訊息 ===")
    
    # 輸入自訂內容
    user_id = input(f"👤 輸入使用者ID (預設: {DEFAULT_USER_ID}): ").strip()
    if not user_id:
        user_id = DEFAULT_USER_ID
    
    message_text = input("📝 輸入訊息內容: ").strip()
    if not message_text:
        print("❌ 訊息內容不能為空!")
        return
    
    # 發送訊息
    simulator.send_text_message(
        user_id=user_id,
        message_text=message_text
    )

def stress_test_mode(simulator):
    """壓力測試模式"""
    print("\n=== 🚨 壓力測試模式 ===")
    print("⚠️  警告: 此模式會連續發送大量訊息，請確保你的伺服器能夠處理!")
    
    # 確認是否要繼續
    confirm = input("確定要進行壓力測試嗎？(y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("❌ 取消壓力測試")
        return
    
    print("\n📋 壓力測試設定:")
    
    # 輸入測試參數
    count_input = input(f"發送次數 (預設: {STRESS_TEST_COUNT}): ").strip()
    count = int(count_input) if count_input.isdigit() else STRESS_TEST_COUNT
    
    delay_input = input(f"間隔時間/秒 (預設: {STRESS_TEST_DELAY}): ").strip()
    try:
        delay = float(delay_input) if delay_input else STRESS_TEST_DELAY
    except ValueError:
        delay = STRESS_TEST_DELAY
    
    user_id = input(f"使用者ID (預設: {DEFAULT_USER_ID}): ").strip()
    if not user_id:
        user_id = DEFAULT_USER_ID
    
    message_template = input(f"訊息模板 (預設: {STRESS_TEST_MESSAGE}): ").strip()
    if not message_template:
        message_template = STRESS_TEST_MESSAGE
    
    # 最後確認
    print(f"\n🎯 壓力測試參數:")
    print(f"  📊 發送次數: {count} 個")
    print(f"  ⏱️ 間隔時間: {delay} 秒")
    print(f"  👤 使用者ID: {user_id}")
    print(f"  📝 訊息模板: {message_template}")
    
    final_confirm = input("\n最後確認，開始壓力測試？(y/n): ").strip().lower()
    if final_confirm not in ['y', 'yes', '是']:
        print("❌ 取消壓力測試")
        return
    
    # 開始壓力測試
    simulator.send_stress_test(
        count=count,
        user_id=user_id,
        message_template=message_template,
        delay=delay
    )

def main():
    # 建立模擬器實例
    simulator = LineMessageSimulator(WEBHOOK_URL, CHANNEL_SECRET)
    
    while True:
        display_menu()
        
        try:
            choice = input("請選擇功能 (0-5): ").strip()
            
            if choice == "0":
                print("👋 程式結束，再見!")
                break
            elif choice == "1":
                test_single_message(simulator)
            elif choice == "2":
                test_multiple_messages(simulator)
            elif choice == "3":
                custom_single_message(simulator)
            elif choice == "4":
                stress_test_mode(simulator)
            elif choice == "5":
                display_settings()
            else:
                print("❌ 無效選項，請重新選擇!")
                
        except KeyboardInterrupt:
            print("\n👋 程式被中斷，再見!")
            break
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
        
        # 等待使用者按鍵繼續
        if choice in ["1", "2", "3", "4"]:
            input("\n按 Enter 鍵繼續...")
        
        print()  # 空行分隔

if __name__ == "__main__":
    main()