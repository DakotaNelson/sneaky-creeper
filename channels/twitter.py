from twython import Twython, TwythonError
import time

# TODO add optional params?
requiredParams = {
    'sending': {
       'app_key':'Application key for Twitter API.',
       'app_secret': 'Application secret for Twitter API.',
       'oauth_token': 'OAuth token for Twitter API.',
       'oauth_token_secret': 'OAuth token secret for Twitter API.',
       'screen_name': 'Screen name of Twitter account to post data to.'
               },
    'receiving': {
       'app_key':'Application key for Twitter API.',
       'app_secret': 'Application secret for Twitter API.',
       'oauth_token': 'OAuth token for Twitter API.',
       'oauth_token_secret': 'OAuth token secret for Twitter API.',
       'screen_name': 'Screen name of Twitter account to post data to.'
                 }
    }

def send(data, params):
    APP_KEY = params['app_key']
    APP_SECRET = params['app_secret']
    OAUTH_TOKEN = params['oauth_token']
    OAUTH_TOKEN_SECRET = params['oauth_token_secret']
    SCREEN_NAME = params['screen_name']

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME)
    twitter.update_status(status= data)
    print "Sending Complete"
    return

def receive(params):
    APP_KEY = params['app_key']
    APP_SECRET = params['app_secret']
    OAUTH_TOKEN = params['oauth_token']
    OAUTH_TOKEN_SECRET = params['oauth_token_secret']
    SCREEN_NAME = params['screen_name']

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

