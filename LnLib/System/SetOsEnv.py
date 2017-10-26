#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
# updated by Loreto: 24-10-2017 12.53.07
#
# ####################################################################################################################

from os                           import environ, getenv
from LnLib.Common.LnLogger import SetLogger
from LnLib.File.VerifyPath        import VerifyPath   as LnVerifyPath

#########################################################################
#
#########################################################################
# def setOsEnv(varName, varValue, fDEBUG=False):
def setVar(varName, varValue, fDEBUG=False):
    logger = SetLogger(__package__)
    msg = '{0:<20} : {1}'.format(varName, varValue)
    logger.info(msg)
    if fDEBUG: print (msg)
    environ[varName] = str(varValue)


#########################################################################
# - Setting PATH
#########################################################################
def setPath(pathName, pathValue, fMANDATORY=True, sepChar=';'):
    logger = SetLogger(__package__)
    newPATH = getenv(pathName)
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
    logger = SetLogger(__package__)

        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for varName, varValue in dictVARS.items():
        if varName.startswith('opt.'):
            varName = varName[4:]
            fMANDATORY = False
        else:
            fMANDATORY = True
        path = LnVerifyPath(varValue, exitOnError=fMANDATORY)
        setVar(varName, path, fDEBUG=fDEBUG)



#########################################################################
# imposta le path passate come dictionary
#########################################################################
def setPaths(dictVARS):
    logger = SetLogger(__package__)
    for pathName, pathValue in dictVARS.items():
        if pathName.startswith('opt.'):
            fMANDATORY = False
        else:
            fMANDATORY = True

        # -------------------------------------------------
        # - Setting PATH
        # -------------------------------------------------
        setPath('PATH', pathValue, fMANDATORY=True, sepChar='\n')
