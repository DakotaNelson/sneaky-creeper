import scrypt

requiredParams = {
    'encode': {
        'key': 'string used as encryption key'
    },
    'decode': {
        'key': 'string used as decryption key'
    }
}


def encode(data, params):
    return scrypt.encrypt(data, params['key'].encode('ascii'), 0.1)


def decode(data, params):
    return scrypt.decrypt(data, params['key'].encode('ascii'))


