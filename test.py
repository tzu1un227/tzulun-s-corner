import requests

url = "http://irl-svr.ee.yzu.edu.tw/.well-known/acme-challenge/test.txt"

try:
    response = requests.get(url, timeout=10)  # 10秒超時
    if response.status_code == 200:
        print("可以訪問！內容如下：")
        print(response.text)
    else:
        print(f"訪問失敗，HTTP 狀態碼: {response.status_code}")
except requests.exceptions.Timeout:
    print("訪問超時！")
except requests.exceptions.ConnectionError:
    print("無法連線到伺服器！")
except Exception as e:
    print("其他錯誤：", e)
