from google.cloud import bigquery
import database as db

def get_user_by_uuid(uuid):
    """Fetches user details using UUID."""
    query = f"SELECT * FROM `{db.USERS_TABLE_ID}` WHERE uuid = @uuid"
    job = db.client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("uuid", "STRING", uuid)]
    ))
    rows = job.result()
    return list(rows)[0] if rows.total_rows > 0 else None


def update_user(uuid, update_data):
    """Updates user profile fields in BigQuery."""
    set_statements = ", ".join([f"{key} = @{key}" for key in update_data.keys()])
    query = f"UPDATE `{db.USERS_TABLE_ID}` SET {set_statements} WHERE uuid = @uuid"

    query_params = [
        bigquery.ScalarQueryParameter("uuid", "STRING", uuid)
    ] + [
        bigquery.ScalarQueryParameter(key, "STRING", value) for key, value in update_data.items()
    ]

    db.client.query(query, job_config=bigquery.QueryJobConfig(query_parameters=query_params))