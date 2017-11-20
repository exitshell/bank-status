import json

from flask import (
    Flask, jsonify, request, make_response
)

from . import bank
from . import settings
from .logging import configure_logging, log_bank_status_response
from .response import random_response, tw_response

# Initialize flask application.
app = Flask(import_name=__name__)
# Load flask configs from application settings.
app.config.from_object(settings)
# Disable strict slashes for flask routes.
app.url_map.strict_slashes = False
# Configure logging.
configure_logging(app)


@app.route('/', methods=['GET'])
def index():
    user_agent = request.user_agent
    response_data = {
        'server_name': 'Bank Status',
        'status': 'online',
        'request': {
            'ip_address': request.remote_addr,
            'user_agent': user_agent.string or ''
        },
    }
    app.logger.info(json.dumps(response_data, indent=2))
    return make_response(jsonify(response_data), 200)


@app.route('/status', methods=['POST'])
def status():
    required_fields = ['AccountSid', 'From', 'Body']

    # Check that the appropriate fields are given.
    for field in required_fields:
        if field not in request.values:
            return tw_response('Invalid Data')

    # Get POSTed values.
    account_id = request.values.get('AccountSid')
    from_number = request.values.get('From')
    body = request.values.get('Body').lower()

    # Validate the account id.
    if not account_id == settings.ACCOUNT_ID:
        return tw_response('Invalid Account Id')

    # Validate the imcoming phone number.
    if from_number not in settings.AUTHORIZED_NUMBERS:
        return tw_response('Phone not authorized')

    # Perform checking account status.
    if 'checking' in body:
        phone_message, log_message = bank.get_checking_balance()
        log_bank_status_response(request, 'Checking', log_message)
        return tw_response(phone_message)

    # Perform saving account status.
    elif 'saving' in body:
        phone_message, log_message = bank.get_savings_balance()
        log_bank_status_response(request, 'Savings', log_message)
        return tw_response(phone_message)

    # Return default response.
    message, response = random_response()
    log_bank_status_response(request, 'Default', message)
    return response
