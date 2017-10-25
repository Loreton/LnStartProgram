#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.47
# -----------------------------------------------
from os     import chdir
import  platform


from LnLib.Common.LnLogger import SetLogger  as LnSetLogger
from LnLib.System.SetOsEnv import setOsEnv   as LnDetOsEnv
from LnLib.File.VerifyPath import VerifyPath as LnVerifyPath

# =============================================
# = Parsing
# =============================================
def SetTotalCommander(iniVar):
    logger = LnSetLogger(__package__)
    CMDList = []

        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for varName, varValue in iniVar.items():
        if varName.startswith('opt.'):
            varName = varName[4:]
            fMANDATORY = False
        else:
            fMANDATORY = True

        # salviamolo in formato Path
        iniVar[varName] = LnVerifyPath(varValue, exitOnError=fMANDATORY)
        LnDetOsEnv(varName, iniVar[varName])
        if varName.lower() == 'workingdir':
            chdir(str(iniVar[varName]))


    OSbits = platform.architecture()[0]
    logger.info( "Stiamo lavorando con TotalCommander {}".format(OSbits))
    if OSbits.lower() == "64bit":
        TCexe = LnVerifyPath(iniVar.TCDir.joinpath('realApp/WinCmd/TOTALCMD64.exe'))
    else:
        TCexe = LnVerifyPath(iniVar.TCDir.joinpath('realApp/WinCmd/TOTALCMD.exe'))


    CMDList.append(TCexe)
    CMDList.append('/I={}'.format(iniVar.tcIniFile))
    CMDList.append('/F={}'.format(iniVar.ftpIniFile))

    return CMDList
