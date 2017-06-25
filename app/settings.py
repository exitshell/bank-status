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

PLAID_CLIENT_ID = env('PLAID_CLIENT_ID')

PLAID_SECRET = env('PLAID_SECRET')

PLAID_PUBLIC_KEY = env('PLAID_PUBLIC_KEY')

PLAID_ENV = env('PLAID_ENV')

PLAID_ACCESS_TOKEN = env('PLAID_ACCESS_TOKEN')

SAVINGS_ACCOUNT_MASK = env('SAVINGS_ACCOUNT_MASK')

CHECKING_ACCOUNT_MASK = env('CHECKING_ACCOUNT_MASK')


# Gunicorn settings.

bind = '{}:{}'.format(HOST, PORT)

workers = int(env('GUNICORN_WORKERS'))

timeout = int(env('GUNICORN_TIMEOUT'))

accesslog = os.path.join(BASE_DIR, 'logs', 'gunicorn-access.log')

errorlog = os.path.join(BASE_DIR, 'logs', 'gunicorn-error.log')

reload = True
