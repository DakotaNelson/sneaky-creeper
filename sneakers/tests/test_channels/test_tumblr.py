import unittest
import json
import random
import string
import os

from unittest.case import SkipTest

import pytumblr
from sneakers.channels import tumblrText

import sneakers
basePath = os.path.dirname(os.path.abspath(sneakers.__file__))

class TestTumblr(unittest.TestCase):

    # number of posts made by tests that need to be cleaned up
    toDelete = 0

    def setUp(self):
        configPath = os.path.join(basePath, 'config', 'tumblr-config.json')
        try:
            with open(configPath, 'rb') as f:
                s = json.loads(f.read())
        except:
            raise SkipTest("Could not access Tumblr configuration file.")

        self.params = s['tumblrText']

        self.client = pytumblr.TumblrRestClient(
                        self.params['key'],
                        self.params['secret'],
                        self.params['token'],
                        self.params['token_secret'],
                 )

        self.randText = ''.join([random.choice(string.letters) for i in range(10)])

        self.apiParams = {}
        self.apiParams['filter'] = 'raw'

        from sneakers.channels.tumblrText import Tumblrtext

        self.chan = Tumblrtext()
        self.chan.params['sending'] = self.params
        self.chan.params['receiving'] = self.params

    def tearDown(self):
        resp = self.client.posts(self.params['username'])
        for i in range(self.toDelete):
            self.client.delete_post(self.params['username'], resp['posts'][i]['id'])
            self.toDelete -= 1

    def test_send(self):
        ''' test that the Tumblr module can send '''

        self.chan.send(self.randText)

        resp = self.client.posts(self.params['username'], **self.apiParams)
        self.assertEqual(resp['posts'][0]['body'], self.randText)

        self.toDelete += 1

    def test_receive(self):
        ''' test that the Tumblr module can receive '''
        self.client.create_text(self.params['username'],
                                state="private",
                                slug=self.randText,
                                title="unit test",
                                body=self.randText)
        self.toDelete += 1

        posts = self.chan.receive()

        self.assertEqual(posts[0], self.randText)


if __name__ == '__main__':
    unittest.main()
