import paho.mqtt.client as paho
import time
import ssl
import sys

# =================================================================
# 1. Broker 連線資訊 (請根據您的 HiveMQ Cloud 資訊修改)
# =================================================================
HOST = "5714042bef9b4763959e0df544869cf4.s1.eu.hivemq.cloud" # 您的 Broker 主機名稱
PORT = 8883                                                 # HiveMQ Cloud 預設使用 8883 進行 TLS 安全連線
TOPIC = "TLtest"                                 # 您要發布到的主題 (Topic)
CLIENT_ID = f"PythonPublisher_{int(time.time())}"           # 客戶端 ID (建議使用唯一 ID)

# 驗證資訊
AUTH = {
    'username': "yzuirl", 
    'password': "Yzu70640"
}
# =================================================================

# MQTT 客戶端實例
client = paho.Client(paho.CallbackAPIVersion.VERSION1, CLIENT_ID)

# =================================================================
# 2. 定義回呼函數 (Callbacks)
# =================================================================

def on_connect(client, userdata, flags, rc):
    """連線成功或失敗時的回呼函數"""
    if rc == 0:
        print(f"[INFO] 成功連線到 Broker！(Result Code: {rc})")
        # 連線成功後，您可以選擇在這裡進行訂閱
    elif rc == 5:
        print(f"[ERROR] 連線失敗，請檢查使用者名稱或密碼是否正確！(Result Code: {rc})")
        sys.exit(1) # 連線失敗則退出程式
    else:
        print(f"[ERROR] 連線失敗，Result Code: {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    """發布訊息後的回呼函數"""
    print(f"[INFO] 訊息發布成功！(MID: {mid})")

def on_disconnect(client, userdata, rc):
    """斷開連線時的回呼函數"""
    print(f"[INFO] 已斷開連線 (Result Code: {rc})")

# 設定回呼函數
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
# =================================================================

# =================================================================
# 3. 客戶端初始化與連線
# =================================================================

try:
    # 設定使用者名稱和密碼
    client.username_pw_set(username=AUTH['username'], password=AUTH['password'])
    
    # 啟用 TLS/SSL 安全連線 (因為 port 是 8883)
    # 使用預設的系統 CA 憑證進行伺服器驗證
    print("[INFO] 設定 TLS/SSL...")
    client.tls_set(tls_version=ssl.PROTOCOL_TLS) 
    
    # 連線到 Broker
    print(f"[INFO] 嘗試連線到 {HOST}:{PORT}...")
    client.connect(host=HOST, port=PORT, keepalive=60)
    
    # 啟動網路迴圈，在背景處理連線、重連和訊息收發
    client.loop_start() 
    
    # 等待連線完成。如果連線失敗，on_connect 已經會退出程式。
    time.sleep(2) 
    
except Exception as e:
    print(f"[FATAL] 連線或初始化發生錯誤: {e}")
    sys.exit(1)

# =================================================================
# 4. 發布訊息
# =================================================================

def publish_test_message(topic, message, qos=1):
    """發布訊息的函數"""
    print(f"[INFO] 準備發布訊息到主題: {topic}")
    
    # 發布訊息，QoS 設為 1 (至少一次)
    # client.is_connected() 可以檢查連線狀態，但 loop_start 會處理重連
    if client.is_connected():
        try:
            # payload 必須是 bytes 或 str
            result = client.publish(topic, message, qos=qos)
            # result.rc = paho.MQTT_ERR_SUCCESS (0) 表示成功加入發布佇列
            # result.mid = 訊息 ID (會傳遞給 on_publish 回呼函數)
            print(f"[INFO] 訊息已加入發布佇列。")
        except Exception as e:
            print(f"[ERROR] 發布訊息時發生錯誤: {e}")
    else:
        print("[WARNING] 客戶端尚未連線成功，訊息將在連線後嘗試發送。")

# 您要發布的測試訊息
test_message = "Hello from Python Paho Client! Current time: " + time.strftime("%Y-%m-%d %H:%M:%S")

# 呼叫發布函數
publish_test_message(TOPIC, test_message, 2)

# 給予 Paho 客戶端一些時間來發送訊息並接收 Broker 的確認 (on_publish)
time.sleep(5) 

# 停止網路迴圈並斷開連線
client.loop_stop()
client.disconnect()

print("--- 程式執行結束 ---")