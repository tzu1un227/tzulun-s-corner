import requests
import json
import hashlib
import hmac
import base64
import time
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    """配置類"""
    webhook_url: str = "https://irl-svr.ee.yzu.edu.tw:5013/bot1/callback"
    channel_secret: str = "dcec13a765291ac6495ef28147ce21d4"
    default_user_id: str = "U6d82c4b234135c5f0a2af724e81cf089"
    message_delay: float = 2.0
    stress_test_count: int = 10
    stress_test_delay: float = 0.5
    timeout: int = 30

class LineMessageSimulator:
    def __init__(self, config: Config):
        self.config = config
        self._message_counter = 0  # 避免時間戳重複
        
    def _get_unique_timestamp(self) -> int:
        """獲取唯一時間戳"""
        timestamp = int(time.time() * 1000)
        self._message_counter += 1
        return timestamp + self._message_counter
    
    def _create_signature(self, body: str) -> Optional[str]:
        """建立 LINE 簽名"""
        if not self.config.channel_secret:
            return None
            
        signature = hmac.new(
            self.config.channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        return base64.b64encode(signature).decode('utf-8')
    
    def _create_payload(self, user_id: str, message_text: str) -> str:
        """建立 webhook payload"""
        timestamp = self._get_unique_timestamp()
        
        payload = {
            "destination": "your_bot_basic_id",
            "events": [{
                "type": "message",
                "mode": "active",
                "timestamp": timestamp,
                "source": {"type": "user", "userId": user_id},
                "webhookEventId": f"webhook_event_{timestamp}",
                "deliveryContext": {"isRedelivery": False},
                "message": {
                    "id": f"message_{timestamp}",
                    "type": "text",
                    "quoteToken": f"quote_{timestamp}",
                    "text": message_text
                },
                "replyToken": f"reply_token_{timestamp}"
            }]
        }
        
        return json.dumps(payload, separators=(',', ':'))
    
    def send_message(self, user_id: str, message_text: str) -> Optional[requests.Response]:
        """發送單一訊息"""
        body = self._create_payload(user_id, message_text)
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'LineBotSdk/1.0'
        }
        
        if self.config.channel_secret:
            signature = self._create_signature(body)
            if signature:
                headers['X-Line-Signature'] = signature
        
        try:
            response = requests.post(
                self.config.webhook_url,
                data=body,
                headers=headers,
                timeout=self.config.timeout
            )
            
            print(f"✅ 訊息發送 {'成功' if response.status_code == 200 else '失敗'}")
            print(f"📤 內容: {message_text}")
            print(f"👤 用戶: {user_id}")
            print(f"🌐 狀態: {response.status_code}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 發送失敗: {e}")
            return None
    
    def send_multiple_messages(self, messages: List[str], user_id: str, delay: float) -> dict:
        """發送多個訊息並返回統計"""
        print(f"🚀 開始發送 {len(messages)} 個訊息...")
        
        stats = {"success": 0, "failed": 0, "start_time": time.time()}
        
        for i, message in enumerate(messages, 1):
            print(f"\n--- 第 {i}/{len(messages)} 個訊息 ---")
            response = self.send_message(user_id, message)
            
            if response and response.status_code == 200:
                stats["success"] += 1
            else:
                stats["failed"] += 1
                
            if i < len(messages):
                time.sleep(delay)
        
        stats["end_time"] = time.time()
        stats["total_time"] = stats["end_time"] - stats["start_time"]
        
        print(f"\n🎉 發送完成! 成功: {stats['success']}, 失敗: {stats['failed']}")
        return stats
    
    def stress_test(self, count: int, user_id: str, message_template: str, delay: float) -> dict:
        """壓力測試"""
        messages = [message_template.format(count=i) for i in range(1, count + 1)]
        
        print(f"🚨 壓力測試開始: {count} 個訊息，間隔 {delay} 秒")
        print("=" * 50)
        
        stats = self.send_multiple_messages(messages, user_id, delay)
        
        # 顯示詳細統計
        self._print_stats(stats, count)
        return stats
    
    def _print_stats(self, stats: dict, total_count: int):
        """顯示統計結果"""
        success_rate = stats['success'] / total_count * 100
        avg_time = stats['total_time'] / total_count
        messages_per_sec = total_count / stats['total_time']
        
        print("\n" + "="*50)
        print("📊 測試結果統計")
        print("="*50)
        print(f"✅ 成功: {stats['success']} 個")
        print(f"❌ 失敗: {stats['failed']} 個") 
        print(f"📈 成功率: {success_rate:.1f}%")
        print(f"⏱️ 總耗時: {stats['total_time']:.2f} 秒")
        print(f"📊 平均時間: {avg_time:.2f} 秒/個")
        print(f"🚀 發送速率: {messages_per_sec:.2f} 個/秒")
        print("="*50)

