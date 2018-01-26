from sneakers.modules import Encoder, Parameter

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as cryptoRSA

class Rsa(Encoder):
    description = """\
        Encrypts data using RSA.
    """

    params = {
        'sending': [
            Parameter('publicKey', True, 'The filename of the public key, matched to the private key used for decryption.')
        ],
        'receiving': [
            Parameter('privateKey', True, 'The filename of the private key, matched to the public key used for decryption.')
        ]
    }

    def encode(self, data):
        publicKeyFile = self.param('sending', 'publicKey')
        keystring = open(publicKeyFile).read()
        key = cryptoRSA.importKey(keystring)
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def decode(self, data):
        privateKeyFile = self.param('receiving', 'privateKey')
        keystring = open(privateKeyFile).read()
        key = cryptoRSA.importKey(keystring)
        cipher = PKCS1_OAEP.new(key)
        message = cipher.decrypt(data)
        return message
