#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 19-10-2017 16.19.02
# -----------------------------------------------

import  os, sys
from    pathlib import Path, PurePath         # dalla versione 3.4
# import  pathlib as p         # dalla versione 3.4
from    time import sleep

logger = None
#########################################################################
#
#########################################################################
def setOsEnv(varName, varValue):
    logger.info('{0:<20} : {1}'.format(varName, varValue))
    os.environ[varName] = str(varValue)

#########################################################################
#
#########################################################################
def setSUBST(drive, substDir):
    CMDList = []
    CMDList.append('subst')
    CMDList.append(str(drive))
    CMDList.append(str(substDir))
    gv.Ln.LaunchProgram(gv, "executing SUBST command:", CMDList)
    sleep(1) #diamo tempo che avvenga il montaggio


#########################################################################
#
#########################################################################
def CalculateMainDirs(gVars, myArgs):
    global logger, gv
    gv     = gVars
    logger = gv.Ln.SetLogger(__package__)

        # ---------------------------------------------------------------
        # - prepare dirs
        # - devo partire dalla directory del caller in quanto mi serve
        # - la root di partenza di LnDisk
        # ---------------------------------------------------------------
    scriptMain  = Path(sys.argv[0]).resolve()

    gv.env.StartDir    = gv.Ln.VerifyPath(gv, myArgs['callerDir'])
    gv.env.Drive       = gv.Ln.VerifyPath(gv, gv.env.StartDir.drive)
    gv.env.RootDir     = gv.Ln.VerifyPath(gv, gv.env.StartDir.parent)
    gv.env.LoretoDir   = gv.Ln.VerifyPath(gv, gv.env.RootDir.joinpath('Loreto'))
    gv.env.FreeDir     = gv.Ln.VerifyPath(gv, gv.env.RootDir.joinpath('LnFree'))
    gv.env.GitRepoDir  = gv.Ln.VerifyPath(gv, gv.env.RootDir.joinpath('GIT-REPO'))

         # - setting and logging
    setOsEnv('Ln.Drive'     ,gv.env.Drive)
    setOsEnv('Ln.RootDir'   ,gv.env.RootDir)
    setOsEnv('Ln.StartDir'  ,gv.env.StartDir)
    setOsEnv('Ln.LoretoDir' ,gv.env.LoretoDir)
    setOsEnv('Ln.FreeDir'   ,gv.env.FreeDir)
    setOsEnv('Ln.GitRepoDir',gv.env.GitRepoDir)


        # --------------------------------------------
        # - se e' richiesto un drive SUBST ...
        # - impostiamo anche i path per quel drive
        # --------------------------------------------
    if myArgs['subst']:
        gv.subst = gv.Ln.LnClass()
        substDrive = myArgs['subst'].strip()
        if substDrive.lower() in ['x:', 'y:', 'w:', 'z:']:
            gv.subst.MountDir  = gv.env.RootDir
            if not Path(substDrive).exists():
                setSUBST(substDrive, gv.subst.MountDir )

            # verifico che il comando di SUBST sia andato a buon fine...
            gv.subst.FreeDir = gv.Ln.VerifyPath(gv, Path(substDrive).joinpath('/LnFree'), exitOnError=False)
            if gv.subst.FreeDir:
                gv.subst.Drive      = gv.Ln.VerifyPath(gv, Path(substDrive))
                gv.subst.LoretoDir  = gv.Ln.VerifyPath(gv, gv.subst.Drive.joinpath('/Loreto'))
                gv.subst.StartDir   = gv.Ln.VerifyPath(gv, gv.subst.Drive.joinpath('/LnStart'))
                gv.subst.GitRepoDir = gv.Ln.VerifyPath(gv, gv.subst.Drive.joinpath('/GIT-REPO'))

                    # - setting and logging
                setOsEnv('Ln.subst.Drive'     ,gv.subst.Drive)
                setOsEnv('Ln.subst.MountDir'  ,gv.subst.MountDir)
                setOsEnv('Ln.subst.StartDir'  ,gv.subst.StartDir)
                setOsEnv('Ln.subst.LoretoDir' ,gv.subst.LoretoDir)
                setOsEnv('Ln.subst.FreeDir'   ,gv.subst.FreeDir)
                setOsEnv('Ln.subst.GitRepoDir',gv.subst.GitRepoDir)

            else:
                logger.warning("il comando di SUBST non ha avuto successo...")
                input()


        # - se abbiamo attivato il SUBST,
        # - facciamo riferimento ad esso
    if gv.subst.FreeDir:
        gv.env.Drive        = gv.subst.Drive
        gv.env.RootDir      = gv.subst.Drive
        gv.env.StartDir     = gv.subst.StartDir
        gv.env.LoretoDir    = gv.subst.LoretoDir
        gv.env.FreeDir      = gv.subst.FreeDir
        gv.env.GitRepoDir   = gv.subst.GitRepoDir

        # - re-impostiamo le vriabili di ambiente
        setOsEnv('Ln.Drive'     ,gv.env.Drive)
        setOsEnv('Ln.RootDir'   ,gv.env.RootDir)
        setOsEnv('Ln.StartDir'  ,gv.env.StartDir)
        setOsEnv('Ln.LoretoDir' ,gv.env.LoretoDir)
        setOsEnv('Ln.FreeDir'   ,gv.env.FreeDir)
        setOsEnv('Ln.GitRepoDir',gv.env.GitRepoDir)

