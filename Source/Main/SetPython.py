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
def SetPython(gVars, logger, fEXECUTE=False):
    assert isinstance(gVars, dict)

    CMDList = []

        # -------------------------------------------------
        # - scroling dictionary_variables
        # -------------------------------------------------
    for _label, _value in gVars.items():
        logger.info('envar {0:<15}: {1}'.format(_label, _value))
        os.environ[_label] = str(_value)
        if _label.lower() == 'workingdir':
            os.chdir(_value)

    my_exe = Path.LnCheckPath(gVars['vscode_exe'])

    CMDList.append(my_exe)


    return CMDList


