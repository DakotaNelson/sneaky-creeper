"""
Contains classes for channels and encoders to inherit from.
"""

"""
Module Class

Used as the base for both Channel and Encoder classes
"""

class Module(object):
    def __init__(self):
        self.params = {}

    def set_params(self, params):
        for k in params.keys():
            self.params[k] = params[k]
        self.check_params()

    def check_params(self):
        """
            Makes sure the current parameters are valid.
            More complex modules can override this to allow for custom
            parameter validation.

            Returns true if parameters are valid, else false.
        """
        for p in self.requiredParams.keys():
            if not p in self.params:
                return False
        return True

"""
Channel Class

To create a new channel, create a new file named yourChannelName.py
with a class YourChannelName that inherits from this base class.
"""

class Channel(Module):
    description = """\
        A description of the channel goes here.
    """

    requiredParams = {
        'sending': {
            # 'param_name': 'Brief description of the parameter.'
        },
        'receiving': {
            # 'param_name': 'Brief description of the parameter.'
        }
    }

    maxLength = 140
    # maximum length of one post (characters)

    maxHourly = 100
    # maximum number of posts per hour

    def __init__(self):
        Module.__init__(self)
        self.params = {'sending':{},
                       'receiving':{}}

    # TODO set up a way to pass just sending
    # or just recieving params to these functions
    # (instead of accessing all params)
    def send(self, data):
        pass

    def receive(self):
        pass

"""
Encoder Class

To create a new encoder, create a new file named yourEncoderName.py
with a class YourEncoderName that inherits from this base class.
"""

class Encoder(Module):
    description = """\
        A description of the encoder goes here.
    """

    requiredParams = {
        'encode': {
            # 'param_name': 'Brief description of the parameter.'
        },
        'decode': {
            # 'param_name': 'Brief description of the parameter.'
        }
    }

    def __init__(self):
        Module.__init__(self)
        self.params = {'encode':{},
                       'decode':{}}

    # TODO set up params such that each function
    # only has access to encode/decode params
    def encode(self, data):
        pass

    def decode(self, data):
        pass
