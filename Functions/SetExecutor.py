#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 14.41.28
# -----------------------------------------------
from    sys import exit as sysExit
import os
from pathlib  import Path




# =============================================
# = Parsing
# =============================================
def SetExecutor(gv, iniVar):
    logger = gv.Prj.SetLogger(__package__)
    CMDList = []


    EXE, EXE32, EXE64 = iniVar.executorEXE.split('\n')
    DLL, DLL32, DLL64 = iniVar.hookwinrDLL.split('\n')

    if gv.fDEBUG: print ("Stiamo lavorando con Executor: {}".format(gv.env.OSbits))

    if gv.env.OSbits.lower() == "intel64":
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

    gv.Ln.Exit(9999, 'exit temporanea')
