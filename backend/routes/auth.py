from flask import Blueprint, request, jsonify, redirect, session
from utils.cloud_utils import invalidate_token, generate_jwt, store_fitbit_tokens, access_secret
import requests
import database as db
import uuid
import base64
import hashlib

FITBIT_CLIENT_ID = access_secret('fitbit_client_id')
FITBIT_CLIENT_SECRET = access_secret('fitbit_client_secret')
FITBIT_REDIRECT_URI = 'https://ai-health-analytics-968401790916.us-central1.run.app/auth/fitbit/callback'
FITBIT_AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
FITBIT_TOKEN_URL = "https://api.fitbit.com/oauth2/token"

auth_blueprint = Blueprint('auth', __name__, url_prefix = '/auth')

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required"}), 400

    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user_uuid = str(uuid.uuid4())

    # Check if user exists
    query = f"""
    SELECT username FROM `{db.USERS_TABLE_ID}`
    WHERE username = '{username}'
    """
    result = db.client.query(query).result()

    if next(result, None):
        return jsonify({"success": False, "error": "User already exists"}), 409

    # Insert new user
    insert_query = f"""
    INSERT INTO `{db.USERS_TABLE_ID}` (uuid, username, password_hash)
    VALUES ('{user_uuid}', '{username}', '{password_hash}')
    """
    db.client.query(insert_query)

    return jsonify({"success": True, "message": "User registered successfully"})

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """Handles user login and returns a JWT token."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Hash the password for lookup
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = f"""
    SELECT uuid, username FROM `{db.USERS_TABLE_ID}`
    WHERE username = '{username}' AND password_hash = '{hashed_password}'
    """
    result = db.client.query(query).result()

    # Verify user credentials (dummy check here)
    user = next(result, None)
    if user:
        session['uuid'] = user.uuid  # Store UUID in session
        token = generate_jwt(user.uuid)
        return jsonify({"success": True, "data": {"uuid": user.uuid, "username": user.username, "token": token}})
    else:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    """Logs the user out by invalidating the session."""
    token = request.headers.get("Authorization")
    
    if not token:
        return jsonify({"error": "Token required"}), 400
    
    # If using a token blacklist (optional), add it here
    invalidate_token(token)

    return jsonify({"message": "Logged out successfully"})

@auth_blueprint.route('/fitbit/login', methods=['POST'])
def fitbit_login():
    """Redirects user to Fitbit OAuth login page."""
    state = str(uuid.uuid4())
    session["oauth_state"] = state

    auth_url = (
        f"{FITBIT_AUTH_URL}?response_type=code"  # response_type must be 'code' for Authorization Code Flow
        f"&client_id={FITBIT_CLIENT_ID}"
        f"&redirect_uri={FITBIT_REDIRECT_URI}"
        f"&scope=heartrate%20profile"  # Add the required scopes
        f"&state={state}&prompt=login"
    )
    return redirect(auth_url)

@auth_blueprint.route('/fitbit/callback', methods=['GET'])
def fitbit_callback():
    """Handles Fitbit OAuth callback and retrieves an access token."""
    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return jsonify({"error": "Authorization code is missing"}), 400
    
    if state != session.get("oauth_state"):
        return jsonify({"error": "Invalid state parameter"}), 400

    # Exchange code for access token
    auth_header = f"{FITBIT_CLIENT_ID}:{FITBIT_CLIENT_SECRET}"
    auth_bytes = auth_header.encode("utf-8")
    auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": FITBIT_CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": FITBIT_REDIRECT_URI,
        "code": code
    }
    
    response = requests.post(FITBIT_TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        fitbit_data = response.json()
        access_token = fitbit_data["access_token"]
        refresh_token = fitbit_data["refresh_token"]
        
        # Store tokens in the database (linked to the user's UUID)
        store_fitbit_tokens(session.get('uuid'), access_token, refresh_token)

        return redirect(request.host_url)

    return jsonify({"error": f"Failed to retrieve Fitbit access token: {response.text}"}), 400