from sneakers.modules import Encoder, Parameter

import scrypt
import base64

# note that the class name *must* be title cased
class Aes(Encoder):
    description = """\
        Encrypts data using AES and the provided encryption key. The resulting bits are then base64 encoded to allow them to be represented as text.
    """

    params = {
        'sending': [
            Parameter('key', True, 'String used as encryption key.')
        ],
        'receiving': [
            Parameter('key', True, 'String used as encryption key.')
        ]
    }

    def encode(self, data):
        key = self.param('sending', 'key')
        en = scrypt.encrypt(data, key.encode('ascii'), 0.1)
        return base64.b64encode(en)

    def decode(self, data):
        key = self.param('sending', 'key')
        de = base64.b64decode(data)
        return scrypt.decrypt(de, key.encode('ascii'))

