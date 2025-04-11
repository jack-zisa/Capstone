from flask import Blueprint
from utils.cloud_utils import access_secret
import requests

google_blueprint = Blueprint('google', __name__, url_prefix = '/google')

@google_blueprint.route("/sync", methods=["POST"])
def google_sync():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={access_secret('google_api_key')}"
    
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "homeMobileCountryCode": 310,
        "homeMobileNetworkCode": 410,
        "radioType": "gsm",
        "carrier": "Vodafone",
        "considerIp": True
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f'GEOLOC: {response.json()}')
    return response.json()
