import json

from flask import (
    Flask, jsonify, request, make_response
)

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
            'platform': user_agent.platform or '',
            'browser': user_agent.browser or '',
            'version': user_agent.version or '',
            'string': user_agent.string or ''
        },
    }
    app.logger.info(json.dumps(response_data, indent=2))
    return make_response(jsonify(response_data), 200)


@app.route('/status', methods=['POST'])
def status():
    required_fields = ['AccountSid', 'To', 'Body']

    # Check that the appropriate fields are given.
    for field in required_fields:
        if field not in request.values:
            return tw_response('Invalid Data')

    # Get values.
    account_id = request.values.get('AccountSid')
    from_number = request.values.get('From')
    body = request.values.get('Body').lower()

    # Validate the account id.
    if not account_id == settings.ACCOUNT_ID:
        return tw_response('Invalid Account Id')

    # Validate the imcoming phone number.
    if from_number not in settings.AUTHORIZED_NUMBERS:
        return tw_response('Phone not authorized')

    # Perform account status update.
    if 'checking' in body:
        # message = bank.status_checking()
        message = '[debug] status checking...'
        log_bank_status_response(request, 'Checking', message)
        return tw_response(message)
    elif 'savings' in body:
        # message = bank.status_savings()
        message = '[debug] status savings...'
        log_bank_status_response(request, 'Savings', message)
        return tw_response(message)

    # Return default response.
    message, response = random_response()
    log_bank_status_response(request, 'Default', message)
    return response