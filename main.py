# This file will pull everything together:
# Take and process command line args -> read in data -> encode data (potentially multiple times) -> transmit data
# OR  Take and process command line args -> use transmit module's retrieve method to grab data -> write out data


# to use an encoder:
import importlib
encoderName = 'exampleEncoder'
moduleName = '.'.join(['encoders', encoderName])
enc = importlib.import_module(moduleName)
# This is a programmatic equivalent of:
# from encoding import exampleEncoder as enc

enc.send("some data")

ret = enc.receive()
print(ret)
