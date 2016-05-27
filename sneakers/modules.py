"""
Contains classes for channels and encoders to inherit from.
"""
from sneakers.errors import ExfilChannel, ExfilEncoder

"""
Module Class

Used as the base for both Channel and Encoder classes
"""


class Module(object):

    optionalParams = {}

    def __init__(self):
        self.reqParams = {}
        self.optParams = {}

    def set_opt_params(self, params):
        for k in params.keys():
            if k not in self.optionalParams.keys():
                raise ExfilChannel('Unrecognized optional parameter \'{}\''.format(k))
            self.optParams[k] = params[k]

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

    # same format as requiredParams but free
    optionalParams = {}

    # maximum length of characters of each transmission
    # useful in case of media limitations (i.e. Twitter)
    maxLength = 140

    # maximum number of posts per hour
    maxHourly = 100

    opsecSafe = False

    def __init__(self):
        Module.__init__(self)
        self.reqParams = {'sending': {},
                          'receiving': {}
                          }

    # TODO
    # set up a way to pass just sending
    # or just receiving params to these functions
    # (instead of accessing all params)
    def send(self, data):
        pass

    def receive(self):
        pass

    def set_params(self, params):
        for k in params.keys():
            if 'sending' not in k and 'receiving' not in k:
                raise ExfilChannel('Missing sending and/or receiving for channel {}'.format(self.__class__.__name__))
            for param in self.requiredParams[k]:
                if param not in params[k]:
                    raise ExfilChannel(
                        'Missing required parameter \'{}\' for channel \'{}\' ({}).'.format(param,
                                                                                            self.__class__.__name__, k))
                self.reqParams[k] = params[k]


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
        self.reqParams = {'encode': {},
                          'decode': {}
                          }

    # TODO
    # set up params such that each function
    # only has access to encode/decode params
    def encode(self, data):
        pass

    def decode(self, data):
        pass

    def set_params(self, params):
        for k in params.keys():
            if 'encode' not in k and 'decode' not in k:
                raise ExfilEncoder('Missing encode and/or decode for decoder {}'.format(self.__class__.__name__))
            for param in self.requiredParams[k]:
                if param not in params[k]:
                    raise ExfilEncoder(
                        'Missing required parameter \'{}\' for encoder \'{}\' ({}).'.format(param,
                                                                                            self.__class__.__name__, k))
                self.reqParams[k] = params[k]
