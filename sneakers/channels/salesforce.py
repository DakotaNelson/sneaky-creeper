# Written by Dakota Nelson (@jerkota)

from sneakers.modules import Channel

import random
import string
import requests
import json

class Salesforce(Channel):
    description = """\
        Posts data to Salesforce as a "Document" upload.
        See https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_sobject_insert_update_blob.htm
    """

    requiredParams = {
        'sending': {
            'username': 'Your Salesforce username (in the form of an email).',
            'password': 'Your Salesforce password.',
            'client_id': 'The "Consumer Key" from the connected app definition.',
            'client_secret': 'The "Consumer Secret" from the connected app definition.',
            'security_token': 'Your account\'s security token. For more detail see https://help.salesforce.com/apex/HTViewHelpDoc?id=user_security_token.htm&language=en'
                   },
        'receiving': {
            'username': 'Your Salesforce username (in the form of an email).',
            'password': 'Your Salesforce password.',
            'client_id': 'The "Consumer Key" from the connected app definition.',
            'client_secret': 'The "Consumer Secret" from the connected app definition.',
            'security_token': 'Your account\'s security token. For more detail see https://help.salesforce.com/apex/HTViewHelpDoc?id=user_security_token.htm&language=en'
                     }
        }

    maxLength = 3.75e+7 / 2
    # yay for large Salesforce documents!
    # this is 37.5 MB / 2 bytes per character just in case

    maxHourly = 100
    # Can only post 100 times per hour
    # not sure if there's an actual limit, but this is it for now

    def send(self, data):
        params = self.params['sending']

        # first, authenticate
        # see: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_understanding_username_password_oauth_flow.htm
        self.authenticate()

        # second, get the ID of the folder to put the file in
        folderId = self.getFolderId()

        # third, upload the file
        # see https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_sobject_insert_update_blob.htm
        # and http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

        filename = ''.join(random.choice(string.lowercase) for i in range(20))

        # some metadata Salesforce needs
        filedata = {
                    'Name': filename,
                    'FolderId': folderId
                   }

        # upload a two-part file; the first part is metadata from above,
        # JSON encoded, the second part is the actual file
        files = [
                  ('entity_document',
                    ('',
                     json.dumps(filedata),
                     'application/json',
                     {'Type': 'application/json'}
                    )
                  ),
                  ('Body',
                    (filename,
                     data,
                     'application/pdf')
                  )
                ]

        url = '{}/services/data/v23.0/sobjects/Document/'.format(
                                                     self.auth['instance_url'])

        resp = requests.post(url,
                 headers = {'Authorization':
                              'Bearer {}'.format(self.auth['access_token'])
                           },
                 files = files)

        if not resp.json()['success'] == True:
            raise ValueError('Salesforce file upload error occurred')

        return

    def receive(self):
        params = self.params['receiving']
        self.authenticate()

        query = 'SELECT body FROM Document'
        url = '{}/services/data/v20.0/query/?q={}'.format(self.auth['instance_url'], query)

        r = requests.get(url, headers={"Authorization": "Bearer {}".format(self.auth['access_token'])})

        respJson = r.json()

        posts = []
        # now loop through each of the document body records returned
        for record in respJson['records']:
            url = '{}{}'.format(self.auth['instance_url'], record['Body'])
            r = requests.get(url, headers={"Authorization": "Bearer {}".format(self.auth['access_token'])})
            posts.append(r.text)

        return posts

    ###################################
    ###### Convenience Functions ######
    ###################################

    def authenticate(self):
        ''' Authenticates to Salesforce, puts the result in self.auth if
            successful, otherwise throws a ValueError '''

        params = self.params['sending']

        # see: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_understanding_username_password_oauth_flow.htm
        params = {'grant_type':'password',
                  'client_id': params['client_id'],
                  'client_secret': params['client_secret'],
                  'username': params['username'],
                  'password': params['password'] + params['security_token']}

        r = requests.post('https://login.salesforce.com/services/oauth2/token',
                          data=params)

        js = r.json()

        if u'error' in js.keys():
            raise ValueError('Salesforce authentication unsuccessful')

        # should return:
        # [u'access_token', u'token_type', u'signature', u'issued_at',
        #  u'instance_url', u'id']
        self.auth = js

    def getFolderId(self):
        ''' Returns the ID of a folder, and creates one if there are none. '''

        query = 'SELECT Id FROM Folder'

        url = '{}/services/data/v20.0/query/?q={}'.format(self.auth['instance_url'], query)

        r = requests.get(url, headers={"Authorization": "Bearer {}".format(self.auth['access_token'])})

        respJson = r.json()

        # if there are no folders, make one
        if respJson['totalSize'] < 1:
            return self.createFolder()
        else:
            return respJson['records'][0]['Id']

    def createFolder(self):
        ''' Creates a folder and returns its ID. '''

        url = '{}/services/data/v20.0/sobjects/Folder/'.format(self.auth['instance_url'])

        folder = {
                  "Name": "screep_folder",
                  "DeveloperName" : "screep",
                  "AccessType" : "Public",
                  "Type" : "Document"
                 }

        r = requests.post(url, headers={"Authorization": "Bearer {}".format(self.auth['access_token']), "Content-Type": "application/json"}, json=folder)

        return r.json()['id']
