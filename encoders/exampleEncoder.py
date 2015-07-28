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

dependencies = []
# specify any external dependencies here as pip package name strings
# for example:
# dependencies = ['somePyPIPackage']
# if you have to pip install it, it needs to go here

def encode(data, params):
    print('Foo: ' + params['foo']) # test the 'foo' param defined below
    return "here's your encoded data back: {}".format(data)

def decode(data, params):
    return "this is decoded data, I guess"
