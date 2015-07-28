#!/usr/bin/python2

import os
import subprocess

# absolute path to this file
basedir = os.path.dirname(os.path.abspath(__file__))

# change to this file's directory
os.chdir(basedir)

print(os.getcwd())
subprocess.check_call(["pyinstaller","./screep.spec"])
