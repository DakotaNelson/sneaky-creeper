

from modules import module
from datetime import datetime

class Twitter(module.Module):
    ''' adapted from recon-ng Twitter module
        written by Tim Tomes (@LaNMaSteR53) '''

    def __init__(self):
        return

    def run(self, locname, lat, lon, rad):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        count = 0
        pins = []
        self.output('Collecting data from Twitter...')
        point = str(lat) + "," + str(lon)
        results = self.search_twitter_api({'q':'', 'geocode': '%s,%dkm' % (point, rad), 'count': '100'})

        for tweet in results:
            if not tweet['geo']:
                continue
            tweet_id = tweet['id_str']
            source = 'Twitter'
            screen_name = tweet['user']['screen_name']
            profile_name = tweet['user']['name']
            profile_url = 'https://twitter.com/%s' % screen_name
            media_url = 'https://twitter.com/%s/statuses/%s' % (screen_name, tweet_id)
            thumb_url = tweet['user']['profile_image_url_https']
            message = tweet['text']
            latitude = tweet['geo']['coordinates'][0]
            longitude = tweet['geo']['coordinates'][1]
            time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
            count += 1
        self.addPins(locname, pins)
        #self.verbose('%s tweets processed.' % (len(results)))
        #self.summarize(new, count)


