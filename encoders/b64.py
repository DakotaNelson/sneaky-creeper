import base64

def encode(data, params=None):
    return base64.b64encode(data)

def decode(data, params=None):
    return base64.b64decode(data)
