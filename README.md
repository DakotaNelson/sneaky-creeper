# sneaky-creeper
Using social media as a tool for data exfiltration.

![diagram](sneaky_creeper_diagram.png)

Usage
=====

**NOTE:** take a look at the setup section before you get started.

sneaky-creeper has two base elements: **encoders** (the left column in the diagram above, they encode/decode data) and **channels** (the part that actually does Internet things, in the dotted rectangle in the diagram above). You can chain encoders to, say, base64 encode your data, then encrypt it with RSA, but there can only be one channel in each command. `-e` specifies encoders (specify as many as you want), and `-c` specifies channels.

To see what channels are available:

`./screep channels`

To see what encoders are available:

`./screep encoders`

To write some data to a file in plaintext:

`echo "some data" | ./screep send -e identity -c file -p '{"file": {"filename", "test.txt"}}'`

See how useful that is?

To read the file back in:

`./screep receive -e identity -c file -p '{"file": {"filename", "test.txt"}}'`

To do the same, but encrypt the file's contents with RSA:

`echo "some data" | ./screep send -e rsa -c file -p '{"file": {"filename", "test.txt"}, "rsa": {"publicKey": "rsakey.pem.pub"}}'  `  
`./screep receive -e rsa -c file -p '{"file": {"filename", "test.txt"}, "rsa": {"privateKey": "rsakey.pem"}}' privateKey`

To just test out the base64 encoder:

`echo "some data" | ./screep echo -e b64`

If you specify multiple encoders, the order is automatically reversed on decode so that you can specify them in the same order on both sides of the transmission and everything will work.


Setup
=====

#### Dependencies:

sneaky-creeper will install dependencies for you. It even automagically creates a virtualenv to put everything in.

#### Compiling:

First, you're probably going to want to set up a virtualenv so you don't have to install global packages (which usually requires sudo):

`pip install virtualenv` (if required)
`virtualenv venv`
`source venv/bin/activate`

Note that this is done automatically when `screep` is run, but for some reason it has to be done manually when running `build.py`.

Running `python build.py` will build a self-contained binary. If you build on Windows, it'll work on Windows (probably). If you build on OS X, it'll work on OS X (probably). You get the idea. We're working on cross-platform builds using Wine - coming soon!

**Note that this feature is not yet fully tested and might be pretty shaky. Let us know how it works!**

#### API Keys:

#####Twitter:

Instructions are here: http://twython.readthedocs.org/en/latest/usage/starting_out.html

When the instructions are complete, go to the Twitter API page. Examine your access level for consumer key and access key and be sure they are set to read and write.

1. If not set to read and write, change the consumer key settings to be read and write
2. Revoke the access token
3. Wait five minutes
4. Generate a new access token

The access token should now mimic the access level of the consumer key. You're ready to go!

#####Tumblr:

Make a Tumblr account and [create an app](https://www.tumblr.com/oauth/apps). Then, visit the [API console](https://api.tumblr.com/console/calls/user/info) and note down the four strings there; these are your `key`, `secret`, `token`, and `token_secret`.
