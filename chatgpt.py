from openai import OpenAI
import objects as objs

client: OpenAI = None

def init(key: str):
    global client
    client = OpenAI(api_key = key)

def query(person: objs.Person, health_data: dict):
    if client is None:
        print('Client not initialized')
        return

    message: str = f'''Using the demographic data and health data tables, make an assessment on whether this person may be facing a medical issue.

HEALTH:    
{'|'.join(health_data.keys())}
{'|'.join('-' * len(health_data))}

DEMOGRAPHICS:
age|gender|height|weight|city|state|ethnicity|smokes|occupation_city|occupation_state|occupation_remote|occupation_physical
-|-|-|-|-|-|-|-|-|-|-|-
{person.age}|{person.gender}|{person.height}|{person.weight}|{person.city}|{person.state}|{person.ethnicity}|{person.smokes}|{person.occupation.city}|{person.occupation.state}|{person.occupation.remote}|{person.occupation.physical}

Provide your conclusions in table format with columns: Issue Name, Issue Severity (low, medium, high), Issue Reasoning.
'''
    completion = client.chat.completions.create(
        model = 'gpt-4o-mini',
        store = False,
        messages = [
            {'role': 'user', 'content': message}
        ]
    )

    print(completion.choices[0].message.content)
