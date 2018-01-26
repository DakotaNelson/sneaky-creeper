import unittest
import json
import random
import string
import os

from unittest.case import SkipTest
from nose.tools import assert_equals, assert_in
from functools import partial

from twython import TwythonError

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

    t.set_channel_params({'sending': params[channel],
                          'receiving': params[channel]})

    try:
        t.send(data)
    except TwythonError as e:
        # something out of our control
        raise SkipTest("Twython error occurred: {}".format(e))

    got = t.receive()
    if len(data) > 300:
        assert_in(data, got,
          'Failed in assertion for the \'{}\' channel with a very large payload.'.format(channel))
    else:
        assert_in(data, got)

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

    our_printable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ "
    # excludes \t\r\n
    data = ''.join([our_printable, rand])

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

