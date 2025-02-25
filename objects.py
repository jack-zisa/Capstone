import hashlib
import auth

# Data source keys
APPLE_WATCH: str = 'apple_watch'
FITBIT: str = 'fitbit'

# Data keys
HEART_RATE: str = 'HKQuantityTypeIdentifierHeartRate'
HEART_RATE_VARIABILITY: str = 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN'
ACTIVITY_WALKING: str = 'HKWorkoutActivityTypeWalking'
ACTIVITY_TENNIS: str = 'HKWorkoutActivityTypeTennis'
OXYGEN_CONSUMPTION: str = 'HKQuantityTypeIdentifierVO2Max'
AUDIO_EXPOSURE: str = 'HKQuantityTypeIdentifierHeadphoneAudioExposure'
EXERCISE_TIME: str = 'HKQuantityTypeIdentifierAppleExerciseTime'
ACTIVE_ENERGY_BURNED: str = 'HKQuantityTypeIdentifierActiveEnergyBurned'
RESTING_ENERGY_BURNED: str = 'HKQuantityTypeIdentifierBasalEnergyBurned'
RESPIRATORY_RATE: str = 'HKQuantityTypeIdentifierRespiratoryRate'
WATER_INTAKE: str = 'HKQuantityTypeIdentifierDietaryWater'

class Occupation:
    def __init__(self, city: str, state: str, remote: bool, physical: bool):
        self.city = city
        self.state = state
        self.remote = remote
        self.physical = physical

class Person:
    def __init__(self, age: int, gender: str, height: int, weight: int, data_source_type: str, name: str, city: str, state: str, ethnicity: str, smokes: bool, occupation: Occupation):
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.data_source_type = data_source_type
        self.uuid = hashlib.sha256(name.encode('utf-8')).hexdigest()
        self.city = city
        self.state = state
        self.ethnicity = ethnicity
        self.smokes = smokes
        self.occupation = occupation
    
    def __str__(self):
        return f'{self.age}|{self.gender}|{self.height}|{self.weight}|{self.data_source_type}|{self.uuid}|{self.city}|{self.state}|{self.ethnicity}|{self.smokes}'
    
    def fromRequest():
        data: dict = auth.request('https://api.fitbit.com/1/user/-/profile.json')['user']
        return Person(data['age'], data['gender'][0], data['height'], data['weight'], FITBIT, f'{data['firstName']} {data['lastName']}', '', '', '', False, Occupation('', '', False, False))

class HealthRecord:
    def __init__(self, person_id: str, timestamp: str,
                 heart_rate: int = None, water_intake: float = None, respiratory_rate: float = None, resting_energy_burned: float = None,
                 active_energy_burned: float = None, audio_exposure: float = None, oxygen_consumption: float = None,
                 heart_rate_variability: float = None, sleep_blood_oxygen_saturation: float = None, oxygen_saturation: float = None,
                 sleep_score: int = None, sleep_time: int = None, sleeping_heart_rate: int = None, restlessness: float = None, stress_score: int = None,
                 floors: int = None, steps: int = None, swim_lengths: int = None, stroke_count: int = None, swim_stroke: str = None, calories: float = None,
                 altitude: int = None, heart_rate_zone: str = None, distance: float = None):
        self.person_id = person_id
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.water_intake = water_intake
        self.respiratory_rate = respiratory_rate
        self.resting_energy_burned = resting_energy_burned
        self.active_energy_burned = active_energy_burned
        self.audio_exposure = audio_exposure
        self.oxygen_consumption = oxygen_consumption
        self.heart_rate_variability = heart_rate_variability
        self.sleep_blood_oxygen_saturation = sleep_blood_oxygen_saturation
        self.oxygen_saturation = oxygen_saturation
        self.sleep_score = sleep_score
        self.sleep_time = sleep_time
        self.sleeping_heart_rate = sleeping_heart_rate
        self.restlessness = restlessness
        self.stress_score = stress_score
        self.floors = floors
        self.steps = steps
        self.swim_lengths = swim_lengths
        self.stroke_count = stroke_count
        self.swim_stroke = swim_stroke
        self.calories = calories
        self.altitude = altitude
        self.heart_rate_zone = heart_rate_zone
        self.distance = distance
    
    def __str__(self):
        return f'{self.person_id}|{self.timestamp}|{'' if self.heart_rate is None else self.heart_rate}|{'' if self.water_intake is None else self.water_intake}|{'' if self.respiratory_rate is None else self.respiratory_rate}|{'' if self.resting_energy_burned is None else self.resting_energy_burned}|{'' if self.active_energy_burned is None else self.active_energy_burned}|{'' if self.audio_exposure is None else self.audio_exposure}|{'' if self.oxygen_consumption is None else self.oxygen_consumption}|{'' if self.heart_rate_variability is None else self.heart_rate_variability}|{'' if self.sleep_blood_oxygen_saturation is None else self.sleep_blood_oxygen_saturation}|{'' if self.oxygen_saturation is None else self.oxygen_saturation}|{'' if self.sleep_score is None else self.sleep_score}|{'' if self.sleep_time is None else self.sleep_time}|{'' if self.sleeping_heart_rate is None else self.sleeping_heart_rate}|{'' if self.restlessness is None else self.restlessness}|{'' if self.stress_score is None else self.stress_score}|{'' if self.floors is None else self.floors}|{'' if self.steps is None else self.steps}|{'' if self.swim_lengths is None else self.swim_lengths}|{'' if self.stroke_count is None else self.stroke_count}|{'' if self.swim_stroke is None else self.swim_stroke}|{'' if self.calories is None else self.calories}|{'' if self.altitude is None else self.altitude}|{'' if self.heart_rate_zone is None else self.heart_rate_zone}|{'' if self.distance is None else self.distance}\n'