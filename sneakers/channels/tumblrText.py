# Written by Dakota Nelson (@jerkota)

from sneakers.modules import Channel, Parameter

import random
import string
import pytumblr

class Tumblrtext(Channel):
    description = """\
        Posts data to Tumblr as text.
    """

    params = {
        'sending': [
            Parameter('username', True, 'Your Tumblr username.'),
            Parameter('key', True, 'Your Tumblr OAuth key.'),
            Parameter('secret', True, 'Your Tumblr OAuth secret.'),
            Parameter('token', True, 'Your Tumblr OAuth token.'),
            Parameter('token_secret', True, 'Your Tumblr OAuth token secret.'),
                   ],
        'receiving': [
            Parameter('username', True, 'Your Tumblr username (also known as blog name).'),
            Parameter('key', True, 'Your Tumblr OAuth key.'),
            Parameter('secret', True, 'Your Tumblr OAuth secret.'),
            Parameter('token', True, 'Your Tumblr OAuth token.'),
            Parameter('token_secret', True, 'Your Tumblr OAuth token secret.'),
                     ]
        }

    maxLength = 50000
    # I don't think there's an actual limit, but let's pace ourselves

    maxHourly = 250/24
    # Can only post 250 times per day

    def send(self, data):
        client = pytumblr.TumblrRestClient(
                        self.param('sending', 'key'),
                        self.param('sending', 'secret'),
                        self.param('sending', 'token'),
                        self.param('sending', 'token_secret'),
                 )

        # create a random title for the post
        rand = ''.join(random.choice(string.lowercase) for i in range(20))
        client.create_text(self.param('sending', 'username'), state="private", slug=rand, title=rand, body=data)
        return

    def receive(self):
        client = pytumblr.TumblrRestClient(
                        self.param('receiving', 'key'),
                        self.param('receiving', 'secret'),
                        self.param('receiving', 'token'),
                        self.param('receiving', 'token_secret'),
                 )

        # https://www.tumblr.com/docs/en/api/v2#posts
        apiParams = {}
        apiParams['limit'] = 50
        apiParams['filter'] = 'raw'

        resp = client.posts(self.param('receiving', 'username'), **apiParams)

        posts = [post['body'] for post in resp['posts']]

        return posts
