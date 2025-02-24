import xml.etree.ElementTree as et
import os
import objects as objs
import hashlib

data_paths = ['data/apple_watch/']

def load(persons: dict, data: dict):
    for data_path in data_paths:
        for filename in os.listdir(data_path):
            filedata = filename.split('.')
            key = hashlib.sha256(filedata[0].encode('utf-8')).hexdigest()

            if os.path.exists('exports/') and f'{key}.csv' in os.listdir('exports/'):
                print(f'Already parsed person \'{key}\'')
                continue
            
            if key in persons:
                person: objs.Person = persons.get(key)
                if person.data_source_type == objs.APPLE_WATCH and filedata[1] == 'xml':
                    load_apple_watch(person, data, f'{data_path}{filename}')

def load_apple_watch(person: objs.Person, data: dict, filename: str):
    print(f'Loading \'{person.uuid}\' of data source type \'{person.data_source_type}\'')

    tree = et.parse(filename)
    root = tree.getroot()

    for element in root.findall('Record'):
        type: str = element.get('type') if 'type' in element.keys() else None
        startDate: str = element.get('startDate').split(' ')
        endDate: str = element.get('endDate')
        value: str = element.get('value') if 'value' in element.keys() else None

        timestamp: str = f'{startDate[0]}T{startDate[1]}Z'

        if timestamp not in data[person.uuid]:
            data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)

        if type is None or value is None:
            continue
        
        if type == objs.HEART_RATE:
            data[person.uuid][timestamp].heart_rate = value.strip().replace('\n','')
        elif type == objs.WATER_INTAKE:
            data[person.uuid][timestamp].water_intake = value.strip().replace('\n','')
        elif type == objs.RESPIRATORY_RATE:
            data[person.uuid][timestamp].respiratory_rate = value.strip().replace('\n','')
        elif type == objs.RESTING_ENERGY_BURNED:
            data[person.uuid][timestamp].resting_energy_burned = value.strip().replace('\n','')
        elif type == objs.ACTIVE_ENERGY_BURNED:
            data[person.uuid][timestamp].active_energy_burned = value.strip().replace('\n','')
        elif type == objs.AUDIO_EXPOSURE:
            data[person.uuid][timestamp].audio_exposure = value.strip().replace('\n','')
        elif type == objs.OXYGEN_CONSUMPTION:
            data[person.uuid][timestamp].oxygen_consumption = value.strip().replace('\n','')
        elif type == objs.HEART_RATE_VARIABILITY:
            data[person.uuid][timestamp].heart_rate_variability = value.strip().replace('\n','')
