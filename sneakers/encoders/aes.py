from sneakers.modules import Encoder

import scrypt
import base64

# note that the class name *must* be title cased
class Aes(Encoder):
    requiredParams = {
        'encode': {
            'key': 'string used as encryption key'
        },
        'decode': {
            'key': 'string used as decryption key'
        }
    }

    description = """\
        Encrypts data using AES and the provided encryption key. The resulting bits are then base64 encoded to allow them to be represented as text.
    """

    def encode(self, data):
        params = self.params['encode']
        en = scrypt.encrypt(data, params['key'].encode('ascii'), 0.1)
        return base64.b64encode(en)

    def decode(self, data):
        params = self.params['decode']
        de = base64.b64decode(data)
        return scrypt.decrypt(de, params['key'].encode('ascii'))

