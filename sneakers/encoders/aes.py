import scrypt
import base64

class AES():
    requiredParams = {
        'encode': {
            'key': 'string used as encryption key'
        },
        'decode': {
            'key': 'string used as decryption key'
        }
    }

    def __init__(self):
        pass

    def set_params(self, params):
        self.params = params

    def encode(self, data, params={}):
        en = scrypt.encrypt(data, params['key'].encode('ascii'), 0.1)
        return base64.b64encode(en)

    def decode(self, data, params={}):
        de = base64.b64decode(data)
        return scrypt.decrypt(de, params['key'].encode('ascii'))

