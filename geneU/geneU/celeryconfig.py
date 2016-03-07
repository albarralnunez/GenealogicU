# from os import environ


# BROKER_URL = environ['BROKER_URL']
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ENABLE_UTC = True
#  CELERY_TASK_SERIALIZER = 'json'
#  CELERY_RESULT_SERIALIZER = 'json'
#  CELERY_ACCEPT_CONTENT = ['json']
#  CELERY_TIMEZONE = 'Europe/Oslo'
