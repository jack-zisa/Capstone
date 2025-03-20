from openai import OpenAI
from utils.cloud_utils import access_secret
import re

client: OpenAI = OpenAI(api_key = access_secret('openai_api_key'))

def query(message: str) -> str:
    if client is None:
        print('Client not initialized')
        return

    completion = client.chat.completions.create(
        model = 'gpt-4o-mini',
        store = False,
        messages = [
            {'role': 'user', 'content': message}
        ]
    )

    return completion.choices[0].message.content

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
