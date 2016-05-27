# Written by Dakota Nelson (@jerkota)

from sneakers.modules import Channel

import random
import string
import pytumblr

class Tumblrtext(Channel):
    description = """\
        Posts data to Tumblr as text.
    """

    requiredParams = {
        'sending': {
            'username': 'Your Tumblr username.',
            'key': 'Your Tumblr OAuth key.',
            'secret': 'Your Tumblr OAuth secret.',
            'token': 'Your Tumblr OAuth token.',
            'token_secret': 'Your Tumblr OAuth token secret.',
                   },
        'receiving': {
            'username': 'Your Tumblr username (also known as blog name).',
            'key': 'Your Tumblr OAuth key.',
            'secret': 'Your Tumblr OAuth secret.',
            'token': 'Your Tumblr OAuth token.',
            'token_secret': 'Your Tumblr OAuth token secret.',
                     }
        }

    maxLength = 50000
    # I don't think there's an actual limit, but let's pace ourselves

    maxHourly = 250/24
    # Can only post 250 times per day

    def send(self, data):
        params = self.reqParams['sending']
        client = pytumblr.TumblrRestClient(
                        params['key'],
                        params['secret'],
                        params['token'],
                        params['token_secret'],
                 )

        # create a random title for the post
        rand = ''.join(random.choice(string.lowercase) for i in range(20))
        client.create_text(params['username'], state="private", slug=rand, title=rand, body=data)
        return

    def receive(self):
        params = self.reqParams['receiving']
        client = pytumblr.TumblrRestClient(
                        params['key'],
                        params['secret'],
                        params['token'],
                        params['token_secret'],
                 )

        # https://www.tumblr.com/docs/en/api/v2#posts
        apiParams = {}
        apiParams['limit'] = 50
        apiParams['filter'] = 'raw'

        resp = client.posts(params['username'], **apiParams)

        posts = [post['body'] for post in resp['posts']]

        return posts
