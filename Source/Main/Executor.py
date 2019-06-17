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
def SetExecutor(d_vars, logger):
    assert isinstance(d_vars, dict)

    CMDList = []

        # -------------------------------------------------
        # - scroling dictionary_variables
        # -------------------------------------------------
    # for _label, _path in d_vars.items():
    #     _path = Path(_path).resolve()
    #     if not _path.exists():
    #         logger.error(_path, "doesn't exists.")
    #         print("{0} doesn't exists".format(_path))
    #         sys.exit(1)

    #     logger.info('envar {0:<15}: {1}'.format(_label, _path))
    #     os.environ[_label] = str(_path)
    #     if _label.lower() == 'workingdir':
    #         os.chdir(_path)

    EXE, EXE32, EXE64 = d_vars['executorEXE'] # .split('\n')
    DLL, DLL32, DLL64 = d_vars['hookwinrDLL'] # .split('\n')

    OSbits = platform.architecture()[0]
    logger.info("Stiamo lavorando con Executor: {0}".format(OSbits))
    if OSbits == "64bit":
        myExe = Path(EXE64)
        myDll = Path(DLL64)
    else:
        myExe = Path(EXE32)
        myDll = Path(DLL32)

        # faccio uso delle LnMonkeyFunctions
    myExe.LnCopy(target=EXE, logger=logger)
    myDll.LnCopy(target=DLL, logger=logger)

    myIni = Path(d_vars['iniFile'])
    myIni.LnBackup(d_vars['backupDir'], logger=logger)

    CMDList.append(EXE)
    CMDList.append('-s')


    return CMDList
    Ln.Exit(9999, 'exit temporanea')

