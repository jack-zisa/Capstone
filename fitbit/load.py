import os
import objects as objs
import hashlib

data_paths = ['data/fitbit/']

def load(persons: dict, data: dict):
    for data_path in data_paths:
        for dir in os.listdir(data_path):
            path: str = f'{data_path}/{dir}'
            if os.path.isdir(path):
                key = hashlib.sha256(dir.encode('utf-8')).hexdigest()

                if os.path.exists('exports/') and f'{key}.csv' in os.listdir('exports/'):
                    print(f'Already parsed person \'{key}\'')
                    continue

                if key in persons:
                    person: objs.Person = persons.get(key)

                    print(f'Loading \'{key}\' of data source type \'{person.data_source_type}\'')
                    if person.data_source_type == objs.FITBIT:
                        load_heart_rate_data(person, data, path)
                        load_heart_rate_variability_data(person, data, path)
                        load_respiratory_rate_data(person, data, path)
                        load_sleep_blood_oxygen_saturation_data(person, data, path)
                        load_oxygen_saturation_data(person, data, path)
                        load_physical_activity_data(person, data, path)
                        load_sleep_score_data(person, data, path)
                        load_noise_detection_data(person, data, path)
                        load_stress_data(person, data, path)

def load_heart_rate_data(person: objs.Person, data: dict, path: str):
    for dir in os.listdir(f'{path}/Physical Activity_GoogleData'):
        if dir.endswith('.csv') and 'heart_rate' in dir:
            with open(f'{path}/Physical Activity_GoogleData/{dir}', 'r') as file:
                if 'timestamp,beats per minute' in file.readline():
                    for line in file.readlines():
                        line_data = line.split(',')
                        timestamp = line_data[0]

                        if timestamp not in data[person.uuid]:
                            data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)

                        data[person.uuid][timestamp].heart_rate = line_data[1].strip().replace('\n','')

def load_heart_rate_variability_data(person: str, data: dict, path: str):
    pass

def load_respiratory_rate_data(person: str, data: dict, path: str):
    for dir in os.listdir(f'{path}/Heart Rate Variability'):
        if dir.endswith('.csv') and 'Respiratory Rate' in dir:
            with open(f'{path}/Heart Rate Variability/{dir}', 'r') as file:
                if 'timestamp,daily_respiratory_rate' in file.readline():
                    for line in file.readlines():
                        line_data = line.split(',')
                        timestamp = line_data[0]

                        if timestamp not in data[person.uuid]:
                            data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)
                        
                        data[person.uuid][timestamp].respiratory_rate = line_data[1].strip().replace('\n','')
                        
def load_sleep_blood_oxygen_saturation_data(person: str, data: dict, path: str):
    for dir in os.listdir(f'{path}/Oxygen Saturation (SpO2)'):
        if dir.endswith('.csv'):
            with open(f'{path}/Oxygen Saturation (SpO2)/{dir}', 'r') as file:
                if 'timestamp,value' in file.readline():
                    for line in file.readlines():
                        line_data = line.split(',')
                        timestamp = line_data[0]

                        if timestamp not in data[person.uuid]:
                            data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)

                        data[person.uuid][timestamp].sleep_blood_oxygen_saturation = line_data[1].strip().replace('\n','')

def load_oxygen_saturation_data(person: str, data: dict, path: str):
    for dir in os.listdir(f'{path}/Physical Activity_GoogleData'):
        if dir.endswith('.csv') and 'oxygen_saturation' in dir:
            with open(f'{path}/Physical Activity_GoogleData/{dir}', 'r') as file:
                if 'timestamp,oxygen saturation percentage' in file.readline():
                    for line in file.readlines():
                        line_data = line.split(',')
                        timestamp = line_data[0]

                        if timestamp not in data[person.uuid]:
                            data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)

                        data[person.uuid][timestamp].oxygen_saturation = line_data[1].strip().replace('\n','')

def load_physical_activity_data(person: str, data: dict, path: str):
    pass

def load_sleep_score_data(person: str, data: dict, path: str):
    with open(f'{path}/Sleep Score/sleep_score.csv', 'r') as file:
        for line in file.readlines():
            line_data = line.split(',')
            timestamp = line_data[1]

            if timestamp not in data[person.uuid]:
                data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)

            scores = [line_data[2], line_data[3], line_data[4], line_data[5]]
            if type(scores[0]) == str:
                continue
            score = 0
            for s in scores:
                score += s
            score /= 4

            data[person.uuid][timestamp].sleep_score = score
            data[person.uuid][timestamp].sleep_time = line_data[6].strip().replace('\n','')
            data[person.uuid][timestamp].sleeping_heart_rate = line_data[7].strip().replace('\n','')
            data[person.uuid][timestamp].restlessness = line_data[8].strip().replace('\n','')

def load_noise_detection_data(person: str, data: dict, path: str):
    pass

def load_stress_data(person: str, data: dict, path: str):
    with open(f'{path}/Stress Score/Stress Score.csv', 'r') as file:
        for line in file.readlines():
            line_data = line.split(',')
            timestamp = line_data[0]

            if timestamp not in data[person.uuid]:
                data[person.uuid][timestamp] = objs.HealthRecord(person.uuid, timestamp)

            data[person.uuid][timestamp].stress_score = line_data[2].strip().replace('\n','')