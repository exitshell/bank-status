import random

from twilio.twiml.messaging_response import (
    MessagingResponse
)

default_responses = [
    'Hello from Bank Status',
    'Hi',
    'Hello',
    'Bank Status says Hello',
    'What would you like to check today?',
    'I\'m not a robot -- just kidding!',
    '[Bank Status]: Online',
    'This is the Bank Status Server'
]


def tw_response(message):
    resp = MessagingResponse().message(message)
    return str(resp)


def random_response():
    message = random.choice(default_responses)
    return message, tw_response(message)
