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

    my_exe = Path(d_vars['executorEXE']).resolve()
    my_dll = Path(d_vars['hookwinrDLL']).resolve()

    if OSbits == "64bit":
        exe_to_run = Path(d_vars['executor64EXE']).resolve()
        dll_to_run = Path(d_vars['hookwinr64DLL']).resolve()
    else:
        exe_to_run = Path(d_vars['executor32EXE']).resolve()
        dll_to_run = Path(d_vars['hookwinr32DLL']).resolve()

        # faccio uso delle LnMonkeyFunctions
    if fEXECUTE:
        exe_to_run.LnCopy(target=my_exe, logger=logger)
        dll_to_run.LnCopy(target=my_dll, logger=logger)

        my_ini = Path(d_vars['iniFile'])
        my_ini.LnBackup(d_vars['backupDir'], logger=logger)
    else:
        logger.info('skipping copyfile due to dry-run')

    CMDList.append(my_exe)
    CMDList.append('-s')


    return CMDList


