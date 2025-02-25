import webbrowser
from urllib.parse import urlencode
import requests
from requests.auth import HTTPBasicAuth

tokens: dict = None

def authenticate(client_id: str, client_secret: str):
    global tokens

    REDIRECT_URI = 'https://github.com/jack-zisa/Capstone'
    SCOPE = 'activity heartrate location nutrition profile settings sleep social weight'
    AUTH_URL = 'https://www.fitbit.com/oauth2/authorize'

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URI
    }

    # Open the authorization URL in a browser
    auth_link = f'{AUTH_URL}?{urlencode(params)}'
    print(f'Go to the following link to authorize:\n{auth_link}')
    webbrowser.open(auth_link)

    # STEP 2 - TOKENS

    TOKEN_URL = 'https://api.fitbit.com/oauth2/token'

    auth_code = input('Enter the authorization code from URL: ')

    data = {
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }

    # Fitbit requires Basic Authentication using Client ID and Secret
    response = requests.post(
        TOKEN_URL,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret),
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    tokens = response.json()
    #print('Access Token:', tokens.get('access_token'))
    #print('Refresh Token:', tokens.get('refresh_token'))    

def request(url: str) -> dict:
    global tokens

    if tokens is None:
        return {}
    
    headers = {
        'Authorization': f'Bearer {tokens.get('access_token')}'
    }

    return requests.get(url, headers=headers).json()