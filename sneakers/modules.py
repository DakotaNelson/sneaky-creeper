"""
Contains classes for channels and encoders to inherit from.
"""
from sneakers.errors import ExfilChannel, ExfilEncoder

"""
Parameter Class

Handles the possible parameters that can be passed to each channel.
"""

class Parameter(object):
    def __init__(self, name, required, description, default = None):
        self.name = name
        self.required = required
        self.description = description
        self.default = default
        self.value = None

    def __str__(self):
        return '<Parameter {} value={}, required={}>'.format(self.name, self.value, self.required)

"""
Module Class

Used as the base for both Channel and Encoder classes
"""


class Module(object):
    # Param objects go here
    params = {
        'sending': [
        ],
        'receiving': [
        ]
    }

    def __init__(self):
        pass

    def param(self, paramType, name):
        # Get a parameter
        for p in self.params[paramType]:
            if p.name == name:
                if p.value:
                    return p.value
                else:
                    return p.default

    def set_params(self, params):
        if not isinstance(params, dict):
            raise TypeError("Module parameters must be specified as a dictionary.")

        for paramType in ['sending', 'receiving']:
            if paramType not in params:
                # the params passed don't have 'sending' or 'receiving' block
                continue
            for param in self.params[paramType]:
                # each param attempts to fetch its value from values passed in
                try:
                    param.value = params[paramType][param.name]
                except:
                    pass

        for paramType in ['sending', 'receiving']:
            # now check to make sure all the required params are set
            # (in a diffent for block because of the if/continue above)
            missing = []
            for param in self.params[paramType]:
                if param.required and param.value is None:
                    missing.append(param.name)
            if len(missing) > 0:
                raise ValueError("Required parameter(s) '{}' not set for {}.".format(', '.join(missing), paramType))

"""
Channel Class

To create a new channel, create a new file named yourChannelName.py
with a class YourChannelName that inherits from this base class.
"""


class Channel(Module):
    description = """\
        A description of the channel goes here.
    """

    # maximum length of characters of each transmission
    # useful in case of media limitations (i.e. Twitter)
    maxLength = 140

    # maximum number of posts per hour
    maxHourly = 100

    opsecSafe = False

    def __init__(self):
        Module.__init__(self)

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

    def __init__(self):
        Module.__init__(self)

    # TODO set up params such that each function
    # only has access to encode/decode params
    def encode(self, data):
        pass

    def decode(self, data):
        pass
