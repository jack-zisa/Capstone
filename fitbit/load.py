import os
import objects as objs

data_paths = ['data/fitbit/']

def load(persons: dict):
    for data_path in data_paths:
        for dir in os.listdir(data_path):
            if os.path.isdir(f'{data_path}/{dir}'):
                key = hash(dir)

                if key in os.listdir('exports/'):
                    print(f'Already parsed person \'{key}\'')
                    continue

                if key in persons:
                    person: objs.Person = persons.get(key)
                    if person.data_source_type == objs.FITBIT:
                        load_heart_rate_data(person)
                        load_heart_rate_variability_data(person)
                        load_oxygen_saturation_data(person)
                        load_physical_activity_data(person)
                        load_sleep_score_data(person)
                        load_noise_detection_data(person)
                        load_stress_data(person)

def load_heart_rate_data(person: str):
    pass

def load_heart_rate_variability_data(person: str):
    pass

def load_oxygen_saturation_data(person: str):
    pass

def load_physical_activity_data(person: str):
    pass

def load_sleep_score_data(person: str):
    pass

def load_noise_detection_data(person: str):
    pass

def load_stress_data(person: str):
    pass