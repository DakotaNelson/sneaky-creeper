# Authors: Gabriel Butterick and Bonnie Ishiguro

import time
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from sneakers.modules import Channel, Parameter

class GoogleSpread(Channel):
    description = """\
        Posts data to Google Spreadsheets.
    """

    params = {
        'sending': [
            Parameter('client_email', True, 'The client_email value obtained from the Google Developers Console.'),
            Parameter('private_key', True, 'The private_key value obtained from the Google Developers Console.'),
            Parameter('google_sheet', True, 'The name (title) of the spreadsheet you wish to transfer data over.'),
            Parameter('column', False, 'The letter (capital A, B, C...) of the spreadsheet column you wish to write data into. This can be used to create multiple streams in the same spreadsheet.', 'A')
        ],
        'receiving': [
            Parameter('client_email', True, 'The client_email value obtained from the Google Developers Console.'),
            Parameter('private_key', True, 'The private_key value obtained from the Google Developers Console.'),
            Parameter('google_sheet', True, 'The name (title) of the spreadsheet you wish to transfer data over.'),
            Parameter('column', False, 'The letter (capital A, B, C...) of the spreadsheet column you wish to write data into. This can be used to create multiple streams in the same spreadsheet.', 'A')
        ]
    }

    # Courtesy Limit: 10,000,000 queries/day

    def send(self, data):
        CLIENT_EMAIL = self.param('sending', 'client_email')
        PRIVATE_KEY = self.param('sending', 'private_key')
        GOOGLE_SPREAD = self.param('sending', 'google_sheet')

        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open(GOOGLE_SPREAD).sheet1

        WRITE_COL = self.param('sending', 'column')
        row = 1
        while sheet.acell(WRITE_COL+str(row)).value:
            row += 1
        cell = WRITE_COL + str(row)

        sheet.update_acell(cell, data)
        return

    def receive(self):
        CLIENT_EMAIL = self.param('receiving', 'client_email')
        PRIVATE_KEY = self.param('receiving', 'private_key')
        GOOGLE_SPREAD = self.param('receiving', 'google_sheet')

        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open(GOOGLE_SPREAD).sheet1

        READ_COL = self.param('receiving', 'column')

        cells = []
        row = 1

        while sheet.acell(READ_COL+str(row)).value:
            cells.append(sheet.acell(READ_COL+str(row)).value)
            row += 1

        return cells
