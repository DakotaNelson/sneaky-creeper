# see: https://github.com/burnash/gspread

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


requiredParams = {
    'sending': {
        'json': 'The json file containing the client email and private key.',
        'google_sheet': 'The file on google drive the data should be written to.'
    },
    'receiving': {
        'json': 'The json file containing the client email and private key.',
        'google_sheet': 'The file on google drive the data should be written to.',
        'cell': 'The cell on the spreadsheet to bring data from'
    }
}
def send(data, params):
    #Uses the personalized json file located in the same place as the main file to gather required credentials
    json_key = json.load(open(params['json']))
    GOOGLE_SPREAD = unicode(params['google_sheet'])
    scope = ['https://spreadsheets.google.com/feeds']
    
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

    gc = gspread.authorize(credentials)
    sheet = gc.open(GOOGLE_SPREAD).sheet1
    #adds new information to empty rows instead of overwriting existing ones
    col = 'A'
    row = 1
    while sheet.acell(col+str(row)).value:
        row += 1
    cell = col + str(row)

    sheet.update_acell(cell, data)
    print "Sending Complete"
    print col + str(row)
    return

def receive(params):
    
    json_key = json.load(open(params['json']))
    GOOGLE_SPREAD = unicode(params['google_sheet'])
    scope = ['https://spreadsheets.google.com/feeds']
    
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    
    gc = gspread.authorize(credentials)
    sheet = gc.open(GOOGLE_SPREAD).sheet1

    cell = params['cell'] 
    info = []
    #todo: set this up so that if the user puts in 'all' as the cell, returns all info on sheet.
    info.append(sheet.acell(cell).value)
    return info