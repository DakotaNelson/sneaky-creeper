import unittest
import json
import random
import string

import pytumblr
from sneakers.channels import tumblrText

class TestTumblr(unittest.TestCase):

    # number of posts made by tests that need to be cleaned up
    toDelete = 0

    def setUp(self):
        with open('../config/tumblr-config.json', 'rb') as f:
            s = json.loads(f.read())

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

    def tearDown(self):
        resp = self.client.posts(self.params['username'])
        for i in range(self.toDelete):
            self.client.delete_post(self.params['username'], resp['posts'][i]['id'])
            self.toDelete -= 1

    def test_send(self):
        ''' test that the Tumblr module can send '''
        tumblrText.send(self.randText, self.params)

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

        posts = tumblrText.receive(self.params)

        self.assertEqual(posts[0], self.randText)


if __name__ == '__main__':
    unittest.main()
