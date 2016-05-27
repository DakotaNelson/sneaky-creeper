from sneakers.modules import Channel

from twython import Twython, TwythonError
import time

class Twitter(Channel):

    info = {
        "name": "Twitter",
        "author": "Gabriel Butterick & Bonnie Ishiguro",
        "description": "Posts data to Twitter as a series of 140 character Tweets",
        "comments": []
    }

    requiredParams = {
        'sending': {
            'key': 'Application key for Twitter API.',
            'secret': 'Application secret for Twitter API.',
            'token': 'OAuth token for Twitter API.',
            'tsecret': 'OAuth token secret for Twitter API.',
            'name': 'Screen name of Twitter account to post data to.'
        },
        'receiving': {
            'key': 'Application key for Twitter API.',
            'secret': 'Application secret for Twitter API.',
            'token': 'OAuth token for Twitter API.',
            'tsecret': 'OAuth token secret for Twitter API.',
            'name': 'Screen name of Twitter account to post data to.'
        }
    }

    # Can only post 100 times per hour or 1000 times per day
    max_length = 140
    max_hourly = 100

    def send(self, data):
        send_params = self.reqParams['sending']
        APP_KEY = send_params['key']
        APP_SECRET = send_params['secret']
        OAUTH_TOKEN = send_params['token']
        OAUTH_TOKEN_SECRET = send_params['tsecret']

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter.update_status(status=data)

        return

    def receive(self):
        rec_params = self.reqParams['receiving']

        APP_KEY = rec_params['key']
        APP_SECRET = rec_params['secret']
        OAUTH_TOKEN = rec_params['token']
        OAUTH_TOKEN_SECRET = rec_params['tsecret']
        SCREEN_NAME = rec_params['name']

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        # let's throw the exception
        user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME)

        tweets = []
        for x in user_timeline:
            if 'text' in x:
                tweets.append(x['text'])

        return tweets

