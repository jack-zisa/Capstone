import objects as objs
import apple_watch.load as ap_load
import fitbit.load as fb_load
import export as exp
import chatgpt
import auth

openai_api_key: str = ''
fitbit_client_id: str = ''
fitbit_client_secret: str = ''

with open('secrets.txt', 'r') as secrets:
    for line in secrets.readlines():
        line_data = line.split('=')
        if line_data[0] == 'openai_api_key':
            openai_api_key = line_data[1].strip().replace('\n','')
        elif line_data[0] == 'fitbit_client_id':
            fitbit_client_id = line_data[1].strip().replace('\n','')
        elif line_data[0] == 'fitbit_client_secret':
            fitbit_client_secret = line_data[1].strip().replace('\n','')

chatgpt.init(openai_api_key)
auth.authenticate(fitbit_client_id, fitbit_client_secret)

persons: dict = {}
data: dict = {}

person1: objs.Person = objs.Person(22, 'F', 64, 107, objs.APPLE_WATCH, 'heather_belitskus', 'Middletown', 'DE', 'caucasian', False, objs.Occupation('Wilmington', 'DE', True, False))
persons[person1.uuid] = person1

person2: objs.Person = objs.Person(22, 'M', 64, 107, objs.FITBIT, 'andrew_geisler', 'Middletown', 'PA', 'caucasian', False, objs.Occupation('Altoona', 'PA', False, True))
persons[person2.uuid] = person2

for person in persons:
    data[person] = {}

ap_load.load(persons, data)
fb_load.load(persons, data)

exp.export(persons, data)

#auth.query(person1, {"Name": "Alice", "Age": 25, "Height": "5'6\"", "Weight": "130 lbs"})