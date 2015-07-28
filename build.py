#!/usr/bin/python2

import os
import subprocess
import pip

import encoders
import channels

pip.main(['install', 'pyinstaller'])

# absolute path to this file
basedir = os.path.dirname(os.path.abspath(__file__))

# change to this file's directory
os.chdir(basedir)

subprocess.check_call(["pyinstaller","screep.spec"])
