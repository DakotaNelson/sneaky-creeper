# To create a new encoder, create a new file named yourEncoderName.py that has the following functions:
import inspect

def encode(data, params):
    print('Foo: ' + params['foo']) # test the 'foo' param defined below
    return "here's your encoded data back: {}".format(data)

def decode(data, params):
    return "this is decoded data, I guess"

def args():
    # list of required arguments for this module
    args = {
            "foo": "this can be anything, it's not actually used"
           }
    # when an arg is defined here, it can be accesed in the functions above
    # as 'params[arg]'

    # sort of hacky way to make this class-like
    return args
