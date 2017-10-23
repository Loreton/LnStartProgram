#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 09.55.12
# -----------------------------------------------
from    sys import exit as sysExit
# import os

from os import chdir


# =============================================
# = Parsing
# =============================================
def SetTotalCommander(gv, iniVar):
    logger = gv.Prj.SetLogger(__package__)
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
        iniVar[varName] = gv.Prj.VerifyPath(gv, varValue, exitOnError=fMANDATORY)
        gv.Prj.setOsEnv(gv, varName, iniVar[varName])
        if varName.lower() == 'workingdir':
            chdir(str(iniVar[varName]))

    if gv.env.OSbits.lower() == "intel64":
        TCexe = gv.Prj.VerifyPath(gv, iniVar.TCDir.joinpath('realApp/WinCmd/TOTALCMD64.exe'))
        if gv.fDEBUG: print ("Stiamo lavorando con TotalCommander 64 Bits")
    else:
        TCexe = gv.Prj.VerifyPath(gv, iniVar.TCDir.joinpath('realApp/WinCmd/TOTALCMD.exe'))
        if gv.fDEBUG: print ("Stiamo lavorando con TotalCommander 32 Bits")


    CMDList.append(TCexe)
    CMDList.append('/I={}'.format(iniVar.tcIniFile))
    CMDList.append('/F={}'.format(iniVar.ftpIniFile))

    return CMDList

