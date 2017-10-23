#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 10.10.39
# -----------------------------------------------


from    os     import environ, getenv
from    sys     import exit as sysExit
from    pathlib import Path, PurePath


#########################################################################
#
#########################################################################
def setOsEnv(gv, varName, varValue, fDEBUG=False):
    msg = '{0:<20} : {1}'.format(varName, varValue)
    gv.logger.info(msg)
    if fDEBUG: print (msg)
    environ[varName] = str(varValue)



#########################################################################
# - Setting PATH
#########################################################################
def setPath(pathName, pathValue, fMANDATORY=True, sepChar=';'):
    newPATH = getenv(pathName)
    paths = pathValue.split(sepChar)
    for path in paths:
        path    = gv.Prj.VerifyPath(gv, path, exitOnError=fMANDATORY)
        path    = '{0};'.format(path)           # add ;
        newPATH = newPATH.replace(path, '')     # delete if exists
        newPATH = path + newPATH                # add new one

    setOsEnv(gv, pathName, newPATH, fDEBUG=False)


#########################################################################
# imposta le variabili passate come dictionary
#########################################################################
def SetEnvVars(gVars, dictVARS):
    global gv, logger
    gv = gVars
    logger = gv.Prj.SetLogger(__name__)

        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for varName, varValue in dictVARS.items():
        if varName.startswith('opt.'):
            varName = varName[4:]
            fMANDATORY = False
        else:
            fMANDATORY = True
        path = gv.Prj.VerifyPath(gv, varValue, exitOnError=fMANDATORY)
        setOsEnv(gv, varName, path, fDEBUG=gv.fDEBUG)



#########################################################################
# imposta le path passate come dictionary
#########################################################################
def SetEnvPaths(gVars, dictVARS):
    global gv, logger
    gv = gVars
    logger = gv.Prj.SetLogger(__name__)
    for pathName, pathValue in dictVARS.items():
        if pathName.startswith('opt.'):
            fMANDATORY = False
        else:
            fMANDATORY = True

        # -------------------------------------------------
        # - Setting PATH
        # -------------------------------------------------
        setPath('PATH', pathValue, fMANDATORY=True, sepChar='\n')
