import requests

# 這裡換成你的 Channel Access Token
TOKEN = "7c1wt3Cf/CmRj1TJvCOU2lgZ5h2xPQ/2QlKfjL9MCAlq3Vkh54c53h+DmrWch5kUOsxduK9yOwvpBogAAQspRgoRo48RhhfNvj/nNoDgD/kgX7pCatGuv+RalBYfJB7S0ykAuWxCtevcR4HIG/p47gdB04t89/1O/w1cDnyilFU="

headers = {"Authorization": "Bearer " + TOKEN}

def get_bot_info():
    url = "https://api.line.me/v2/bot/info"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def get_quota():
    url = "https://api.line.me/v2/bot/message/quota"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def get_consumption():
    url = "https://api.line.me/v2/bot/message/quota/consumption"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return f"{r.json()['totalUsage']}"

if __name__ == "__main__":
    print("=== Bot Info ===")
    print(get_bot_info())
    print("\n=== Quota ===")
    print(get_quota())
    print("\n=== Consumption ===")
    print(get_consumption())