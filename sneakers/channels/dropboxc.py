from sneakers.modules import Channel
import dropbox
import os
import string
import random

class Dropboxc(Channel):
    info = {
        "name": "Dropbox",
        "author": "davinerd",
        "description": "Send and receive files through Dropbox",
        "comments": []
    }

    requiredParams = {
        'sending': {
            'token': 'Access token.',
            'rfile': 'Remote file location (overrides opsec_safe).'
        },
        'receiving': {
            'token': 'Access token.',
            'rfile': 'File to retrieve (absolute remote path).',
        }
    }

    opsec_safe = False

    def send(self, data):
        send_params = self.reqParams['sending']
        dbx = dropbox.Dropbox(send_params['token'])
        is_file = True
        buf = None

        try:
            with open(data, 'r') as f:
                buf = f.read()
        except Exception:
            is_file = False

        if 'rfile' in send_params:
            upload_filename = send_params['rfile']
            if is_file:
                data = buf
        else:
            chars = string.ascii_uppercase + string.ascii_lowercase
            upload_filename = ''.join(random.choice(chars) for _ in range(8))

            if is_file:
                data = buf
                if not self.opsec_safe:
                    upload_filename = os.path.basename(data)

        # ensure the path is remote absolute
        if not upload_filename.startswith("/"):
            upload_filename = "/"+upload_filename

        dbx.files_upload(data, upload_filename)

        return

    def receive(self):
        rec_params = self.reqParams['receiving']
        remote_file = rec_params['rfile']

        dbx = dropbox.Dropbox(rec_params['token'])
        # ensure the path is remote absolute
        if not remote_file.startswith("/"):
            remote_file = "/"+remote_file

        res = dbx.files_download(remote_file)
        return [res[1].content]