import unittest
import json
import random
import string
import os

from unittest.case import SkipTest
import twython
from twython import TwythonError

from sneakers.channels import twitter
import sneakers
basePath = os.path.dirname(os.path.abspath(sneakers.__file__))

class TwitterTest(unittest.TestCase):

    def setUp(self):

        configPath = os.path.join(basePath, 'config', 'twitter-config.json')
        try:
            with open(configPath, 'rb') as f:
                s = json.loads(f.read())
        except:
            raise SkipTest("Could not access Twitter configuration file.")

        self.testParams = s['twitter']

        self.client = twython.Twython(
            self.testParams['key'],
            self.testParams['secret'],
            self.testParams['token'],
            self.testParams['tsecret'])

        self.randText = ''.join([random.choice(string.letters) for i in range(10)])

        self.channel = twitter.Twitter()

        for e in self.channel.params['sending']:
            if e.name in self.testParams:
                e.value = self.testParams[e.name]
        for e in self.channel.params['receiving']:
            if e.name in self.testParams:
                e.value = self.testParams[e.name]

    def test_send(self):
        try:
            self.channel.send(self.randText)
        except TwythonError as e:
            # something out of our control
            raise SkipTest("Twython error occurred: {}".format(e))

        resp = self.client.get_user_timeline(screen_name=self.testParams['name'])
        if 'text' in resp[0]:
            self.assertEqual(resp[0]['text'], self.randText)

    def test_receive(self):
        try:
            self.client.update_status(status=self.randText)
        except TwythonError as e:
            # something out of our control
            raise SkipTest("Twython error occurred: {}".format(e))

        tweets = self.channel.receive()
        self.assertEqual(tweets[0], self.randText)
