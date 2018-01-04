#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 10.57.58
#
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    pathlib import Path

from .. Common.Exit          import Exit       as LnExit
from .. Common.LnLogger      import SetLogger


def VerifyPath(path, exitOnError=True):
    '''
    verify if the path exists.
    return:
        realPath: if exists
        None    : if NOT exists
    '''
    logger = SetLogger(__name__, stackNum=1) # log the caller

    logger.info('verifying path: {0} [{1}]'.format(path, type(path)))

    retPath = None
    try:
        if isinstance(path, str):
            path = Path(path)
        retPath = path.resolve()
        retPath.exists()   # exeption if not exists

    except (Exception) as why:
        logger.error(str(why))
        logger.error("it doesn't exists.")
        if exitOnError:
            LnExit(10, "{} doesn't exists".format(path))


    logger.info('returning path: {0} [{1}]'.format(retPath, type(retPath)))
    return retPath