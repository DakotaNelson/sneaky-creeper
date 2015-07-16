# sneaky-creeper
Using social media as a tool for data exfiltration.

![diagram](sneaky_creeper_diagram.png)


Dependencies:

`sudo pip install pycrypto`

How to get API keys:

Twitter:
Go here: http://twython.readthedocs.org/en/latest/usage/starting_out.html 
When the instructions are complete, go to the Twitter API page
Examine your access level for Consumer Key and Access Key
Be sure they are set to read and write
If not set to read and write, change the Consumer Key settings to be read and write
Revoke the Access Token
Wait five minutes
Generate a new access token
It should now mimic the access level of the Consumer Key
