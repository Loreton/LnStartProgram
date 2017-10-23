#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 07.57.10
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    sys     import exit as sysExit
from    pathlib import Path, PurePath

def VerifyPath(gv, path, exitOnError=True):
    logger = gv.Prj.SetLogger(__name__)
    logger.info('path: {} - {}'.format(path, type(path)))



    try:
        pathExists = Path(path).exists()

    except (Exception) as why:
        pathExists = False
        logger.error(str(why))


    if pathExists:
        retPath = PurePath(path)
        logger.info('exists.')

    else:
        retPath = None
        logger.error('not exists.')
        if exitOnError:
            gv.Ln.Exit(10, "{} doesn't exists".format(path))


    return retPath