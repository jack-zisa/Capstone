from google.cloud import bigquery
import os

# Initialize BigQuery client
client = bigquery.Client()

PROJECT_ID = "genuine-flight-397402"
META_DATASET_ID = f"{PROJECT_ID}.meta"
DATA_DATASET_ID = f"{PROJECT_ID}.data"
USERS_TABLE_ID = f"{META_DATASET_ID}.users"
SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
