import requests

def find_land_bank_text_search(query):
    url = "https://places.googleapis.com/v1/places:searchText?key=AIzaSyBp1b7fufMPm3H0hZUC8pbPGpwoSCvpTDg"

    payload = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {"latitude": 24.9607, "longitude": 121},
                "radius": 5000
            }
        },
        "languageCode": "zh-TW",
        "maxResultCount": 2
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.id"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        places = data.get("places", [])

        if not places:
            print("未找到任何符合的土地銀行分行。")
            return

        print("找到的土地銀行分行：")
        for place in places:
            print(f"名稱: {place['displayName']['text']}")
            print(f"地址: {place.get('formattedAddress', '無地址資訊')}")
            print(f"類型: {', '.join(place.get('types', []))}")
            print(f"地點 ID: {place.get('id', '無 ID 資訊')}")
            print("---")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 錯誤: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"請求失敗: {e}")
    except ValueError as e:
        print(f"回應解析錯誤: {e}")

find_land_bank_text_search("土地銀行")