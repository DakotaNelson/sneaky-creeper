# This file will pull everything together:
# Take and process command line args -> read in data -> encode data (potentially multiple times) -> transmit data
# OR  Take and process command line args -> use transmit module's retrieve method to grab data -> write out data

# command line arguments:
# you can input multiple transfer arguments, so -transfer and encoder will give a 
# list of arguments. Need to change use encoder and use channel to loop
import argparse
parser = argparse.ArgumentParser(description = 'Use social media as a tool\
								 for data exfiltration.', epilog = "Aw yee.")
parser.add_argument('-transfer', '-t', dest = 'channelName', action = 'append',
							 help = 'Choose location to transfer to \
							 (e.g, -transfer twitter). Channels that are supported:\
							  twitter (not really yet)', required = False) #change to True when done
parser.add_argument('-encode', '-e', dest = 'encoderName', action = 'append',
							 help = 'Choose methods of encoding (done in order given).\
							  Current methods: none :-(', required = False) #change to True when done
args = parser.parse_args()
d =  vars(args)
if d.get('channelName', -1) != -1: #if arguement is put in
	channelName = d['channelName']
if d.get('encoderName', -1) != -1:
	encoderName = d['encoderName']

print channelName, encoderName

# to use an encoder:
import importlib
encoderName = 'exampleEncoder'
moduleName = '.'.join(['encoders', encoderName])
enc = importlib.import_module(moduleName)
# This is a programmatic equivalent of:
# from encoding import exampleEncoder as enc

ret = enc.encode('this is my data')
print(ret)


# to use a channel:
channelName = 'exampleChannel'
moduleName = '.'.join(['channels', channelName])
chan = importlib.import_module(moduleName)

# send some stuff
chan.send("some data")

# receive some stuff
ret = chan.receive()
print(ret)
