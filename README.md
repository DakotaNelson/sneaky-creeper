# sneaky-creeper
Using social media as a tool for data exfiltration.

![diagram](diagram.png)

Usage
=====
See `screep`:
```python
  from sneakers import Exfil

  print(Exfil.list_channels())
  print(Exfil.list_encoders())

  channel = "file"
  encoders = ["b64"]

  dataz = "very secret and private message"

  # think of the exfil object like a tube
  # (or some kind of weird socket)
  t = Exfil(channel, encoders)

  t.set_channel_params({'sending': {'filename': 'test.txt'},
                        'receiving': {'filename': 'test.txt'}})

  t.set_encoder_params('b64', {})
  # this isn't actually necessary, just for demonstration

  print(t.channel_config())
  print(t.encoder_config('b64'))

  t.send(dataz)

  print(t.receive())
```

Setup
=====

#### Dependencies:

`virtuelenv venv && source venv/bin/activate && pip install -r requirements.txt`

There have been some odd issues with dependencies due to the way sneaky-creeper dynamically imports modules (the runtime imports tend to ignore virtualenvs). These have been solved in the past by installing modules globally using `pip install --user -r requirements.txt`, which is a pretty ugly hack. We're working on a better solution. Go ahead and try the above, and if it fails, open an issue so we can take a look.

#### API Keys:

##### Twitter:

Instructions are here: http://twython.readthedocs.org/en/latest/usage/starting_out.html

When the instructions are complete, go to the Twitter API page

Examine your access level for Consumer Key and Access Key and be sure they are set to read and write.

1. If not set to read and write, change the Consumer Key settings to be read and write
2. Revoke the Access Token
3. Wait five minutes
4. Generate a new access token

It should now mimic the access level of the Consumer Key

##### Tumblr:

Make a Tumblr account and [create an app](https://www.tumblr.com/oauth/apps). Then, visit the [API console](https://api.tumblr.com/console/calls/user/info) and note down the four strings there; these are your `key`, `secret`, `token`, and `token_secret`.

##### Soundcloud:

Make a Soundcloud account and [register an app](https://developers.soundcloud.com/docs/api/guide). Visit your [apps console](https://soundcloud.com/you/apps/) and note the strings for Client ID and for the Client Secret. These are for the `ID` and `secret`, while your username and password are for the `username` and `password`.

##### Salesforce:
First, set up a [Salesforce developer edition account](https://developer.salesforce.com/signup?d=70130000000td6N). [Define a connected app](https://help.salesforce.com/articleView?id=connected_app_create.htm&type=5).Make sure it has full permissions, and don't worry about the callback URL - it won't be used. Once you've successfully defined your app, note down the `client_id` and `client_secret` tokens. Lastly, [reset your security token](https://help.salesforce.com/apex/HTViewHelpDoc?id=user_security_token.htm&language=en) and note down its value.

##### Google Spreadsheets:
Follow the instructions found at http://gspread.readthedocs.io/en/latest/oauth2.html. You can stop noce you've noted down your `client_email` and `private_key`. You then need to create a Google Sheet (in the same account you just authorized!), and note down its title, then share it (using Google's share feature) with the email account you noted down as `client_email`.

Tests
=====

`source venv/bin/activate && nosetests` will run all the tests. Note that this will leave random junk on some of the channels you have set up - you've been warned! Credentials for these tests should go in `sneakers/config/` - there's another readme there to help you out.
