# Authors: Gabriel Butterick and Bonnie Ishiguro

import time
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

from sneakers.modules import Channel

class GoogleDocs(Channel):
    description = """\
        Posts data to Google Spreadsheets.
    """

    requiredParams = {
        'sending': {
            'client_email': '',
            'private_key': '',
            'google_sheet': ''
        },
        'receiving': {
            'client_email': '',
            'private_key': '',
            'google_sheet': ''
        }
    }

    # Courtesy Limit: 10,000,000 queries/day

    def send(self, data):

        send_params = self.params['sending']

        CLIENT_EMAIL = send_params['client_email']
        PRIVATE_KEY = send_params['private_key']
        GOOGLE_SPREAD = send_params['google_sheet']

        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open(GOOGLE_SPREAD).sheet1

        WRITE_COL = 'A'
        row = 1
        if not sheet.acell(WRITE_COL+str(row)).value:
            row += 1
        cell = col + str(row)

        sheet.update_acell(cell, data)
        return

    def receive(self):

        rec_params = self.params['receiving']

        CLIENT_EMAIL = rec_params['client_email']
        PRIVATE_KEY = rec_params['private_key']
        GOOGLE_SPREAD = rec_params['google_sheet']

        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open(GOOGLE_SPREAD).sheet1

        READ_COL = 'A'
        
        cells = []
        row = 1

        while sheet.acell(READ_COL+str(row)).value:
            cells.append(sheet.acell(READ_COL+str(row)).value)
            row += 1

        return cells