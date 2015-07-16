'''
To create a new channel, create a new file named yourChannelName.py that has the following functions:
'''

import time

requiredParams = {
    'sending': {
        # 'param_name': 'Brief description of the parameter.'
               },
    'receiving': {
        # 'param_name': 'Brief description of the parameter.'
                 }
    }

def send(data, params):
    for _ in range(3):
        print("Simulating sending data...")
        time.sleep(1)
    return

def receive(params):
    return ["there would be some data here", "and here as well"]
