# To create a new encoder, create a new file named yourEncoderName.py that has the following functions:
import inspect

# TODO add optional params?
requiredParams = {
    'encode': {
        'foo':'A random variable defined here for example purposes.'
               },
    'decode': {
                 }
    }

def encode(data, params):
    print('Foo: ' + params['foo']) # test the 'foo' param defined below
    return "here's your encoded data back: {}".format(data)

def decode(data, params):
    return "this is decoded data, I guess"
