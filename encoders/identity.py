'''
An encoder that does no encoding. Ironic, but also useful for testing channels.
Or not encoding/decoding.
'''

requiredParams = {
    'encode': {},
    'decode': {}
}

dependencies = []

def encode(data, params=None):
    return data


def decode(data, params=None):
    return data
