#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.41
# -----------------------------------------------
from    pathlib import Path
import  platform


import Source as Prj

# =============================================
# = Parsing
# =============================================
def SetExecutor(gv, iniVar):
    # ----- common part into the Prj modules --------
    Ln     = Prj.LnLib
    logger = Ln.SetLogger(__name__)
    # -----------------------------------------------

    CMDList = []

    EXE, EXE32, EXE64 = iniVar.executorEXE.split('\n')
    DLL, DLL32, DLL64 = iniVar.hookwinrDLL.split('\n')

    OSbits = platform.architecture()[0]
    logger.info("Stiamo lavorando con Executor: {}".format(OSbits))
    if OSbits.lower() == "64bit":
        myExe = Path(EXE64)
        myDll = Path(DLL64)
    else:
        myExe = Path(EXE32)
        myDll = Path(DLL32)

        # faccio uso delle LnMonkeyFunctions
    myExe.LnCopy(EXE, vSize=True)
    myDll.LnCopy(DLL, vSize=True)

    myIni = Path(iniVar.iniFile)
    myIni.LnBackup(iniVar.backupDir)

    CMDList.append(EXE)
    CMDList.append('-s')


    return CMDList
    Ln.Exit(9999, 'exit temporanea')

