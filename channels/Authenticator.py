from twython import Twython
from twython import Twython, TwythonError
#from oauth_dancey import oauth_dance

APP_KEY = input('App Key: ')
APP_SECRET = input('App Secret: ')
OAUTH_TOKEN = input('OAuth Token: ')
OAUTH_TOKEN_SECRET = input('OAuth Token Secret: ')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    twitter.update_status(status='Just a test, please ignore')
except TwythonError as e:
    print e  
    #TODO the current error with the code is a 401 unauthorized error. try to get the api to log in using just oauth codes.