import requests

# 你的 LINE Channel Access Token（長期 token）
ACCESS_TOKEN = '7c1wt3Cf/CmRj1TJvCOU2lgZ5h2xPQ/2QlKfjL9MCAlq3Vkh54c53h+DmrWch5kUOsxduK9yOwvpBogAAQspRgoRo48RhhfNvj/nNoDgD/kgX7pCatGuv+RalBYfJB7S0ykAuWxCtevcR4HIG/p47gdB04t89/1O/w1cDnyilFU='

# 想查詢的使用者 userId
user_id = 'U6d82c4b234135c5f0a2af724e81cf089'

# 組成 API URL
url = f'https://api.line.me/v2/bot/profile/{user_id}'

# 設定 header（授權必須帶 Bearer token）
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# 發送 GET 請求
response = requests.get(url, headers=headers)

# 檢查回應狀態
if response.status_code == 200:
    profile = response.json()
    print("使用者資訊如下：")
    print("userId:", profile['userId'])
    print("displayName:", profile['displayName'])
    print("pictureUrl:", profile.get('pictureUrl', '無'))
    print("statusMessage:", profile.get('statusMessage', '無'))
else:
    print("查詢失敗")
    print("狀態碼:", response.status_code)
    print("回應內容:", response.text)