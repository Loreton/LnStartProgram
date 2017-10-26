#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.56.43
# -----------------------------------------------
from  subprocess import Popen
from  pathlib import PureWindowsPath, WindowsPath         # dalla versione 3.4


from LnLib.Common.LnLogger      import SetLogger

#########################################################################
#
#########################################################################
def RunProgram(textMsg, CMDList):
    logger = SetLogger(__package__)

        # --------------------------------------------------
        # - Nella lista del comando potrebbero essere presenti
        # - path di file in formato PurePath... o simili
        # - e devo convertirli in str prima di lanciarli
        # --------------------------------------------------
    logger.info(textMsg)
    myCMDList = []
    for line in CMDList:
        if isinstance(line, (PureWindowsPath, WindowsPath )):
            line = str(line)
        myCMDList.append(line)
        logger.info('   ' + line)

    procID = Popen(myCMDList, shell=False, universal_newlines=True)
    # print(procID)


