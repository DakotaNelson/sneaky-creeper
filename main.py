# This file will pull everything together:
# Take and process command line args -> read in data -> encode data (potentially multiple times) -> transmit data
# OR  Take and process command line args -> use transmit module's retrieve method to grab data -> write out data

import sys
import importlib
import argparse
#import inspect

# get list of available modules
# TODO make this detect modules instaed of being manual
channelOptions = ['twitter', 'exampleChannel']
encodingOptions = ['b64', 'exampleEncoder']

# command line arguments:
# you can input multiple transfer arguments, so -transfer and encoder will give a
# list of arguments. Need to change use encoder and use channel to loop
parser = argparse.ArgumentParser(description = 'Use social media as a tool for data exfiltration.')
subparsers = parser.add_subparsers(dest='subcommand')


#  subparser for encoder exploration
parser_encoders = subparsers.add_parser('encoders')
#parser_encoders.add_argument()

#  subparser for channel exploration
parser_channels = subparsers.add_parser('channels')
#parser_channels.add_argument()


#  subparser for sending data
parser_send = subparsers.add_parser('send')
parser_send.add_argument('--channel', '-c', dest = 'channelName', metavar="channel_name", action = 'store',
                             help = 'Choose a channel to transfer data over \
                             (e.g, --transfer twitter).', required = True)

parser_send.add_argument('--encoder', '-e', dest = 'encoderNames', metavar="encoder_name", nargs='+', action = 'store',
                             help = 'Choose one or more methods of encoding (done in order given).', required=True)

parser_send.add_argument('--input', '-i', help = 'Specify a file to read from, or leave blank for stdin.',\
                             metavar = 'filename', type = argparse.FileType('r'), default = '-')

#  subparser for fetching data
parser_receive = subparsers.add_parser('receive')

######### END ARG PARSER #########

def sendData(channelName, encoderNames, data):
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
    params = {'foo':'bar'} # eventually this will be command line params

    # TODO read from files with command line arg?
    #data = sys.stdin.read()
    for encoderName in encoderNames:
        moduleName = '.'.join(['encoders', encoderName])
        enc = importlib.import_module(moduleName)
        # This is a programmatic equivalent of:
        # from encoding import exampleEncoder as enc

        #required_args = inspect.getargspec(enc.encode)[0]
        #print(required_args)
        # this gives us the names of all the required arguments for the module

        args = enc.args()
        # make sure all required arguments are available
        for arg in args:
            if arg not in params:
                print("ERROR: argument {} is required for module {}.".format(arg, encoderName))
                print("Arg description: {}".format(args[arg]))
                sys.exit()

        data = enc.encode(data, params)

    print(data)

    # to use a channel:
    moduleName = '.'.join(['channels', channelName])
    chan = importlib.import_module(moduleName)

    # send some stuff
    chan.send(data, params)

    # TODO command line args for separate send and receive modes
    # receive some stuff
    resp = chan.receive(params)
    sys.stdout.write(str(resp))

############## RUN ##############
args = parser.parse_args()
d =  vars(args)

if args.subcommand == 'encoders':
    pass

if args.subcommand == 'channels':
    pass

if args.subcommand == 'send':
    channelName = d.get('channelName')
    encoderNames = d.get('encoderNames')
    data = d.get('input').read() # either a given file, or stdin
    sendData(channelName, encoderNames, data)

if args.subcommand == 'receive':
    pass
