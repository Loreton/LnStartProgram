#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.41
# -----------------------------------------------
from    pathlib import Path
from    LnLib.Common.LnLogger import SetLogger

import  platform

import LnLib.Monkey.LnMonkeyFunctions # per .LnCopy e .LnBackup

# =============================================
# = Parsing
# =============================================
def SetExecutor(iniVar):
    logger = SetLogger(__package__)

    CMDList = []

    EXE, EXE32, EXE64 = iniVar.executorEXE.split('\n')
    DLL, DLL32, DLL64 = iniVar.hookwinrDLL.split('\n')

    OSbits = platform.architecture()[0]
    logger.info("Stiamo lavorando con Executor: {}".format(OSbits))
    if OSbits.lower() == "64bit":
        myExe = Path(EXE64) # faccio uso delle LnMonkeyFunctions
        myDll = Path(DLL64)
    else:
        myExe = Path(EXE32)
        myDll = Path(DLL32)

    myExe.LnCopy(EXE, vSize=True, logger=logger)
    myDll.LnCopy(DLL, vSize=True, logger=logger)

    myIni = Path(iniVar.iniFile)
    myIni.LnBackup(iniVar.backupDir)

    CMDList.append(EXE)
    CMDList.append('-s')


    return CMDList

    # LnExit(9999, 'exit temporanea')
