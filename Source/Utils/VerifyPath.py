#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-06-2019 17.04.39
#
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    pathlib import Path

def checkPath(path, logger, exitOnError=True):
    '''
    verify if the path exists.
    return:
        None    : if NOT exists
        realPath: if exists
    '''
    logger = SetLogger(__name__) # log the caller

    logger.info('verifying path: {0} [{1}]'.format(path, type(path)))

    realPath = None
    try:
        if isinstance(path, str):
            path = Path(path)
        realPath = path.resolve()
        realPath.exists()   # exeption if not exists

    except (Exception) as why:
        logger.error(str(why))
        logger.error("it doesn't exists.")
        if exitOnError:
            LnExit(10, "{} doesn't exists".format(path))


    logger.info('returning path: {0} [{1}]'.format(realPath, type(realPath)))
    SetLogger(__name__, exiting=True) # log the caller
    return realPath