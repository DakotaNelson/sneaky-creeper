# see: https://github.com/themson/MurDocK/blob/master/docBuffer.py

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def send(data, params):
    CLIENT_EMAIL = unicode(params['client_email'])
    PRIVATE_KEY = unicode(params['private_key'])
    GOOGLE_SPREAD = unicode(params['sheet'])

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, scope)
	gc = gspread.authorize(credentials)
	sheet = gc.open(GOOGLE_SPREAD).sheet1

	col = 'A'
	row = 1
	if sheet.acell(col+str(row)).value = "":
		row += 1
	cell = col + str(row)

	sheet.update_acell(cell, data)
	print "Sending Complete"
	return

def receive(params):
    CLIENT_EMAIL = unicode(params['client_email'])
    PRIVATE_KEY = unicode(params['private_key'])
    GOOGLE_SPREAD = unicode(params['sheet'])

    credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, scope)
	gc = gspread.authorize(credentials)
	sheet = gc.open(GOOGLE_SPREAD).sheet1

    cell = 
    return sheet.acell(cell).value