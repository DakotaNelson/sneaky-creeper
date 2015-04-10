#This module written by Gabriel Butterick and Bonnie Ishiguro 

from twython import Twython, TwythonError
import time



def send(data, params):
    APP_KEY = params['key']
    APP_SECRET = params['secret']
    OAUTH_TOKEN = params['token']
    OAUTH_TOKEN_SECRET = params['tsecret']
    SCREEN_NAME = params['name']

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME)
    twitter.update_status(status= data)
    print "Sending Complete"
    return

def receive(params):
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

