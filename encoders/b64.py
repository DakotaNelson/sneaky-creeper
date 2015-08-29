import base64


class B64():
    requiredParams = {
        'encode': {},
        'decode': {}
    }

    params = dict()

    def __init__(self):
        pass

    def set_params(self, params):
        self.params = params

    def encode(self, data, params={}):
        return base64.b64encode(data)

    def decode(self, data, params={}):
        return base64.urlsafe_b64decode(str(data))