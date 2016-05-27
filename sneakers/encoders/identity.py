from sneakers.modules import Encoder

class Identity(Encoder):

    info = {
        "name": "Identity",
        "author": "davinerd",
        "description": "An encoder that does no encoding. Ironic, but also useful for testing channels. Or not encoding/decoding.",
        "comments": []
    }


    def encode(self, data):
        return data

    def decode(self, data):
        return data
