# This module written by Gabriel Butterick and Bonnie Ishiguro

from sneakers.modules import Channel, Parameter

from twython import Twython, TwythonError
import time

class Twitter(Channel):
    description = """\
        Posts data to Twitter as a series of 280 character Tweets.
    """

    params = {
        'sending': [
            Parameter('key', True, 'Application key for Twitter API.'),
            Parameter('secret', True, 'Application secret for Twitter API.'),
            Parameter('token', True, 'OAuth token for Twitter API.'),
            Parameter('tsecret', True, 'OAuth token secret for Twitter API.'),
            Parameter('name', True, 'Screen name of Twitter account to post data to.')
        ],
        'receiving': [
            Parameter('key', True, 'Application key for Twitter API.'),
            Parameter('secret', True, 'Application secret for Twitter API.'),
            Parameter('token', True, 'OAuth token for Twitter API.'),
            Parameter('tsecret', True, 'OAuth token secret for Twitter API.'),
            Parameter('name', True, 'Screen name of Twitter account to post data to.')
        ]
    }

    # Can only post 100 times per hour or 1000 times per day
    max_length = 280
    max_hourly = 41

    def send(self, data):
        APP_KEY = self.param('sending', 'key')
        APP_SECRET = self.param('sending', 'secret')
        OAUTH_TOKEN = self.param('sending', 'token')
        OAUTH_TOKEN_SECRET = self.param('sending', 'tsecret')
        SCREEN_NAME = self.param('sending', 'name')

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter.update_status(status=data)

        return

    def receive(self):
        APP_KEY = self.param('receiving', 'key')
        APP_SECRET = self.param('receiving', 'secret')
        OAUTH_TOKEN = self.param('receiving', 'token')
        OAUTH_TOKEN_SECRET = self.param('receiving', 'tsecret')
        SCREEN_NAME = self.param('receiving', 'name')

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME, count=200, trim_user=True)
        timeline = user_timeline

        # TODO pagination
        # while len(user_timeline) == 200:
        #     max_id = user_timeline[-1]['id'] + 1
        #     user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME, count=200, trim_user=True, max_id=max_id)
        #     timeline.extend(user_timeline)

        tweets = []
        for x in reversed(timeline):
            if 'text' in x:
                tweets.append(x['text'].encode('utf-8'))

        return tweets

