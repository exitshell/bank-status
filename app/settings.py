import os


def env(key, default=None):
    '''
    Get an environment variable.
    '''
    return os.environ.get(key, default)


# Application settings.

DEBUG = env('DEBUG', False) in ['True', 'true']

HOST = env('HOST')

PORT = int(env('PORT', ''))

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(PROJECT_DIR)

LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

AUTHORIZED_NUMBERS = env('AUTHORIZED_NUMBERS', '').split(',')

ACCOUNT_ID = env('TWILIO_ACC_ID')


# Gunicorn settings.

bind = '{}:{}'.format(HOST, PORT)

workers = int(env('GUNICORN_WORKERS'))

timeout = int(env('GUNICORN_TIMEOUT'))

accesslog = os.path.join(BASE_DIR, 'logs', 'gunicorn-access.log')

errorlog = os.path.join(BASE_DIR, 'logs', 'gunicorn-error.log')

reload = True
