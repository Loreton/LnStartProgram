#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.41
# -----------------------------------------------
from    pathlib import Path
import  platform, sys, os


# import Source as Prj

# =============================================
# = Parsing
# =============================================
def SetExecutor(d_vars, logger, fEXECUTE=False):
    assert isinstance(d_vars, dict)

    CMDList = []

        # -------------------------------------------------
        # - scroling dictionary_variables
        # -------------------------------------------------

    OSbits = platform.architecture()[0]
    logger.info("Stiamo lavorando con Executor", OSbits)

    my_exe = Path.LnCheckPath(d_vars['executorEXE'], errorOnPathNotFound=True)
    exe_to_run = Path.LnCheckPath(d_vars['executorEXE'], errorOnPathNotFound=True)

        # faccio uso delle LnMonkeyFunctions
    if fEXECUTE:
        exe_to_run.LnCopy(target=my_exe, logger=logger)

        my_ini = Path.LnCheckPath(d_vars['iniFile'], errorOnPathNotFound=True)
        my_ini.LnBackup(d_vars['backupDir'], logger=logger)
    else:
        logger.info('skipping copyfile due to dry-run')

    CMDList.append(my_exe)
    CMDList.append('-s')

    return CMDList


