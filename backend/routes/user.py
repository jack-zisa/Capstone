from flask import Blueprint, request, jsonify, session
from utils.cloud_utils import set_user_demographics
from google.cloud import bigquery
import database as db

user_blueprint = Blueprint('user', __name__, url_prefix = '/user')

@user_blueprint.route('/demographics', methods=['POST', 'GET'])
def set_demographics():
    uuid = session.get('uuid')

    if not uuid:
        return jsonify({"error": "UUID is required"}), 400

    if request.method == 'GET':
        # Fetch user demographics
        query = f"""
        SELECT gender, age, height, weight 
        FROM `{db.USERS_TABLE_ID}`
        WHERE uuid = @uuid
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("uuid", "STRING", uuid)
            ]
        )

        query_job = db.client.query(query, job_config=job_config)
        result = query_job.result()

        row = next(result, None)
        if row:
            return jsonify({
                "gender": row.gender,
                "age": row.age,
                "height": row.height,
                "weight": row.weight
            })
        else:
            return jsonify({"error": "User not found"}), 404

    elif request.method == 'POST':
        # Update user demographics
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        set_user_demographics(uuid, data)
        return jsonify({"message": "Demographics saved successfully!"})