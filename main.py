# This file will pull everything together:
# Take and process command line args -> read in data -> encode data (potentially multiple times) -> transmit data
# OR  Take and process command line args -> use transmit module's retrieve method to grab data -> write out data

import sys
import importlib
import argparse

# get list of available modules
# TODO make this detect modules instaed of being manual
channelOptions = ['twitter', 'exampleChannel']
encodingOptions = ['b64', 'exampleEncoder']

# command line arguments:
# you can input multiple transfer arguments, so -transfer and encoder will give a
# list of arguments. Need to change use encoder and use channel to loop
parser = argparse.ArgumentParser(description = 'Use social media as a tool for data exfiltration.')
parser.add_argument('--channel', '-c', dest = 'channelName', metavar="channel_name", action = 'store',
                             help = 'Choose a channel to transfer data over \
                             (e.g, --transfer twitter). Channels available: '+\
                             ", ".join(channelOptions), required = True)
parser.add_argument('--encode', '-e', dest = 'encoderNames', metavar="encoder_name", nargs='+', action = 'store',
                             help = 'Choose one or more methods of encoding (done in order given).\
                             Encoders available: ' + ", ".join(encodingOptions), required = True)

args = parser.parse_args()
d =  vars(args)
channelName = d.get('channelName')
encoderNames = d.get('encoderNames')

# ensure the passed modules are valid
if not channelName in channelOptions:
    print("ERROR: channel " + channelName + " does not exist.")
    sys.exit()

for encoderName in encoderNames:
    if not encoderName in encodingOptions:
        print("ERROR: encoder " + encoderName + " does not exist.")
        sys.exit()

# tell the user what we're going to do
print("")
print("Pipeline: " + "-> ".join(encoderNames) + "-> " + channelName)
print("")

# TODO set up command line params to pass to modules
params = {} # eventually this will be command line params

# TODO read in data from stdin or a file
data = 'this is my data'
for encoderName in encoderNames:
    moduleName = '.'.join(['encoders', encoderName])
    enc = importlib.import_module(moduleName)
    # This is a programmatic equivalent of:
    # from encoding import exampleEncoder as enc

    data = enc.encode(data, params)

print(data)

# to use a channel:
moduleName = '.'.join(['channels', channelName])
chan = importlib.import_module(moduleName)

# send some stuff
chan.send(data, params)

# TODO command line args for separate send and receive modes
# TODO write out received data to a file or stdout
# receive some stuff
resp = chan.receive(params)
print(resp)
