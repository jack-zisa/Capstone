import hashlib

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

DEFAULT_PERSON_DATA: dict = {'water_intake': {}, 'heart_rate': {}, 'respiratory_rate': {}, 'active_energy_burned': {}, 'resting_energy_burned': {}, 'exercise_time': {}, 'audio_exposure': {}, 'heart_rate_variability': {}, 'oxygen_consumption': {}}

class Occupation:
    def __init__(self, city: str, state: str, remote: bool, physical: bool):
        self.city = city
        self.state = state
        self.remote = remote
        self.physical = physical

class Person:
    def __init__(self, age: int, gender: str, height: int, weight: int, data_source_type: str, data: dict, name: str, city: str, state: str, ethnicity: str, smokes: bool, occupation: Occupation):
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.data_source_type = data_source_type
        self.data = data
        self.uuid = hashlib.sha256(name.encode('utf-8')).hexdigest()
        self.city = city
        self.state = state
        self.ethnicity = ethnicity
        self.smokes = smokes
        self.occupation = occupation