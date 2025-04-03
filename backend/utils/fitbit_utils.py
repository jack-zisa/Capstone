import requests

fitbit_api_urls: dict = {
    'heart_rate': 'activities/heart/date/today/1d/1sec.json',
    'hrv': 'hrv/date/today/all.json',
    'breathing_rate': 'br/date/today/all.json',
    'spo2': 'spo2/date/today/all.json'
}

def get_all_fitbit_data(access_token):
    data: dict = {
        'heart_rate': {},
        'hrv': {},
        'breathing_rate': {},
        'spo2': {},
    }

    for key in fitbit_api_urls.keys():
        ret_data = get_fitbit_data(access_token, key)
        if ret_data is None:
            continue
        data[key] = ret_data
    
    return data

def get_fitbit_data(access_token, type: str):
    """Fetch Fitbit data using the access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f'https://api.fitbit.com/1/user/-/{fitbit_api_urls.get(type)}', headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
