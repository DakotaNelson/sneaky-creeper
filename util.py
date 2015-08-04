"""
Utility functions for screep.

"""

import json


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
