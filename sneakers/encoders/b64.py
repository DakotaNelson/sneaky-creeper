from sneakers.modules import Encoder

import base64

class B64(Encoder):
    description = """\
        Encodes data using base64.
    """

    def encode(self, data):
        params = self.params['encode']
        return base64.b64encode(data)

    def decode(self, data):
        params = self.params['decode']
        return base64.urlsafe_b64decode(str(data))
