from google.cloud import bigquery, secretmanager
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import database as db
import google_crc32c
import jwt

def get_user_by_username(username):
    """Retrieves user data by username from BigQuery."""
    query = f"SELECT * FROM `{db.USERS_TABLE_ID}` WHERE username = @username"
    job = db.client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("username", "STRING", username)]
    ))
    rows = job.result()
    return list(rows)[0] if rows.total_rows > 0 else None

def get_user_by_uuid(uuid):
    """Retrieves user data by username from BigQuery."""
    query = f"SELECT * FROM `{db.USERS_TABLE_ID}` WHERE uuid = @uuid"
    job = db.client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("uuid", "STRING", uuid)]
    ))
    rows = job.result()
    return list(rows)[0] if rows.total_rows > 0 else None

def create_user(username, password):
    """Creates a new user in BigQuery."""
    hashed_password = generate_password_hash(password)
    query = f"""
        INSERT INTO `{db.USERS_TABLE_ID}` (username, password, created_at)
        VALUES (@username, @password, @created_at)
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password", "STRING", hashed_password),
            bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", datetime.utcnow())
        ]
    )
    db.client.query(query, job_config=job_config)

def verify_user(username, password):
    """Verifies user credentials."""
    user = get_user_by_username(username)
    if user and check_password_hash(user["password"], password):
        return user
    return None

def generate_jwt(user_id):
    """Generates a JWT token for authentication."""
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=24)}
    return jwt.encode(payload, db.SECRET_KEY, algorithm="HS256")

def invalidate_token(token):
    """Stores an invalid token in a blacklist table (if required)."""
    query = f"""
        INSERT INTO `{db.META_DATASET_ID}.token_blacklist` (token, created_at)
        VALUES (@token, @created_at)
    """
    db.client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("token", "STRING", token),
            bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", datetime.utcnow())
        ]
    ))

def store_fitbit_tokens(uuid, access_token, refresh_token):
    query = f"""
    UPDATE `{db.USERS_TABLE_ID}`
    SET fitbit_access_token = @access_token, fitbit_refresh_token = @refresh_token
    WHERE uuid = @uuid
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("access_token", "STRING", access_token),
            bigquery.ScalarQueryParameter("refresh_token", "STRING", refresh_token),
            bigquery.ScalarQueryParameter("uuid", "STRING", uuid),
        ]
    )

    db.client.query(query, job_config=job_config)  # Executes safely

def store_data_in_bigquery(uuid, fitbit_data):
    """Insert Fitbit data into Google BigQuery."""
    table_id = f"{db.DATA_DATASET_ID}.daily"

    heart_data = fitbit_data['heart_rate']["activities-heart"][0]["value"]["heartRateZones"]
    spo2_data = fitbit_data['spo2']
    br_data = fitbit_data['breathing_rate']
    hrv_data = fitbit_data['hrv']

    # Prepare rows to insert for each heart rate zone
    rows_to_insert = []
    for zone in heart_data:
        rows_to_insert.append({
            "uuid": uuid,
            "timestamp": datetime.fromisoformat(fitbit_data['heart_rate']["activities-heart"][0]['dateTime']).isoformat(),
            "heart_rate_min": zone["min"],
            "heart_rate_max": zone["max"],
            "heart_rate_type": zone["name"],
        })
    if spo2_data:
        rows_to_insert.append({
            "uuid": uuid,
            "timestamp": datetime.fromisoformat(spo2_data["dateTime"].rstrip('Z')).isoformat(),
            "sp02_min": spo2_data['value']["min"],
            "sp02_max": spo2_data['value']["max"],
            "sp02_avg": spo2_data['value']['avg'],
        })
    if br_data:
        rows_to_insert.append({
            "uuid": uuid,
            "timestamp": datetime.fromisoformat(br_data["dateTime"].rstrip('Z')).isoformat(),
            "breathing_rate": br_data['value']["breathingRate"],
        })
    if hrv_data:
        rows_to_insert.append({
            "uuid": uuid,
            "timestamp": datetime.fromisoformat(hrv_data["dateTime"].rstrip('Z')).isoformat(),
            "daily_rmssd": hrv_data['value']["dailyRmssd"],
            "deep_rmssd": hrv_data['value']["deepRmssd"],
        })

    errors = db.client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print("BigQuery errors:", errors)

def get_user_health_data(uuid, timestamp) -> list:
    table_id = f"{db.DATA_DATASET_ID}.daily"
    # ADD 'and timestamp = @timestamp' TO QUERY
    query = f"SELECT * FROM `{table_id}` WHERE uuid = @uuid"
    job = db.client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("uuid", "STRING", uuid)
            #bigquery.ScalarQueryParameter("timestamp", "TIMESTAMP", timestamp)
        ]
    ))

    data = []
    for row in job.result():
        row_dict = dict(row.items())  # Convert each row into a dictionary
        data.append(row_dict)
    return data

def set_user_demographics(uuid, data: dict):
    query = f"""
    UPDATE `{db.USERS_TABLE_ID}`
    SET gender = @gender, age = @age, height = @height, weight = @weight, phone_number = @phone_number
    WHERE uuid = @uuid
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("gender", "STRING", data.get('gender', "")),
            bigquery.ScalarQueryParameter("age", "INT64", data.get('age', 0)),
            bigquery.ScalarQueryParameter("height", "FLOAT64", data.get('height', 0.0)),
            bigquery.ScalarQueryParameter("weight", "FLOAT64", data.get('weight', 0.0)),
            bigquery.ScalarQueryParameter("phone_number", "STRING", data.get('phoneNumber', "")),
            bigquery.ScalarQueryParameter("uuid", "STRING", uuid),
        ]
    )

    db.client.query(query, job_config=job_config)

def set_user_email(uuid, email: str):
    query = f"""
    UPDATE `{db.USERS_TABLE_ID}`
    SET email = @email
    WHERE uuid = @uuid
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("uuid", "STRING", uuid),
            bigquery.ScalarQueryParameter("email", "STRING", email),
        ]
    )

    db.client.query(query, job_config=job_config)

def access_secret(secret_id):
    """
    Access a secret version from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()

    # Access the secret
    response = client.access_secret_version(request={"name": f"projects/968401790916/secrets/{secret_id}/versions/latest"})

    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("Data corruption detected.")
        return response

    # Decode and return the secret payload
    return response.payload.data.decode("UTF-8")