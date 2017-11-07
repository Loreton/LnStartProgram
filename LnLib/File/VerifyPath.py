#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.33.20
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    sys     import exit as sysExit
from    pathlib import Path, PurePath, WindowsPath

# from LnLib.File.LnPath          import Path as LnPath

from LnLib.Common.Exit          import Exit       as LnExit
from LnLib.Common.LnLogger      import SetLogger


def VerifyPath(path, exitOnError=True):
    logger = SetLogger(__package__, stackNum=1) # log the caller

    logger.info('verifying path: {0} [{1}]'.format(path, type(path)))

    try:
        if isinstance(path, str): path = Path(path)
        path.resolve()

        pathExists = path.exists()

    except (Exception) as why:
        pathExists = False
        logger.error(str(why))


    if pathExists:
        retPath = Path(path)
        logger.info('it exists.')

    else:
        retPath = None
        logger.error("it doesn't exists.")
        if exitOnError:
            LnExit(10, "{} doesn't exists".format(path))


    return retPath