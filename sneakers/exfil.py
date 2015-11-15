#!/usr/bin/python2
import os
import math
import pkgutil
import base94

from sneakers.errors import ExfilChannel, ExfilEncoder

# basically opens a data tube
class Exfil():
    def __init__(self, channel_name, encoder_names):
        # the channel this tube will use
        self.channel = dict()
        # the list of encoders this tube will use - order matters
        self.encoders = list()

        if not type(encoder_names) is list:
            raise TypeError("Encoders must be specified as a list of string names.")
        if not type(channel_name) is str:
            raise TypeError("Channel name must be specified as a string.")

        channel_class = self.__import_module('sneakers.channels', channel_name)
        for encoder in encoder_names:
            encoder_class = self.__import_module('sneakers.encoders', encoder.lower())
            self.encoders.append({'name': encoder, 'class': encoder_class()})

        self.channel = {'name': channel_name, 'class': channel_class()}

    @staticmethod
    def __import_module(where, what):
        path = '.'.join([where, what])
        class_name = what.title()
        mod = __import__(path, fromlist=[class_name])
        mod_class = getattr(mod, class_name)
        return mod_class

    def set_channel_params(self, params):
        ch = self.channel['class']
        ch_name = self.channel['name']
        for k in params.keys():
            if 'sending' not in k and 'receiving' not in k:
                raise ExfilChannel('Missing \'sending\' and/or \'receiving\' for channel \'{}\''.format(ch_name))
            for param in ch.requiredParams[k]:
                if param not in params[k]:
                    raise ExfilChannel(
                        'Missing required parameter \'{}\' for channel \'{}\' ({}).'.format(param, ch_name, k))
                ch.set_params(params)

    def set_encoder_params(self, encoder_name, params):
        enc = None
        for encoder in self.encoders:
            if encoder['name'] == encoder_name:
                enc = encoder['class']
                break

        if not enc:
            raise ExfilEncoder('Encoder \'{}\' not found.'.format(encoder_name))

        for k in params.keys():
            if 'encode' not in k and 'decode' not in k:
                raise ExfilEncoder('Missing \'encode\' and/or \'decode\' for decoder \'{}\''.format(encoder_name))
            for param in enc.requiredParams[k]:
                if param not in params[k]:
                    raise ExfilEncoder(
                        'Missing required parameter \'{}\' for encoder \'{}\' ({}).'.format(param, encoder_name, k))
                enc.set_params(params)

    def get_channel_name(self):
        return self.channel['name']

    def get_encoder_names(self):
        return [x['name'] for x in self.encoders]

    def channel_config(self):
        return self.channel['class'].params

    def encoder_config(self, encoder_name):
        for encoder in self.encoders:
            if encoder['name'] == encoder_name:
                return encoder['class'].params

        raise ExfilEncoder('Encoder {} not found'.format(encoder_name))

    @staticmethod
    def list_encoders():
        # find the path to the encoders folder
        currentDir = os.path.dirname(os.path.abspath(__file__))
        encoders = os.path.join(currentDir, 'encoders')
        # then find all the modules
        encoders = pkgutil.iter_modules(path=[encoders])
        # and list them out
        encodingOptions = [modName for _, modName, _ in encoders]
        return encodingOptions

    def channel_meta(self):
        return self.channel['class'].meta

    def encoder_meta(self, encoder_name):
        for encoder in self.encoders:
            if encoder['name'] == encoder_name:
                return encoder['class'].meta

    @staticmethod
    def list_channels():
        # find the path to the channels folder
        currentDir = os.path.dirname(os.path.abspath(__file__))
        channels = os.path.join(currentDir, 'channels')
        # then find all the modules
        channels = pkgutil.iter_modules(path=[channels])
        # and list them out
        channelOptions = [modName for _, modName, _ in channels]
        return channelOptions

    def send(self, data):
        # header format: "lll nnn <data>"
        # where "lll" is a 3 character base94 number representing this packet's index
        # "nnn" is a 3 character base94 number representing the total number of packets in the fragment
        # 3 digits in base 94 = max of 830583 packets per fragment
        # this is 109,636,956 characters sent using Twitter,
        # or ~100ish MB assuming each character is one byte
        # pretty sure nobody will ever need more than 640k of ram

        encoded = data
        for encoder in self.encoders:
            encoded = encoder['class'].encode(encoded)

        chan = self.channel['class']

        header_length = 8  # reserve characters for the headers
        actual_length = chan.maxLength - header_length

        # determine the number of packets we'll need to send
        num_packets = int(math.ceil(len(encoded) / float(actual_length)))
        # '~~~' is the largest three digit number in base94
        max_packets = base94.decode("~~~")
        if num_packets > max_packets:
            raise ValueError("you can only send " + max_packets + " packets at a time")

        for i in range(num_packets):
            # wrap the data in headers
            packet = base94.encode(i) + " " + base94.encode(num_packets) + " " + ''.join(encoded[i * actual_length:(i+1)*actual_length])

            # double check that nothing went wrong
            if len(packet) > chan.maxLength:
                raise ValueError(self.channel['name'] + " cannot send more than " + str(chan.maxLength) + " characters")

            # send it off
            chan.send(packet)

    def receive(self):
        data = self.channel['class'].receive()

        # reassemble packets into segments
        segments = []
        buf = []

        # reverse the response so we get oldest first
        for msg in reversed(data):
            # strip and decode the headers
            tokenized = msg.split(" ", 2)
            packet_no = base94.decode(str(tokenized[0]))
            packet_total = base94.decode(str(tokenized[1]))
            msg = ''.join(tokenized[2:])

            if len(buf) == 0 and packet_no != 0:
                # we caught the end of a segment, drop this packet
                continue

            # if the packet number isn't equal to the total packets in the segment
            if packet_no + 1 != packet_total:
                # we haven't found the last packet yet, so append this one to the buffer
                buf.append(msg)
            else:
                # the buffer plus what we have here is a full sequence of packets
                buf.append(msg)
                # remove the headers and append all the data
                segment = ''.join(buf)
                segments.append(segment)
                buf = []

        if len(buf) != 0:
            raise AssertionError("Buffer is not empty: packet must be missing.")

        if not isinstance(segments, list):
            raise TypeError('Data must be returned from channel receive function as an array.')
            # the array is of individual 'packets' - i.e. metadata-wrapped bits of data
            # this allows for timestamping messages, sending large messages as multiple
            # fragments, etc.

        output = []
        # segments is an array of individual messages - decode them all one at a time
        for datum in segments:
            for encoder in reversed(self.encoders):
                # go through the encoder chain in reverse to decode the data
                # This allows decoders to be specified in the same order on both ends, and still work.
                datum = encoder['class'].decode(datum)
            # remove trailing newlines and spaces - they're added by some channels
            output.append(datum.rstrip())

        # write out the results
        return output
