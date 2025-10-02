import requests

def test_http_connection(url):
    try:
        response = requests.get(url, timeout=15)  # 設定 15 秒逾時
        if response.status_code == 200:
            print(f"成功連線到 {url}！")
        else:
            print(f"連線到 {url}，但回應狀態碼為 {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"連線到 {url} 失敗：{e}")

# 範例使用
# test_http_connection("https://www.google.com")
test_http_connection("https://irl-svr.ee.yzu.edu.tw:5009/bot1/callback")
# test_http_connection("https://140.138.176.197:4999/bot1/callback")
# test_http_connection("https://irl-svr.ee.yzu.edu.tw:80")
# test_http_connection("http://140.138.176.197:80")
# test_http_connection("https://deb.debian.org:80")
# test_http_connection("https://yzuirl.synology.me:516")
