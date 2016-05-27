from sneakers.modules import Encoder

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as cryptoRSA

class Rsa(Encoder):
    description = """\
        Encrypts data using RSA.
    """

    requiredParams = {
        'encode': {
            'publicKey': 'The filename of the public key, ' +
                         'matched to the private key used for decryption.'
        },
        'decode': {
            'privateKey': 'The filename of the private key, ' +
                          'matched to the public key used for decryption.'
        }
    }

    def encode(self, data):
        encode_params = self.reqParams['encode']
        keystring = open(encode_params['publicKey']).read()
        key = cryptoRSA.importKey(keystring)
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def decode(self, data):
        decode_params = self.reqParams['decode']
        keystring = open(decode_params['privateKey']).read()
        key = cryptoRSA.importKey(keystring)
        cipher = PKCS1_OAEP.new(key)
        message = cipher.decrypt(data)
        return message
