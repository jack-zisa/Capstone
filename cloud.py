from google.cloud import bigquery
from google.oauth2 import service_account
import objects as objs
import pandas as pd

client: bigquery.Client = None

PROJECT_ID = 'genuine-flight-397402'
DATASET_ID = 'meta'
USERS_TABLE_ID = 'users'

def init():
    global client
    credentials = service_account.Credentials.from_service_account_file('genuine-flight-397402-20e701a5e711.json')
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    print(f'Found Google BigQuery project \'{client.project}\'')

def register_user(person: objs.Person):
    df = pd.DataFrame([
        {
            'uuid': person.uuid,
            'age': person.age,
            'gender': person.gender,
            'weight': person.weight,
            'height': person.height,
            'data_source_type': person.data_source_type
        }
    ])

    job = client.load_table_from_dataframe(df, f'{PROJECT_ID}.{DATASET_ID}.{USERS_TABLE_ID}')

    job.result()

    print(f'Registered user \'{person.uuid}\'')
