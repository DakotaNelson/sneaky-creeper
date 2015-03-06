# from twython import Twython
# from twython import Twython, TwythonError
from map.models import Keys, Pushpin, Location
from django.core.exceptions import ValidationError
from django.db import models
import requests
from urllib.parse import parse_qs
import json
import re
import pytz
import time
from datetime import datetime
APP_KEY = input('App Key: ')
APP_SECRET = input('App Secret: ')
OAUTH_TOKEN = input('OAuth Token: ')
OAUTH_TOKEN_SECRET = input('OAuth Token Secret: ')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#results = self.search_twitter_api({'q':'', 'geocode': '%s,%dkm' % (point, rad), 'count': '100'})

class ModuleException(Exception):
    pass

class Colors(object):
    N = '\033[m' # native
    R = '\033[31m' # red
    G = '\033[32m' # green
    O = '\033[33m' # orange
    B = '\033[34m' # blue

class Module:
    def __init__(self):
        return

	def search_twitter_api(self, payload):
	    headers = {'Authorization': 'Bearer %s' % (OAUTH_TOKEN)
	    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
	    results = []
	    while True:
	        resp = self.request(url, content=payload, headers=headers)
	        jsonobj = resp.json()
	        for item in ['error', 'errors']:
	            if item in jsonobj:
	                self.error(jsonobj[item])
	                raise ModuleException(jsonobj[item])
	        results += jsonobj['statuses']
	        if 'next_results' in jsonobj['search_metadata']:
	            max_id = parse_qs(jsonobj['search_metadata']['next_results'][1:])['max_id'][0]
	            payload['max_id'] = max_id
	            time.sleep(2) # don't hit the rate limit
	            # TODO: make this more intelligent about using the full limit
	            continue
	        break
	    return results

	def error(self, line):
	    ''' formats and presents errors '''
	    if not re.search('[.,;!?]$', line):
	        line += '.'
	    line = line[:1].upper() + line[1:]
	    print('%s[!] %s%s' % (Colors.R, line, Colors.N))


	 def request(self, url, method="GET", timeout=None, payload=None, headers=None, cookiejar=None, auth=None, content='', redirect=True):
	    if(method.lower() == "get"):
	        r = requests.get(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
	    elif(method.lower() == "post"):
	        r = requests.post(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
	    else:
	        raise ModuleException("Only GET and POST requests are currently supported.")
	        return None

	    # TODO: Other things that would be nice to support:
	    #request.user_agent = self.global_options['user-agent']
	    #request.debug = self.global_options['debug']
	    #request.proxy = self.global_options['proxy']

	    if r.status_code == requests.codes.ok:
	        return r
	    else:
	        raise ModuleException("Request to " + url + " returned with error " + str(r.status_code) + ".\n Response body: " + r.text)
	        return None




#try:
#    twitter.update_status(status='Just a test, please ignore')
#except TwythonError as e:
#    print e  
    #TODO the current error with the code is a 401 unauthorized error. try to get the api to log in using just oauth codes.