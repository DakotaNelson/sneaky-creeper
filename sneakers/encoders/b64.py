from sneakers.modules import Encoder

import base64


class B64(Encoder):
    def encode(self, data):
        # we really don't need it
        params = self.reqParams['encode']
        return base64.b64encode(data)

    def decode(self, data):
        # we really don't need it
        params = self.reqParams['decode']
        return base64.urlsafe_b64decode(str(data))
