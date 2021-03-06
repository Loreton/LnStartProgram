#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-06-2019 13.03.48
#
# ####################################################################################################################

import os
# logger = None
# from .. Logger.LnLogger import SetLogger
# from .. File.VerifyPath import VerifyPath   as LnVerifyPath

# def setLogger(myLogger):
#     global logger
#     logger = myLogger

#########################################################################
#
#########################################################################
def setVar(varName, varValue, fDEBUG=False, logger=None):
    # global logger
    # logger = myLogger
    # logger = SetLogger(__name__)
    msg = '{0:<20} : {1}'.format(varName, varValue)
    if logger: logger.info(msg)
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
def setVars(dictVARS, mandatory=False, fDEBUG=False):

        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for varName, varValue in dictVARS.items():
        # if varName.startswith('opt.'):
        #     varName = varName[4:]
        #     fMANDATORY = False
        # else:
        #     fMANDATORY = True

        paths = []

        for path in varValue.split('\n'):
            realPath = LnVerifyPath(path, exitOnError=mandatory)
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
