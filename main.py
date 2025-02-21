import objects as objs
import apple_watch.load as ap_load
import fitbit.load as fb_load
import export as exp
import auth

openai_api_key: str = ''

with open('secrets.txt', 'r') as secrets:
    openai_api_key = secrets.readline()

print(openai_api_key)

persons: dict = {}

person1: objs.Person = objs.Person(22, 'F', 64, 107, objs.APPLE_WATCH, objs.DEFAULT_PERSON_DATA, 'heather_belitskus', 'Middletown', 'DE', 'caucasian', False, objs.Occupation('Wilmington', 'DE', True, False))
persons[person1.uuid] = person1

person2: objs.Person = objs.Person(22, 'M', 64, 107, objs.FITBIT, objs.DEFAULT_PERSON_DATA, 'andrew_geisler', 'Middletown', 'PA', 'caucasian', False, objs.Occupation('Altoona', 'PA', False, True))
persons[person2.uuid] = person2

ap_load.load(persons)
fb_load.load(persons)

#exp.export(persons)

auth.init(openai_api_key)
#auth.query(person1, {"Name": "Alice", "Age": 25, "Height": "5'6\"", "Weight": "130 lbs"})