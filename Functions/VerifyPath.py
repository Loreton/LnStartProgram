#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 17-10-2017 17.07.21
# -----------------------------------------------
import sys, os
from pathlib import *
# import pathlib as p


def VerifyPath(path, logger=None):
    print ('\n.........', type(path), path)
    if logger: logger.info('verifying path: {}'.format(path))

    retPath = None

    if isinstance(path, WindowsPath):
        if  path.exists():
            retPath = path

    elif isinstance(path, PureWindowsPath):
        if  Path(path).exists():
            retPath = path

    elif  os.path.isfile(path) or os.path.isdir(path):
        retPath = path

    else:
        if  Path(path).exists():
            retPath = path
        # print("ERROR: path: {} doesn't exists".format(path))
        # sys.exit()

    retPath = PurePath(retPath)
    print ('.....', type(retPath),retPath)
    print ()

    return retPath