"""
This channel writes the resultant data out to a file, or reads in from a file to receive.

Useful for testing, and also out of band transfer.
"""
import sys


class File():
    requiredParams = {
        'sending': {
            'filename': 'Name of the file to write data to.'
        },
        'receiving': {
            'filename': 'Name of the file to read data from.'
        }
    }

    max_length = sys.maxint
    # basically just "big"
    max_hourly = sys.maxint

    params = dict()

    def __init__(self):
        pass

    def set_params(self, params):
        for k in params.keys():
            self.params[k] = params[k]

    def send(self, data):
        sending_params = self.params['sending']
        with open(sending_params['filename'], 'w') as f:
            f.write(data)
        return

    def receive(self):
        receiving_params = self.params['receiving']
        with open(receiving_params['filename'], 'rb') as f:
            data = f.read()
        return [data]