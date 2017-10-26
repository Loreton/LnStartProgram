#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.33.20
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    sys     import exit as sysExit
from    pathlib import Path, PurePath

from LnLib.Common.Exit          import Exit       as LnExit
from LnLib.Common.LnLogger      import SetLogger


def VerifyPath(path, exitOnError=True):
    logger = SetLogger(__package__)

    logger.info('verifying path: {}'.format(path))

    try:
        pathExists = Path(path).exists()

    except (Exception) as why:
        pathExists = False
        logger.error(str(why))


    if pathExists:
        retPath = PurePath(path)
        logger.info('it exists.')

    else:
        retPath = None
        logger.error("it doen't exists.")
        if exitOnError:
            LnExit(10, "{} doesn't exists".format(path))


    return retPath