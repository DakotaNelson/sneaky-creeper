#!/usr/bin/python2

import os
import subprocess
import pip

import encoders
import channels

# if there's a virtualenv, activate it
activate_this = 'venv/bin/activate_this.py'
if not os.path.exists(activate_this):
    # if there isn't, create one
    try:
        subprocess.check_call(['virtualenv','venv'])
    except subprocess.CalledProcessError as e:
        # or at least try
        print("Unable to create virtualenv. Please manually create a virtualenv named 'venv' and retry.")
        sys.exit()

execfile(activate_this, dict(__file__=activate_this))

# get pyinstaller installed and ready
pip.main(['install', 'pyinstaller'])

# absolute path to this file
basedir = os.path.dirname(os.path.abspath(__file__))

# change to this file's directory
os.chdir(basedir)

# do the magic
subprocess.check_call(["pyinstaller","screep.spec"])
