# This file will contain a class that can be inherited from to create an encoding module - pass data to it and it will return the encoded version of that data.

import time

def send(data):
    for _ in range(3):
        print("Simulating sending data...")
        time.sleep(1)
    return

def receive():
    return "there would be some data here"
