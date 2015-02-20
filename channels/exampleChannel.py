# To create a new channel, create a new file named yourChannelName.py that has the following functions:

import time

def send(data):
    for _ in range(3):
        print("Simulating sending data...")
        time.sleep(1)
    return

def receive():
    return "there would be some data here"
