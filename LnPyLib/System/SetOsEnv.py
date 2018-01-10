#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-01-2018 08.24.12
#
# ####################################################################################################################

import os
from .. Common.LnLogger import SetLogger
from .. File.VerifyPath import VerifyPath   as LnVerifyPath

#########################################################################
#
#########################################################################
def setVar(varName, varValue, fDEBUG=False):
    logger = SetLogger(__name__)
    msg = '{0:<20} : {1}'.format(varName, varValue)
    logger.info(msg)
    os.environ[varName] = str(varValue)


#########################################################################
# - Setting PATH
#########################################################################
def setPath(pathName, pathValue, fMANDATORY=True, sepChar=';'):
    newPATH = os.getenv(pathName)
    paths = pathValue.split(sepChar)
    for path in paths:
        path    = LnVerifyPath(path, exitOnError=fMANDATORY)
        path    = '{0};'.format(path)           # add ;
        newPATH = newPATH.replace(path, '')     # delete if exists
        newPATH = path + newPATH                # add new one

    setVar(pathName, newPATH, fDEBUG=False)


#########################################################################
# imposta le variabili passate come dictionary
#########################################################################
def setVars(dictVARS, fDEBUG=False):

        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for varName, varValue in dictVARS.items():
        if varName.startswith('opt.'):
            varName = varName[4:]
            fMANDATORY = False
        else:
            fMANDATORY = True

        paths = []

        for path in varValue.split('\n'):
            realPath = LnVerifyPath(path, exitOnError=fMANDATORY)
            if realPath:
                paths.append(str(realPath))

        setVar(varName, ';'.join(paths), fDEBUG=fDEBUG)



#########################################################################
# imposta le path passate come dictionary
#########################################################################
def setPaths(dictVARS):
    for pathName, pathValue in dictVARS.items():
        if pathName.startswith('opt.'):
            fMANDATORY = False
        else:
            fMANDATORY = True

        # -------------------------------------------------
        # - Setting PATH
        # -------------------------------------------------
        setPath('PATH', pathValue, fMANDATORY=fMANDATORY, sepChar='\n')
