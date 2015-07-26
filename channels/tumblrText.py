'''
Posts text to tumblr.

Written by Dakota Nelson (@jerkota)
'''

import random
import string
import pytumblr

requiredParams = {
    'sending': {
        'username': 'Your Tumblr username.',
        'key': 'Your Tumblr OAuth key.',
        'secret': 'Your Tumblr OAuth secret.',
        'token': 'Your Tumblr OAuth token.',
        'token_secret': 'Your Tumblr OAuth token secret.',
               },
    'receiving': {
        'username': 'Your Tumblr username (also known as blog name).',
        'key': 'Your Tumblr OAuth key.',
        'secret': 'Your Tumblr OAuth secret.',
        'token': 'Your Tumblr OAuth token.',
        'token_secret': 'Your Tumblr OAuth token secret.',
                 }
    }

def send(data, params):
    client = pytumblr.TumblrRestClient(
                    params['key'],
                    params['secret'],
                    params['token'],
                    params['token_secret'],
             )

    # create a random title for the post
    rand = ''.join(random.choice(string.lowercase) for i in range(20))
    client.create_text(params['username'], state="private", slug=rand, title=rand, body=data)
    return

def receive(params):
    client = pytumblr.TumblrRestClient(
                    params['key'],
                    params['secret'],
                    params['token'],
                    params['token_secret'],
             )

    # https://www.tumblr.com/docs/en/api/v2#posts
    apiParams = {}
    apiParams['limit'] = 50
    apiParams['filter'] = 'raw'

    resp = client.posts(params['username'], **apiParams)

    posts = [post['body'] for post in resp['posts']]

    return posts
