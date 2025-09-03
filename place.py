import requests

url = f"https://places.googleapis.com/v1/places:searchNearby?key=AIzaSyBp1b7fufMPm3H0hZUC8pbPGpwoSCvpTDg"

headers = {
    "Content-Type": "application/json",
    "X-Goog-FieldMask": "places.displayName,places.googleMapsLinks.directionsUri"
}

request_body = {
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": 24.9607,   
                "longitude": 121.0619
            },
            "radius": 5000
        }
    },
    "maxResultCount": 3,
    "includedTypes":["bank"],
    "rankPreference": "DISTANCE"
}

response = requests.post(url, headers=headers, json=request_body)
print(response.json())
