from openai import OpenAI
import objects as objs

client: OpenAI = None

def init(key: str):
    client = OpenAI(api_key = key)

def query(person: objs.Person, health_data: dict):
    if client is None:
        print('Client not initialized')
        return

    message: str = f'''using the following demographic data and health data tables, make an assessment on whether this person may be facing a medical issue.
{'|'.join(health_data.keys())}
{'|'.join(['-' * 3] * len(health_data))}
'''
    print(message)
    return

    completion = client.chat.completions.create(
        model = 'gpt-4o-mini',
        store = False,
        messages = [
            {'role': 'user', 'content': message}
        ]
    )

    print(completion.choices[0].message.content)
