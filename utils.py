'''
Holds utility functions for sneaky-creeper.
'''

import importlib
import os
import subprocess
import sys

def importModule(moduleName, quiet=True):
    # helper function to import a module, check
    # its dependencies, install if required, then
    # return the module
    #if getattr(sys, 'frozen', False):
    mod = importlib.import_module(moduleName)

    if hasattr(sys, "_MEIPASS"):
        # we are running in a |PyInstaller| bundle
        # abort!
        return mod
    # install dependencies
    import pip
    try:
        for dep in mod.dependencies:
            if quiet:
                pip.main(['install', dep, '-q'])
            else:
                pip.main(['install', dep])
    except AttributeError:
        print("ERROR: module '{}' has no dependencies array.".format(mod.__file__))
        return False
    return mod

def venvMe(venvName):
    if getattr(sys, 'frozen', False):
        # we are running in a |PyInstaller| bundle
        # abort!
        return True
        #filepath = sys._MEIPASS
    else:
        filepath = os.path.abspath(__file__)
    basedir = os.path.dirname(filepath)
    # if there's a virtualenv, activate it
    activate_this = os.path.join(basedir, venvName, 'bin', 'activate_this.py')
    if not os.path.exists(activate_this):
        # if there isn't, create one
        try:
            subprocess.check_call(['virtualenv',venvName])
        except subprocess.CalledProcessError as e:
            # or at least try. Change back to old dir
            os.chdir(origdir)
            return False

    execfile(activate_this, dict(__file__=activate_this))
    # change back to old dir
    #os.chdir(origdir)
    return True

def wrapPath(relative):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
