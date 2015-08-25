'''
This channel writes the resultant data out to a file, or reads in from a file to receive.

Useful for testing, and also out of band transfer.
'''

import sys

################### Attributes ###################

requiredParams = {
    'sending': {
        'filename': 'Name of the file to write data to.'
               },
    'receiving': {
        'filename': 'Name of the file to read data from.'
                 }
    }

maxLength = sys.maxint
# basically just "big"

maxHourly = sys.maxint

################### Functions ###################

def send(data, params):
    #print("Writing data to " + params['filename'] + "...")
    with open(params['filename'] , 'w') as f:
        f.write(data)
    #print("Done.")
    return

def receive(params):
    #print("Reading data from " + params['filename'] + "...")
    with open(params['filename'], 'rb') as f:
        data = f.read()
    #print("Done.")
    return [data]
