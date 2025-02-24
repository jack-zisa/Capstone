import objects as objs
import os

def export(persons: dict, data: dict):
    if not os.path.exists('exports/'):
        os.makedirs('exports/')

    for key in persons.keys():
        print(f'Exporting data for uuid \'{key}\'')
        person: objs.Person = persons[key]
        with open(f'exports/{person.uuid}.csv', 'w') as file:
            file.write('uuid|timestamp|heart_rate|water_intake|respiratory_rate|resting_energy_burned|active_energy_burned|audio_exposure|oxygen_consumption|heart_rate_variability|sleep_blood_oxygen_saturation|oxygen_saturation|sleep_score|sleep_time|sleeping_heart_rate|restlessness|stress_score|floors|steps|swim_lengths|stroke_count|swim_stroke|calories|altitude|heart_rate_zone|distance\n')
            for timestamp in data[key]:
                record: str = str(data[key][timestamp])
                if 'Z||||||||||||||||||||||||' not in record:
                    file.write(record)
        
    print(f'Exporting \'persons\' data')

    with open('exports/persons.csv', 'w') as file:
        file.write('uuid|age|gender|height|weight|city|state|ethnicity|smokes|occupation_city|occupation_state|occupation_remote|occupation_physical\n')
        for key in persons.keys():
            person: objs.Person = persons[key]
            file.write(f'{person.uuid}|{person.age}|{person.gender}|{person.height}|{person.weight}|{person.city}|{person.state}|{person.ethnicity}|{person.smokes}|{person.occupation.city}|{person.occupation.state}|{person.occupation.remote}|{person.occupation.physical}\n')