#This module written by Gabriel Butterick and Bonnie Ishiguro

import time

description = "Posts data to Twitter as a series of 140 character Tweets."

# TODO add optional params?
requiredParams = {
    'sending': {
       'key':'Application key for Twitter API.',
       'secret': 'Application secret for Twitter API.',
       'token': 'OAuth token for Twitter API.',
       'tsecret': 'OAuth token secret for Twitter API.',
       'name': 'Screen name of Twitter account to post data to.'
               },
    'receiving': {
       'key':'Application key for Twitter API.',
       'secret': 'Application secret for Twitter API.',
       'token': 'OAuth token for Twitter API.',
       'tsecret': 'OAuth token secret for Twitter API.',
       'name': 'Screen name of Twitter account to post data to.'
                 }
    }

dependencies = ['twython']

def send(data, params):
    from twython import Twython, TwythonError
    APP_KEY = params['key']
    APP_SECRET = params['secret']
    OAUTH_TOKEN = params['token']
    OAUTH_TOKEN_SECRET = params['tsecret']
    SCREEN_NAME = params['name']

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    tweets = [data[i:i+140] for i in range(0, len(data), 140)]
    for tweet in tweets:
      twitter.update_status(status=tweet)

    return

def receive(params):
    from twython import Twython, TwythonError
    APP_KEY = params['key']
    APP_SECRET = params['secret']
    OAUTH_TOKEN = params['token']
    OAUTH_TOKEN_SECRET = params['tsecret']
    SCREEN_NAME = params['name']

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    try:
        user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME)
    except TwythonError as e:
        print(e)

    tweets = []
    for x in user_timeline:
        if 'text' in x:
            tweets.append(x['text'])

    return tweets

