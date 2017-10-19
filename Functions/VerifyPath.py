#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 19-10-2017 11.50.48
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    sys     import exit as sysExit
from    pathlib import Path, PurePath

def VerifyPath(gv, path, exitOnError=True):
    logger = gv.Ln.SetLogger(__name__)
    logger.info('path: {} - {}'.format(path, type(path)))


    if  Path(path).exists():
        retPath = PurePath(path)
        logger.info('    .... exists - {}'.format(type(retPath)))
    else:
        retPath = None
        logger.info('    .... not exists')
        if exitOnError:
            print("*********** ERROR **************")
            print("* ", path, "doesn't exists.")
            print("*********** ERROR **************")
            sysExit()


    return retPath