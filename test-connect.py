import requests

def test_http_connection(url):
    try:
        response = requests.get(url, timeout=5)  # 設定 5 秒逾時
        if response.status_code == 200:
            print(f"成功連線到 {url}！")
        else:
            print(f"連線到 {url}，但回應狀態碼為 {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"連線到 {url} 失敗：{e}")

# 範例使用
# test_http_connection("https://www.google.com")
test_http_connection("https://irl-svr.ee.yzu.edu.tw:4999")
