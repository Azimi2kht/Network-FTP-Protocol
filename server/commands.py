import os
from random import randint

PORT_LOWER_BOUND = 3000
PORT_UPPER_BOUND = 50000


def respond(message):
    response = None
    random_port = randint(PORT_LOWER_BOUND, PORT_UPPER_BOUND)
    if message.upper() == 'LIST':
        response = '200: ok, port:' + str(random_port)
    else:
        response = '500: command unrecognized'

    return response


def list_files():
    listing = os.listdir(os.getcwd())
    listing_string = convert_list_to_str('&', listing)
    return listing_string


def convert_list_to_str(delimiter, listing):
    string = str()
    for item in listing:
        string += str(item)
        string += delimiter
    return string
