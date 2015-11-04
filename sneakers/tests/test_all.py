import unittest
import json
import random
import string
import os

from unittest.case import SkipTest
from nose.tools import assert_equals
from functools import partial

import sneakers
basePath = os.path.dirname(os.path.abspath(sneakers.__file__))

def unit_channel(channel, data):
    """ Test a channel. """

    t = sneakers.Exfil(channel, [])

    # get parameters from config folder
    configPath = os.path.join(basePath, 'config', '{}-config.json'.format(channel))

    try:
        with open(configPath) as f:
            params = json.loads(f.read())
    except:
        raise SkipTest('could not load configuration file for {}'.format(channel))

    t.set_channel_params({'sending': params[channel]})
    t.set_channel_params({'receiving': params[channel]})

    t.send(data)

    got = t.receive()
    assert_equals(got[0], data)
        #'Failed in \'{}\' channel with payload of "{}"'.format(channel, data))

######################################################
#################### Actual Tests ####################
######################################################

def test_AllChannelsBasic():
    """ Test all channels with basic alphanumeric characters. """
    # need to have some random; a few platforms (looking at you, Twitter) have
    # issues if you post the same thing multiple times
    rand = ''.join([random.choice(string.letters) for i in range(5)])

    data = ''.join([string.letters, string.digits, rand])

    for channel in sneakers.Exfil.list_channels() :
        f = partial(unit_channel, channel, data)
        f.description = "Test the {} channel with basic alphanumeric characters.".format(channel)
        yield (f, )

def test_AllChannelsAdvanced():
    """ Test all channels with a full range of printable characters. """
    # need to have some random; a few platforms (looking at you, Twitter) have
    # issues if you post the same thing multiple times
    rand = ''.join([random.choice(string.letters) for i in range(5)])

    data = ''.join([string.printable, rand])

    for channel in sneakers.Exfil.list_channels() :
        f = partial(unit_channel, channel, data)
        f.description = "Test the {} channel with the full range of printable characters.".format(channel)
        yield (f, )

def test_AllChannelsLong():
    """ Test all channels with long messages. """
    data = ''.join([random.choice(string.letters) for i in range(500000)])

    for channel in sneakers.Exfil.list_channels() :
        f = partial(unit_channel, channel, data)
        f.description = "Test the {} channel with a very long message.".format(channel)
        yield (f, )

