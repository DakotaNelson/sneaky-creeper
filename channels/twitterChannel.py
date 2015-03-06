import requests
from urllib.parse import parse_qs, urlparse
import json
import time

from twython import Twython

class Twitter():
    ''' adapted from recon-ng Twitter module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):   
        return        

    def run(self, screen_name, count=20):
        results = self.search_twitter_api({'screen_name': screen_name, 'count': count})

        for tweet in results:
            tweet_id = tweet['id_str']
            screen_name = tweet['user']['screen_name']
            message = tweet['text']
            print (message)

    def search_twitter_api(self, payload):
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        
        #host = urlparse(url).hostname
        headers = {'Authorization': 'Bearer ' + OAUTH_TOKEN}
        
        results = []
        
        print("Payload: ", payload)
        print("Headers: ", headers)

        while True:
            resp = self.request(url, content=payload, headers=headers)
            print('Response: ', resp)
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
                continue
            break
        return results


    def request(self, url, method="GET", timeout=None, payload=None, headers=None, cookiejar=None, auth=None, content='', redirect=True):
        
        if(method.lower() == "get"):
            r = requests.get(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
            print("GET, Response: ", r)
        elif(method.lower() == "post"):
            r = requests.post(url, params=content, headers=headers, cookies=cookiejar, auth=auth, data=payload, timeout=timeout)
        else:
            #raise ModuleException("Only GET and POST requests are currently supported.")
            return None

        print("Status Code: ", r.status_code) # Returning Code 401 - "Unauthorized"

        if r.status_code == requests.codes.ok:
            return r
        else:
            #raise ModuleException("Request to " + url + " returned with error " + str(r.status_code) + ".\n Response body: " + r.text)
            return None
if __name__ == "__main__":
    
    APP_KEY = input('App Key: ')
    APP_SECRET = input('App Secret: ')
    OAUTH_TOKEN = input('OAuth Token: ')
    OAUTH_TOKEN_SECRET = input('OAuth Token Secret: ')
    screen_name = input('Screen Name: ')

    twitter = Twitter()
    twitter.run()
