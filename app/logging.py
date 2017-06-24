import datetime
import json
import logging
from logging.handlers import RotatingFileHandler

from flask import current_app


def configure_logging(app):
    '''
    Configure logging for the application.
    '''

    # Create a file handler and set its level to DEBUG.
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10000,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)

    # Create a log formatter and set it to the file handler.
    format_str = (
        '[%(asctime)s] {%(filename)s:%(lineno)d} '
        '%(levelname)s - %(message)s'
    )
    formatter = logging.Formatter(format_str, '%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger.
    app.logger.addHandler(file_handler)

    # Set the logger's level to DEBUG.
    app.logger.setLevel(logging.DEBUG)


def log_bank_status_response(request, mode, response_message):
    '''
    Log information about the request and the generated response.
    '''
    data = request.values
    response_data = {
        'datetime': datetime.datetime.now().strftime('%b %d, %Y %H:%M:%S %p'),
        'phone_number': data.get('From'),
        'body': data.get('Body'),
        'twilio': {
            'SmsMessageSid': data.get('SmsMessageSid'),
            'SmsSid': data.get('SmsSid'),
            'MessageSid': data.get('MessageSid'),
            'AccountSid': data.get('AccountSid'),
        },
        'mode': mode,
        'response': response_message
    }
    current_app.logger.info(json.dumps(response_data, indent=2))
