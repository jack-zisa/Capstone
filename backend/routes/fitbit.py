from flask import Blueprint, jsonify, session, request
from utils.fitbit_utils import get_all_fitbit_data
from utils.cloud_utils import store_data_in_bigquery, get_user_by_uuid, access_secret

fitbit_blueprint = Blueprint('fitbit', __name__, url_prefix = '/fitbit')

@fitbit_blueprint.route('/webhook', methods=['POST', 'GET'])
def fitbit_webhook():
    if request.method == 'GET':
        verify_code = request.args.get('verify')
        if verify_code == access_secret('fitbit_webhook_verify_code'):
            return '', 204
        else:
            return 'Not Found', 404
    elif request.method == 'POST':
        # Handle the incoming Fitbit data
        data = request.json
        print("Received Fitbit data:", data)
        return '', 204

@fitbit_blueprint.route("/sync", methods=["POST"])
def fibit_sync():
    """Fetch and store Fitbit data in BigQuery."""
    uuid = session.get("uuid")
    if not uuid:
        return jsonify({"error": "User not authenticated"}), 401

    # Get stored Fitbit tokens from database
    user = get_user_by_uuid(uuid)  # Function to retrieve user info from DB
    access_token = user.get("fitbit_access_token")

    if not access_token:
        return jsonify({"error": "No Fitbit access token found"}), 400

    # Fetch data from Fitbit
    fitbit_data = get_all_fitbit_data(access_token)
    if not fitbit_data:
        return jsonify({"error": "Failed to fetch Fitbit data"}), 400

    # Store in BigQuery
    store_data_in_bigquery(uuid, fitbit_data)

    return jsonify({"message": "Fitbit data synced successfully!"})

@fitbit_blueprint.route("/get_data", methods=["POST"])
def fibit_get_data():
    """Fetch and store Fitbit data in BigQuery."""
    uuid = session.get("uuid")
    if not uuid:
        return jsonify({"error": "User not authenticated"}), 401

    # Get stored Fitbit tokens from database
    user = get_user_by_uuid(uuid)  # Function to retrieve user info from DB
    access_token = user.get("fitbit_access_token")

    if not access_token:
        return jsonify({"error": "No Fitbit access token found"}), 400

    # Fetch data from Fitbit
    fitbit_data = get_all_fitbit_data(access_token)
    if not fitbit_data:
        return jsonify({"error": "Failed to fetch Fitbit data"}), 400

    return jsonify({"data": fitbit_data})
