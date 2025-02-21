import xml.etree.ElementTree as et
import os
import objects as objs

data_paths = ['data/apple_watch/']

def load(persons: dict):
    for data_path in data_paths:
        for filename in os.listdir(data_path):
            filedata = filename.split('.')
            key = hash(filedata[0])

            if key in os.listdir('exports/'):
                print(f'Already parsed person \'{key}\'')
                continue
            
            if key in persons:
                person: objs.Person = persons.get(key)
                if person.data_source_type == objs.APPLE_WATCH and filedata[1] == 'xml':
                    load_apple_watch(person, f'{data_path}{filename}')

def load_apple_watch(person: objs.Person, filename: str):
    print(f'Loading \'{person.uuid}\' of data source type \'{person.data_source_type}\'')

    tree = et.parse(filename)
    root = tree.getroot()

    for element in root.findall('Record'):
        type: str = element.get('type') if 'type' in element.keys() else None
        startDate: str = element.get('startDate')
        endDate: str = element.get('endDate')
        value: str = element.get('value') if 'value' in element.keys() else None

        if type is None or value is None:
            continue
        
        if type == objs.HEART_RATE:
            person.data['heart_rate'][startDate] = value
        elif type == objs.WATER_INTAKE:
            person.data['water_intake'][startDate] = value
        elif type == objs.RESPIRATORY_RATE:
            person.data['respiratory_rate'][startDate] = value
        elif type == objs.RESTING_ENERGY_BURNED:
            person.data['resting_energy_burned'][startDate] = value
        elif type == objs.ACTIVE_ENERGY_BURNED:
            person.data['active_energy_burned'][startDate] = value
        elif type == objs.EXERCISE_TIME:
            person.data['exercise_time'][startDate] = value
        elif type == objs.AUDIO_EXPOSURE:
            person.data['audio_exposure'][startDate] = value
        elif type == objs.OXYGEN_CONSUMPTION:
            person.data['oxygen_consumption'][startDate] = value
        elif type == objs.HEART_RATE_VARIABILITY:
            person.data['heart_rate_variability'][startDate] = value