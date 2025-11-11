import requests
import json

API_KEY = "AIzaSyBp1b7fufMPm3H0hZUC8pbPGpwoSCvpTDg"  # 換成你自己的
URL = "https://places.googleapis.com/v1/places:searchText"

def text_search_with_routing():
    query = "台北 便利商店"

    body = {
        "textQuery": query,
        "routingParameters": {
            "origin": {
                "latitude": 25.033964,
                "longitude": 121.564468
            },
            # 可選 travelMode／routingPreference 等：
            "travelMode": "DRIVE",
            # "routingPreference": "TRAFFIC_UNAWARE"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,routingSummaries"
    }

    resp = requests.post(URL, headers=headers, data=json.dumps(body))
    print(f"狀態碼: {resp.status_code}")
    print(resp.text)

if __name__ == "__main__":
    text_search_with_routing()
