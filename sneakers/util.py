import json
import pkgutil
import os


def jsonParse(strArg):
    """
    A utility to handle a string argument by either parsing it
    directly as JSON or, if that fails, loading a JSON file at that
    filepath.

    :param strArg: Either a JSON string or filepath to a JSON file
    :type strArg: str
    :returns: The parsed JSON object
    :rtype: dict
    :raises: ValueError
    """

    # Try to parse strArg as a JSON string
    try:
        return json.loads(strArg)
    except:
        pass

    # Try to use strArg as a filename and load the file
    try:
        with open(strArg) as configFile:
            return json.load(configFile)
    except:
        pass

    # Otherwise, raise an exception
    exceptionMessage = ("""
        Parameter argument was neither a valid JSON string,
        nor a filepath to a valid JSON file.
    """)
    raise ValueError(exceptionMessage)

def import_module(where, what):
    path = '.'.join([where, what])
    class_name = what.title()
    mod = __import__(path, fromlist=[class_name])
    mod_class = getattr(mod, class_name)
    return mod_class

def list_encoders(verbose=False):
    # find the path to the encoders folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    encoders = os.path.join(current_dir, 'encoders')
    # then find all the modules
    encoders = pkgutil.iter_modules(path=[encoders])
    # and list them out
    encoding_options = [modName for _, modName, _ in encoders]

    if verbose:
        verbose_encoding_opt = list()
        for encoder in encoding_options:
            encoder_class = import_module('sneakers.encoders', encoder.lower())
            verbose_encoding_opt.append({'encoder': encoder, 'info': encoder_class().info})

        return verbose_encoding_opt

    return encoding_options


def list_channels(verbose=False):
    # find the path to the channels folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    channels = os.path.join(current_dir, 'channels')
    # then find all the modules
    channels = pkgutil.iter_modules(path=[channels])
    # and list them out
    channel_options = [modName for _, modName, _ in channels]

    if verbose:
        verbose_channel_opt = list()
        for channel in channel_options:
            channel_class = import_module('sneakers.channels', channel)
            verbose_channel_opt.append({'channel': channel, 'info': channel_class().info})

        return verbose_channel_opt

    return channel_options
