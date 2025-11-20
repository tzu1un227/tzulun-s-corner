import requests
import json
from datetime import datetime, timedelta

# --- 設定您的認證資訊 ---
# 請替換成您的 Channel Access Token
CHANNEL_ACCESS_TOKEN = ""

# Insight API 的基礎 URL
BASE_URL = "https://api.line.me/v2/bot/insight/"

# 請求 Header (包含授權資訊)
HEADERS = {
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_insights_data(endpoint, params=None):
    """
    通用函式：向指定的 Insights API 端點發送 GET 請求。
    """
    url = f"{BASE_URL}{endpoint}"
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status() # 對於非 200 的狀態碼拋出異常
        return response.json()
        
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
             # 有時特定日期的數據尚未產生或無法獲取
             print(f"⚠️ 查詢日期 {params.get('date')} 失敗 (HTTP 404 Not Found), 可能數據尚未產生。")
             return None
        print(f"❌ HTTP 錯誤發生 ({err}): {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"❌ 請求發生錯誤: {err}")
        return None


def generate_custom_date_range(start_date_str, end_date_str):
    """
    【新增函式】根據起始日期和結束日期生成日期列表 (包含起點和終點)。
    日期格式必須是 YYYYMMDD。
    """
    try:
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
    except ValueError:
        print("🛑 日期格式錯誤，請確保輸入為 YYYYMMDD 格式。")
        return []

    if start_date > end_date:
        print("🛑 起始日期不能晚於結束日期。")
        return []

    date_list = []
    current_date = start_date
    
    # 逐日增加，直到超過結束日期
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y%m%d"))
        current_date += timedelta(days=1)
        
    return date_list


def get_delivered_messages_range(date_list):
    """
    1. 逐日取得訊息發送數並彙總
    """
    print("\n====================================")
    print("🚀 1. 訊息發送數 (日期範圍查詢)")
    print("====================================")
    
    for date_str in date_list:
        endpoint = "message/delivery"
        params = {"date": date_str}
        
        data = get_insights_data(endpoint, params)
        print(data)


def get_followers_range(date_list):
    """
    2. 逐日取得好友數並彙總
    """
    print("\n====================================")
    print("🤝 2. 好友數統計 (日期範圍查詢)")
    print("====================================")
    
    for date_str in date_list:
        endpoint = "followers"
        params = {"date": date_str}
        
        data = get_insights_data(endpoint, params)
        print(data)



def get_demographics():
    """
    3. 取得好友屬性 (總體數據，不需範圍)
    """
    print("\n====================================")
    print("👤 3. 好友屬性統計 (總體數據)")
    print("====================================")
    
    endpoint = "demographic"
    data = get_insights_data(endpoint)
    
    print(data)


if __name__ == "__main__":
    
    if CHANNEL_ACCESS_TOKEN == "YOUR_CHANNEL_ACCESS_TOKEN":
        print("🛑 錯誤：請先將程式碼中的 'YOUR_CHANNEL_ACCESS_TOKEN' 替換為您的 Channel Access Token。")
    else:
        # ==========================================================
        # ⬇️ 這裡設定您要查詢的日期範圍 ⬇️
        # 日期格式必須是 YYYYMMDD (例如：20251101)
        # 建議查詢日期設定在昨天或更早，避免遇到數據延遲問題。
        START_DATE_STR = '20251110' 
        END_DATE_STR = '20251119'
        # ==========================================================
        
        # 根據設定的起點和終點生成日期列表
        date_range_list = generate_custom_date_range(START_DATE_STR, END_DATE_STR)
        
        if date_range_list:
            print(f"🗓️ 準備查詢日期範圍: {date_range_list[0]} ~ {date_range_list[-1]}")
            
            # 1. 執行訊息發送數的日期範圍查詢
            get_delivered_messages_range(date_range_list)
            
            # 2. 執行好友數的日期範圍查詢
            get_followers_range(date_range_list)
            
        # 3. 執行好友屬性查詢 (總體數據，不需範圍)
        get_demographics()