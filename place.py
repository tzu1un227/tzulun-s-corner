import requests

url = f"https://places.googleapis.com/v1/places:searchNearby?key=AIzaSyBp1b7fufMPm3H0hZUC8pbPGpwoSCvpTDg"

headers = {
    "Content-Type": "application/json",
    "X-Goog-FieldMask": "places.displayName"
}

request_body = {
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": 25.0330,   # 台北101
                "longitude": 121.5654
            },
            "radius": 500
        }
    },
    "maxResultCount": 5
}

response = requests.post(url, headers=headers, json=request_body)
print(response.json())
