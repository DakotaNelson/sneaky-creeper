
import requests
from urllib.parse import parse_qs
import json
import time
#from modules import module
#from datetime import datetime
APP_KEY = input('App Key: ')
APP_SECRET = input('App Secret: ')
OAUTH_TOKEN = input('OAuth Token: ')
OAUTH_TOKEN_SECRET = input('OAuth Token Secret: ') 
  
class Twitter():
    ''' adapted from recon-ng Twitter module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        # APP_KEY = input('App Key: ')
        # APP_SECRET = input('App Secret: ')
        # OAUTH_TOKEN = input('OAuth Token: ')
        # OAUTH_TOKEN_SECRET = input('OAuth Token Secret: ')    
        return        

    def run(self, screen_name = 'EnglishmanJohny', count = 20):
        #url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        results = self.search_twitter_api({'screen_name': screen_name, 'count': count})

        for tweet in results:
            tweet_id = tweet['id_str']
            screen_name = tweet['user']['screen_name']
            message = tweet['text']
            print (message)
            #time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')



    def search_twitter_api(self, payload):
        headers = {'Authorization': 'Bearer %s' % (OAUTH_TOKEN)}
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        results = []
        while True:
            resp = self.request(url, content=payload, headers=headers)
            jsonobj = resp.json()
            #for item in ['error', 'errors']:
            #    if item in jsonobj:
            #        self.error(jsonobj[item])
            #        raise ModuleException(jsonobj[item])
            results += jsonobj['statuses']
            if 'next_results' in jsonobj['search_metadata']:
                max_id = parse_qs(jsonobj['search_metadata']['next_results'][1:])['max_id'][0]
                payload['max_id'] = max_id
                time.sleep(2) # don't hit the rate limit
                # TODO: make this more intelligent about using the full limit
                continue
            break
        return results


    def request(self, url, method="GET", timeout=None, payload=None, headers=None, cookiejar=None, auth=None, content='', redirect=True):
        if(method.lower() == "get"):
            r = requests.get(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
        elif(method.lower() == "post"):
            r = requests.post(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
        else:
            #raise ModuleException("Only GET and POST requests are currently supported.")
            return None

        # TODO: Other things that would be nice to support:
        #request.user_agent = self.global_options['user-agent']
        #request.debug = self.global_options['debug']
        #request.proxy = self.global_options['proxy']

        if r.status_code == requests.codes.ok:
            return r
        else:
            #raise ModuleException("Request to " + url + " returned with error " + str(r.status_code) + ".\n Response body: " + r.text)
            return None
if __name__ == "__main__":
    twitter = Twitter()

    twitter.run()
