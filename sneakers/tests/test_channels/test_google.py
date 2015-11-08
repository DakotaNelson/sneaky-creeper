import unittest
import json
import random
import string
import os
from oauth2client.client import SignedJwtAssertionCredentials
import gspread

from unittest.case import SkipTest

from sneakers.channels import googleSpread
import sneakers
basePath = os.path.dirname(os.path.abspath(sneakers.__file__))

class GoogleTest(unittest.TestCase):

    def setUp(self):

        configPath = os.path.join(basePath, 'config', 'google-config.json')
        try:
            with open(configPath, 'rb') as f:
                s = json.loads(f.read())
        except:
            raise SkipTest("Could not access Google configuration file.")

        self.params = s['google']

        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(self.params['client_email'], self.params['private_key'], scope)       
        gc = gspread.authorize(credentials)
        
        self.client = gc.open(self.params['google_sheet']).sheet1
        self.randText = ''.join([random.choice(string.letters) for i in range(10)])

        self.channel = googleSpread.GoogleSpread()
        self.channel.params['sending'] = self.params
        self.channel.params['receiving'] = self.params

    def test_send(self):
        self.channel.send(self.randText)

        READ_COL = 'A'
        cell = ''
        row = 1

        while self.client.acell(READ_COL+str(row)).value:
            cell = self.client.acell(READ_COL+str(row)).value
            row += 1

        resp = cell
        self.assertEqual(cell, self.randText)

    def test_receive(self):

        WRITE_COL = 'A'
        row = 1
        if not self.client.acell(WRITE_COL+str(row)).value:
            row += 1
        cell = WRITE_COL + str(row)

        self.client.update_acell(cell, self.randText)
        


        cells = self.channel.receive()

        while self.client.acell(WRITE_COL+str(row)).value:
            cell = self.client.acell(WRITE_COL+str(row)).value
            row += 1

        resp = cell
        self.assertEqual(cell, self.randText)