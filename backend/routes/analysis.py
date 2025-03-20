from flask import Blueprint, jsonify, session
from utils.analysis_utils import query, parse_markdown_table
from utils.cloud_utils import get_user_health_data, get_user_by_uuid
import json

analysis_blueprint = Blueprint('analysis', __name__, url_prefix = '/analysis')

@analysis_blueprint.route("/analyze", methods=["POST"])
def analyze():
    """Fetch recent data and analyze it with OpenAI."""
    uuid = session.get('uuid')

    if not uuid:
        return jsonify({"error": "UUID is required"}), 400
    
    user = get_user_by_uuid(uuid)

    try:
        response: str = query(f'''HEALTH:
{get_user_health_data(uuid, '')}
DEMOGRAPHICS:
age|gender|height|weight
-|-|-|-
{user['age']}|{user['gender']}|{user['height']}|{user['weight']}
Using the demographic & health data tables, provide your conclusions for whether this person may be facing a medical issue. Respond only in a markdown table with the following columns: Timestamp, Issue Name, Issue Severity (low, medium, high), Issue Reasoning. Do not include any other explanation or text''')
        parsed_data = parse_markdown_table(response)
        return jsonify({"response": json.dumps(parsed_data, indent=4)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
