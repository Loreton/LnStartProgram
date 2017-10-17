#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 17-10-2017 09.25.59
# -----------------------------------------------
import sys, os
import pathlib


def VerifyPath(gv, path):
    gv.logger.info('verifying path: {}'.format(path))

    if isinstance(path, pathlib.WindowsPath):
        if  path.exists():
            return path

    elif  os.path.isfile(path) or os.path.isdir(path):
        return path

    else:
        print("ERROR: path: {} doesn't exists".format(path))
        sys.exit()


