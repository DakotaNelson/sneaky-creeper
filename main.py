# This file will pull everything together:
# Take and process command line args -> read in data -> encode data (potentially multiple times) -> transmit data
# OR  Take and process command line args -> use transmit module's retrieve method to grab data -> write out data

import importlib

params = {} # eventually this will be command line params

# to use an encoder:
encoderName = 'exampleEncoder'
moduleName = '.'.join(['encoders', encoderName])
enc = importlib.import_module(moduleName)
# This is a programmatic equivalent of:
# from encoding import exampleEncoder as enc

ret = enc.encode('this is my data', params)
print(ret)


# to use a channel:
channelName = 'exampleChannel'
moduleName = '.'.join(['channels', channelName])
chan = importlib.import_module(moduleName)

# send some stuff
chan.send("some data", params)

# receive some stuff
ret = chan.receive(params)
print(ret)
