# Written by Andrew Pan
from modules import Channel
import urllib, urllib2


class Pastebin(Channel):
	def __init__(self):
		self.pasteKey = ''

	description = """\
        Posts data to Pastebin as plaintext.
    """
	requiredParams = {
    	'sending': {
    		'api_dev_key': 'Developer key for Pastebin API'
    	},
    	'receiving': {
    	}
    }

	def send(self, data):
		send_params = self.params['sending']
		paste_url = 'http://pastebin.com/api/api_post.php'
		values = {'api_dev_key': send_params['api_dev_key'],  # personal API key
          'api_paste_code': data,  # message body
          'api_paste_private': '1',  # 0 = public, 1 = unlisted, 2 = private
          'api_paste_name': '',  # filename
          'api_paste_expire_date': '10M',  # 10 minutes (#1W for 1 week)
          'api_paste_format': 'text',  # plaintext
          'api_option': 'paste'}  # tell pastebin it's a new paste

		url = urllib2.urlopen(urllib2.Request(paste_url, urllib.urlencode(values))).read()
		self.pasteKey = url[len(url) - url[::-1].find('/'):]
		return

	def receive(self):
		if self.pasteKey == '':
			print('Requires a paste key from sent data')
			return
		data = []
		for line in urllib2.urlopen('http://pastebin.com/raw/' + self.pasteKey):
			data.append(line)
		return data

if __name__ == '__main__':
	x = Pastebin()
	x.send('this is a test')
	print(x.pasteKey)
	print(x.receive())