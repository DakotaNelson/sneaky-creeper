from twython import Twython

def main():
	APP_KEY = 'juU7NF2jDmuzSPG4MTwm6M3Ry'
	APP_SECRET = 'dr6MsyrHx0bGWvTYBgsYVuTuFwSQjRIgdocjq6TdtY9qxzNhos'


	twitter = Twython(APP_KEY, APP_SECRET)

	#twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
	#ACCESS_TOKEN = twitter.obtain_access_token()

	#twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

	auth = twitter.get_authentication_tokens()
	
	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
	auth['auth_url']
	print OAUTH_TOKEN
	print OAUTH_TOKEN_SECRET

if __name__ == "__main__":
	main()