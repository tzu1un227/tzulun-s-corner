import requests
import json
import hashlib
import hmac
import base64
from datetime import datetime
import time

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
SINGLE_TEST_MESSAGE = "123"

MULTIPLE_TEST_MESSAGES = [
    "1",
    "2", 
    "3",
    "4"
]

# 多個訊息間隔時間（秒）
MESSAGE_DELAY = 2

# ==============================================


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


def display_menu():
    """顯示選單"""
    print("=" * 50)
    print("📱 LINE Bot 訊息模擬器")
    print("=" * 50)
    print("1. 發送單一測試訊息")
    print("2. 發送多個測試訊息")
    print("3. 自訂單一訊息")
    print("4. 顯示當前設定")
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

def main():
    # 建立模擬器實例
    simulator = LineMessageSimulator(WEBHOOK_URL, CHANNEL_SECRET)
    
    while True:
        display_menu()
        
        try:
            choice = input("請選擇功能 (0-4): ").strip()
            
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
                display_settings()
            else:
                print("❌ 無效選項，請重新選擇!")
                
        except KeyboardInterrupt:
            print("\n👋 程式被中斷，再見!")
            break
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
        
        # 等待使用者按鍵繼續
        if choice in ["1", "2", "3"]:
            input("\n按 Enter 鍵繼續...")
        
        print()  # 空行分隔

if __name__ == "__main__":
    main()