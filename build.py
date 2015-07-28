#!/usr/bin/python2

import os
import subprocess
import pip
import pkgutil
import sys

import encoders
import channels

from utils import venvMe, importModule

'''if not venvMe('venv'):
    print("Unable to create virtualenv. Please manually create a virtualenv named 'venv' and retry.")
    sys.exit()'''

# get pyinstaller installed and ready
pip.main(['install', 'pyinstaller'])

# install all dependencies for encoders and channels
# importModule automatically handles this for us
for importer, modname, ispkg in pkgutil.iter_modules(encoders.__path__):
    if not importModule("encoders." + modname, False):
        print("Unable to import module '{}'".format(modname))
        sys.exit()

for importer, modname, ispkg in pkgutil.iter_modules(channels.__path__):
    if not importModule("channels." + modname, False):
        print("Unable to import module '{}'".format(modname))
        sys.exit()

# absolute path to this file
basedir = os.path.dirname(os.path.abspath(__file__))

# change to this file's directory
os.chdir(basedir)

# do the magic
subprocess.check_call(["pyinstaller","screep.spec"])
