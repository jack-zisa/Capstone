from flask import Blueprint
from utils.cloud_utils import access_secret
import requests

google_blueprint = Blueprint('google', __name__, url_prefix = '/google')

@google_blueprint.route("/sync", methods=["POST"])
def google_sync():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={access_secret('google_api_key')}"
    response = requests.post(url)
    print(response.json())
    return response.json()
