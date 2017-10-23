#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.55.11
# -----------------------------------------------

import  os, sys
from    pathlib import Path, PurePath         # dalla versione 3.4
# import  pathlib as p         # dalla versione 3.4
from    time import sleep

logger = None
#########################################################################
#
#########################################################################
# def setOsEnv(varName, varValue):
#     logger.info('{0:<20} : {1}'.format(varName, varValue))
#     os.environ[varName] = str(varValue)

#########################################################################
#
#########################################################################
def setSUBST(drive, substDir):
    CMDList = []
    CMDList.append('subst')
    CMDList.append(str(drive))
    CMDList.append(str(substDir))
    gv.Prj.LaunchProgram(gv, "executing SUBST command:", CMDList)
    sleep(1) #diamo tempo che avvenga il montaggio


#########################################################################
#
#########################################################################
def CalculateMainDirs(gVars, myArgs):
    global logger, gv
    gv     = gVars
    logger = gv.Ln.SetLogger(__name__)
    logger.info('sono qui')
    gv.Ln.Exit(9999, "temporary exit")

        # ---------------------------------------------------------------
        # - prepare dirs
        # - devo partire dalla directory del caller in quanto mi serve
        # - la root di partenza di LnDisk
        # ---------------------------------------------------------------
    scriptMain  = Path(sys.argv[0]).resolve()

    gv.env.StartDir    = gv.Prj.VerifyPath(gv, myArgs['callerDir'])
    gv.env.Drive       = gv.Prj.VerifyPath(gv, gv.env.StartDir.drive)
    gv.env.RootDir     = gv.Prj.VerifyPath(gv, gv.env.StartDir.parent)

        # --------------------------------------------
        # - se e' richiesto un drive SUBST ...
        # - impostiamo anche i path per quel drive
        # --------------------------------------------
    if myArgs['subst']:
        gv.subst = gv.Prj.LnClass()
        substDrive = myArgs['subst'].strip()
        if substDrive.lower() in ['x:', 'y:', 'w:', 'z:']:
            gv.subst.MountDir  = gv.env.RootDir
            if not Path(substDrive).exists():
                setSUBST(substDrive, gv.subst.MountDir )

            # verifico che il comando di SUBST sia andato a buon fine...
            gv.subst.FreeDir = gv.Prj.VerifyPath(gv, Path(substDrive).joinpath('/LnFree'), exitOnError=False)
            if gv.subst.FreeDir:
                gv.subst.Drive      = gv.Prj.VerifyPath(gv, Path(substDrive))
                gv.subst.StartDir   = gv.Prj.VerifyPath(gv, gv.subst.Drive.joinpath('/LnStart'))

                    # - setting and logging
                gv.Prj.setOsEnv(gv, 'Ln.subst.Drive'     ,gv.subst.Drive)
                gv.Prj.setOsEnv(gv, 'Ln.subst.MountDir'  ,gv.subst.MountDir)
                gv.Prj.setOsEnv(gv, 'Ln.subst.StartDir'  ,gv.subst.StartDir)

            else:
                logger.warning("il comando di SUBST non ha avuto successo...")
                input()

            # - se abbiamo attivato il SUBST,
            # - modifichiamo anche le MAIN variables
            gv.env.Drive        = gv.subst.Drive
            gv.env.RootDir      = gv.subst.Drive
            gv.env.StartDir     = gv.subst.StartDir


    # - re-impostiamo le vriabili di ambiente
    gv.Prj.setOsEnv(gv, 'Ln.Drive'     ,gv.env.Drive)
    gv.Prj.setOsEnv(gv, 'Ln.RootDir'   ,gv.env.RootDir)
    gv.Prj.setOsEnv(gv, 'Ln.StartDir'  ,gv.env.StartDir)

