from flask import request, jsonify
from openai import OpenAI
from utils.cloud_utils import access_secret
from twilio.rest import Client
import re

openai_client: OpenAI = OpenAI(api_key = access_secret('openai_api_key'))
twilio_client = Client(access_secret('twilio_account_sid'), access_secret('twilio_auth_token'))

def query(message: str) -> str:
    if openai_client is None:
        print('Client not initialized')
        return

    completion = openai_client.chat.completions.create(
        model = 'gpt-4o-mini',
        store = False,
        messages = [
            {'role': 'user', 'content': message}
        ]
    )
    
    result = completion.choices[0].message.content

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    #alert(result, "")

    return result

def alert(message: str, phone_number: str):
    twilio_client.api.account.messages.create(
        body=message,
        from_=access_secret('twilio_phone_number'),
        to="+12153375787"
    )

def parse_markdown_table(markdown_str):
    # Regex to match table structure
    table_pattern = r"(\|[^\n]+\|)+"
    match = re.findall(table_pattern, markdown_str)
    
    if match:
        # Split the header (first row) and data rows
        header_row = match[0].strip("|").split("|")
        data_rows = [row.strip("|").split("|") for row in match[1:]]

        # Create a list of dictionaries with header as keys
        table_data = []
        for row in data_rows:
            # Check if the row is just a separator (all cells contain only hyphens)
            if all(cell.strip().startswith("-") for cell in row):
                continue  # Skip separator rows
            
            table_data.append(dict(zip(header_row, row)))
        
        return table_data
    else:
        return []
