import objects as objs
import os

def export(persons: dict):
    for key in persons.keys():
        person: objs.Person = persons[key]
        for data_key in person.data.keys():
            type_data: dict = person.data[data_key]

            directory: str = f'exports/{person.uuid}'
            if not os.path.exists(directory):
                os.makedirs(directory)

            print(f'Exporting \'{data_key}\' data for uuid \'{person.uuid}\'')

            with open(f'{directory}/{data_key}.csv', 'w') as file:
                file.write('uuid|date|time|value\n')
                for type_data_key in type_data.keys():
                    datetime = type_data_key.split(' ')
                    date = datetime[0]
                    time = datetime[1]
                    file.write(f'{person.uuid}|{date}|{time}|{person.data[data_key][type_data_key]}\n')
    
    if not os.path.exists('exports/'):
        os.makedirs('exports/')
    
    print(f'Exporting \'persons\' data')

    with open('exports/persons.csv', 'w') as file:
        file.write('uuid|age|gender|height|weight|city|state|ethnicity|smokes|occupation_city|occupation_state|occupation_remote|occupation_physical\n')
        for key in persons.keys():
            person: objs.Person = persons[key]
            file.write(f'{person.uuid}|{person.age}|{person.gender}|{person.height}|{person.weight}|{person.city}|{person.state}|{person.ethnicity}|{person.smokes}|{person.occupation.city}|{person.occupation.state}|{person.occupation.remote}|{person.occupation.physical}')