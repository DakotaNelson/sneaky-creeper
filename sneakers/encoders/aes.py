import scrypt
import base64

requiredParams = {
    'encode': {
        'key': 'string used as encryption key'
    },
    'decode': {
        'key': 'string used as decryption key'
    }
}


def encode(data, params):
    en = scrypt.encrypt(data, params['key'].encode('ascii'), 0.1)
    return base64.b64encode(en)

def decode(data, params):
    de = base64.b64decode(data)
    return scrypt.decrypt(de, params['key'].encode('ascii'))

