import json
import time
import random
from threading import Thread
import socketio
from concurrent.futures import ThreadPoolExecutor
import ssl
import logging
import argparse
import sys
import os

# 參數
SOCKET_URL = "https://irl-svr.ee.yzu.edu.tw:5013"
#"https://yzuirl04-4da7252cf07d.herokuapp.com"
MAX_WORKERS = 10
REQUEST_FREQUENCY = 10  # 每秒幾次
BOT_NAME = 'websoc'
APIS = 0  #APIS = [0]
NAMESPACE = f"/{BOT_NAME}"
TIMES=2#發送幾次訊息
SLEEPTIME=0.3


# 日誌方便除錯
logging.basicConfig(level=logging.INFO)

# 建立 socket client + thread pool
sio = socketio.Client(logger=True, engineio_logger=True)
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)



# ---- 正確綁定在 namespace 上的事件 ----
@sio.on('connect', namespace=NAMESPACE)
def on_connect():
    print(f"✅ Connected to namespace {NAMESPACE}")

@sio.on('disconnect', namespace=NAMESPACE)
def on_disconnect():
    print(f"🔌 Disconnected from namespace {NAMESPACE}")

@sio.on('connect_error', namespace=NAMESPACE)
def on_connect_error(event):
    print(f"❌ Connect error on {NAMESPACE}: {event}")

# ---- 隨機事件生成 ----
# def generate_random_event():
#     user = random.choice(USERS)
#     event_type, message = random.choice(MESSAGES)
#     api = random.choice(APIS)
#     return {
#         'type': event_type,
#         'user': user,
#         'message': message,
#         'api_index': api
#     }

# ---- 發送事件 ----
def send_event(event):  
    print(f"🟢 發送事件: {event}") # {'type': 'Message', 'message': 'C卷', 'user': 'U99db7a4f6a9cdf3dd46cf12a813ef557', 'api_index': 0}
    try:
        sio.emit(f'{BOT_NAME}_message', event, namespace=NAMESPACE) 
        print(f"🚀 Sent: {event}") 
    except Exception as e:
        print(f"Emit failed: {e}")

# ---- 定時送出事件 ----
def run_fixed_times(events,times=TIMES): 
    for _ in range(times): 
        for event in events:
            send_event(event)  
            time.sleep(SLEEPTIME)
            if event.get("delay", None) ==0:
                print(f"event={event}")
                #print("⏳ 沒有延遲")
            else:
                print(f"event={event}")  
                print(f"⏳ 特殊延遲 {event['delay']} 秒...")
                time.sleep(int(event['delay']))

#TODO 讀取csv送出
def read_file(filepath):
    event_list = []
    with open(filepath, "r", encoding="utf-8") as f: #utf-8編碼中文不會變亂碼
        for line in f:
            parts = line.strip().split(",") 
            print(f"parts ={parts}") # 拆成3份 maxsplit=2
            if len(parts) in [3,4]:
                event_list.append(parts)  # 直接加到 list
            else:  
                print("檔案沒有被拆成三份一組")     
    return event_list


# 迴圈逐一處理每組訊息
def get_event(index,source,events):
    if index == len(source):
        run_fixed_times(events, TIMES)
        return
    event = {
                "type": source[index][0].lower().capitalize(),
                "message": source[index][1],
                "user": source[index][2],
                "api_index": APIS,
                "delay": 0 if len(source[index])!=4 else source[index][3]
    }                  
    events.append(event)
    print(f"events={events}")
    get_event(index+1,source,events)
     #events=[{'type': 'Message', 'message': 'A卷', 'user': 'U99db7a4f6a9cdf3dd46cf12a813ef557', 'api_index': 0}, {'type': 'Message', 'message': 'B卷', 'user': 'U99db7a4f6a9cdf3dd46cf12a813ef557', 'api_index': 0}]
     


# ---- 主程式 ----+
#TODO 送cmd事件
if __name__ == "__main__":
    events = []
    try:
        # 先建立一次連線
        sio.connect(
            SOCKET_URL,
            namespaces=[NAMESPACE],
            wait_timeout=3,
        )
        print("🟢 已連線至 Socket.IO 伺服器")
       
        #判斷是不是用.bat執行
        #if len(sys.argv) > 2:
            #print("sys.argv[0]",sys.argv[0])

        #用.bat執行
        if len(sys.argv) == 4:
            sys.argv.remove("plugin\\發送測試訊息.py")
            #print(f"sys.argv={sys.argv}") 
            event_list=[sys.argv]
            print(f"event_list={event_list}") #event_list=[['Message', 'A卷', 'U99db7a4f6a9cdf3dd46cf12a813ef557']]
            get_event(0,event_list,events) 

        #判斷是不是用可以用讀檔
        elif len(sys.argv) == 2:
            #print('sys.argv[1]=',sys.argv[1]) #檔案路徑
            if not os.path.exists(sys.argv[1]):
                print(f"這個{sys.argv[1]} 路徑不存在，請確認路徑")   
            event_list=read_file(sys.argv[1])
            print('event_list',event_list) # [['Type', 'Content', 'UserID', 'delaytime'], ['Message', 'A卷', 'U99db7a4f6a9cdf3dd46cf12a813ef557', '2']]
            get_event(1,event_list,events)

        else :
            #
            print(" 格式不正確喔! 範例:python 一次發送單一訊息.py <type> <content> <user-id>")  #type第一個字大寫，content是字串            
    except Exception as e:
        print(f"⚠️ 無法連線至 Socket.IO 伺服器: {e}")
    finally:
        sio.disconnect()
        executor.shutdown(wait=True)