class SimulatorUI:
    def __init__(self, simulator: LineMessageSimulator, config: Config):
        self.simulator = simulator
        self.config = config
        
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """獲取用戶輸入，支持預設值"""
        user_input = input(f"{prompt} (預設: {default}): ").strip()
        return user_input if user_input else default
    
    def get_number_input(self, prompt: str, default: float, min_val: float = 0) -> float:
        """獲取數字輸入，帶驗證"""
        while True:
            try:
                user_input = input(f"{prompt} (預設: {default}): ").strip()
                if not user_input:
                    return default
                value = float(user_input)
                if value < min_val:
                    print(f"❌ 值必須 >= {min_val}")
                    continue
                return value
            except ValueError:
                print("❌ 請輸入有效數字")
    
    def confirm_action(self, message: str) -> bool:
        """確認操作"""
        response = input(f"{message} (y/n): ").strip().lower()
        return response in ['y', 'yes', '是']
    
    def run_single_test(self):
        """單一訊息測試"""
        print("\n=== 📤 單一訊息測試 ===")
        user_id = self.get_user_input("👤 使用者ID", self.config.default_user_id)
        message = input("📝 訊息內容: ").strip()
        
        if not message:
            print("❌ 訊息不能為空!")
            return
            
        self.simulator.send_message(user_id, message)
    
    def run_multiple_test(self):
        """多訊息測試"""
        print("\n=== 📤 多訊息測試 ===")
        user_id = self.get_user_input("👤 使用者ID", self.config.default_user_id)
        
        messages = []
        print("📝 輸入訊息內容 (空行結束):")
        while True:
            message = input(f"訊息 {len(messages)+1}: ").strip()
            if not message:
                break
            messages.append(message)
        
        if not messages:
            print("❌ 至少需要一個訊息!")
            return
        
        delay = self.get_number_input("⏱️ 間隔時間(秒)", self.config.message_delay)
        self.simulator.send_multiple_messages(messages, user_id, delay)
    
    def run_stress_test(self):
        """壓力測試"""
        print("\n=== 🚨 壓力測試 ===")
        print("⚠️ 警告: 此模式會連續發送大量訊息!")
        
        if not self.confirm_action("確定要進行壓力測試嗎？"):
            return
        
        count = int(self.get_number_input("發送次數", self.config.stress_test_count, 1))
        delay = self.get_number_input("間隔時間(秒)", self.config.stress_test_delay)
        user_id = self.get_user_input("使用者ID", self.config.default_user_id)
        template = self.get_user_input("訊息模板 ({count}會被替換)", "壓力測試訊息 #{count}")
        
        print(f"\n🎯 測試參數: {count}個訊息, 間隔{delay}秒")
        if not self.confirm_action("開始測試？"):
            return
        
        self.simulator.stress_test(count, user_id, template, delay)
    
    def show_settings(self):
        """顯示設定"""
        print("\n📋 當前設定:")
        print(f"🌐 Webhook URL: {self.config.webhook_url}")
        print(f"🔐 Channel Secret: {'已設定' if self.config.channel_secret else '未設定'}")
        print(f"👤 預設用戶ID: {self.config.default_user_id}")
        print(f"⏱️ 訊息間隔: {self.config.message_delay}秒")
        print(f"🚨 壓力測試設定: {self.config.stress_test_count}個, 間隔{self.config.stress_test_delay}秒")
    
    def run(self):
        """主程式迴圈"""
        menu_options = {
            "1": ("發送單一測試訊息", self.run_single_test),
            "2": ("發送多個測試訊息", self.run_multiple_test), 
            "3": ("壓力測試模式 🚨", self.run_stress_test),
            "4": ("顯示當前設定", self.show_settings),
            "0": ("退出程式", None)
        }
        
        while True:
            print("\n" + "="*50)
            print("📱 LINE Bot 訊息模擬器")
            print("="*50)
            
            for key, (desc, _) in menu_options.items():
                print(f"{key}. {desc}")
            
            print("="*50)
            
            try:
                choice = input("請選擇功能: ").strip()
                
                if choice == "0":
                    print("👋 再見!")
                    break
                elif choice in menu_options:
                    menu_options[choice][1]()
                    if choice != "4":  # 設定頁面不需要等待
                        input("\n按 Enter 繼續...")
                else:
                    print("❌ 無效選項!")
                    
            except KeyboardInterrupt:
                print("\n👋 程式中斷!")
                break
            except Exception as e:
                print(f"❌ 錯誤: {e}")

def main():
    # 建立配置 (可以從檔案或環境變數載入)
    config = Config()
    
    # 建立模擬器和UI
    simulator = LineMessageSimulator(config)
    ui = SimulatorUI(simulator, config)
    
    # 執行程式
    ui.run()

if __name__ == "__main__":
    main()