import requests

FITBIT_API_URL = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"

def get_fitbit_data(access_token):
    """Fetch Fitbit data using the access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(FITBIT_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
