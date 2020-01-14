#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.47
# -----------------------------------------------
import os, sys
import  platform
from pathlib import Path


# =============================================
# = Parsing
# =============================================
def SetTotalCommander(d_vars, logger):
    assert isinstance(d_vars, dict)

    CMDList = []

        # -------------------------------------------------
        # - scroling dictionary_variables
        # -------------------------------------------------
    for _label, _path in d_vars.items():
        _path = Path.LnVerify(_path, errorOnPathNotFound=True)

        logger.info('envar {0:<15}: {1}'.format(_label, _path))
        os.environ[_label] = str(_path)
        if _label.lower() == 'workingdir':
            os.chdir(_path)


    OSbits = platform.architecture()[0]
    logger.info( "Stiamo lavorando con TotalCommander {0}".format(OSbits))
    if OSbits == "64bit":
        # TCexe = Path.LnVerify(d_vars['Ln_TC_PATH'] + '/realApp/WinCmd/TOTALCMD64.exe', errorOnPathNotFound=True)
        TCexe = Path.LnVerify(d_vars['Ln_TC_64EXE'], errorOnPathNotFound=True)
    else:
        # TCexe = Path.LnVerify(d_vars['Ln_TC_PATH'] + '/realApp/WinCmd/TOTALCMD.exe', errorOnPathNotFound=True)
        TCexe = Path.LnVerify(d_vars['Ln_TC_32EXE'], errorOnPathNotFound=True)




    CMDList.append(str(TCexe))
    CMDList.append('/I={}'.format(d_vars['Ln_TC_IniFile']))
    CMDList.append('/F={}'.format(d_vars['Ln_TC_ftpIniFile']))

    return CMDList

