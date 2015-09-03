from sneakers.modules import Encoder

class Identity(Encoder):
    description = """\
        An encoder that does no encoding. Ironic, but also useful for testing channels.
        Or not encoding/decoding.
    """

    def encode(self, data):
        return data

    def decode(self, data):
        return data
