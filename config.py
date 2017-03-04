import os
import json
from datetime import timedelta

class Config(object):
    DEBUG = False

    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'https')

    MONGODB_DB = os.environ.get('MONGODB_DB', None)
    MONGODB_HOST = os.environ.get('MONGODB_HOST', None)
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 0))
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    DATABASE_ENCRYPTION_KEY = os.environ.get('DATABASE_ENCRYPTION_KEY', None) # must be 16, 24 or 32 bytes long
    
    CONDITION_TARGET = int(os.environ.get('CONDITION_TARGET', 0))
    CONDITION_STATEMENT = os.environ.get('CONDITION_STATEMENT', None)
    CONDITION_TERMS = os.environ.get('CONDITION_TERMS', None)
    CONDITION_BACKGROUND = os.environ.get('CONDITION_BACKGROUND', None) #markdown OK here
    CONDITION_RATES_LABEL = os.environ.get('CONDITION_RATES_LABEL', '')
    CONDITION_RATES_CSV = os.environ.get('CONDITION_RATES_CSV', '')
    CONDITION_POSTCODE_AREAS_CSV = os.environ.get('CONDITION_POSTCODE_AREAS_CSV', '') # set to False to allow any postcode
    
    TWILLIO_SID = os.environ.get('TWILLIO_SID', None)
    TWILLIO_AUTH_TOKEN = os.environ.get('TWILLIO_AUTH_TOKEN', None)
    TWILLIO_PHONE_NUMBER = os.environ.get('TWILLIO_PHONE_NUMBER', None)

    GOCARDLESS_ACCESS_TOKEN = os.environ.get('GOCARDLESS_ACCESS_TOKEN', None)
    GOCARDLESS_ENVIRONMENT = os.environ.get('GOCARDLESS_ENVIRONMENT', 'sandbox')

    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 20
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', None)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', None)
    CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', None)
    CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'beckton.tasks.send_halfway_message',
        'schedule': timedelta(seconds=30)
    },
}

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = "beckton_dev"
    SECRET_KEY = 'not-a-secret'
    DATABASE_ENCRYPTION_KEY = "DO NOT USE THIS KEY XXXXXXXXXXXX" #do not use this in production
    CONDITION_TARGET = 2
    CONDITION_STATEMENT = "I will join the union if 10 other widget makers will do the same"
    CONDITION_TERMS = "I work for Widget Makers LLP (Delaware)"
    CONDITION_BACKGROUND = "Employees of [Widget Makers](#) are not currently paid the living wage. If we can get enough people to join the union, we can campaign for change." #markdown OK here
    CONDITION_RATES_LABEL = "What hours do you work?"
    CONDITION_RATES_CSV = "4,Part-time (&pound;4 a month)|8,Full-time (&pound;8 a month)"
    CONDITION_POSTCODE_AREAS_CSV = "SW9,EC1,BR4" # set to False to allow any postcode
    TWILLIO_SID = os.environ.get('TWILLIO_SID', None)
    TWILLIO_AUTH_TOKEN = os.environ.get('TWILLIO_AUTH_TOKEN', None)
    TWILLIO_PHONE_NUMBER = os.environ.get('TWILLIO_PHONE_NUMBER', None)

    CELERY_BROKER_URL='mongodb://localhost:27017/beckton-tasks'
    CELERY_RESULT_BACKEND='mongodb://localhost:27017/beckton-tasks'
    CELERY_TIMEZONE = 'Europe/London'

class TestingConfig(DevelopmentConfig):
    TESTING = True
    MONGODB_SETTINGS = {'DB': "beckton_test"}
    WTF_CSRF_ENABLED = False