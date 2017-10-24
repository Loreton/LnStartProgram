#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 12.55.17
# -----------------------------------------------

import  os, sys
from    pathlib import Path, PurePath         # dalla versione 3.4
from    time import sleep

from LnLib.Common.LnLogger     import SetLogger   as LnSetLogger
from LnLib.Common.Exit         import Exit        as LnExit
from LnLib.System.SetOsEnv     import setOsEnv    as LnDetOsEnv
from LnLib.File.VerifyPath     import VerifyPath  as LnVerifyPath
from LnLib.System.RunProgram   import RunProgram  as LnRunProgram
from LnLib.File.VerifyPath     import VerifyPath  as LnVerifyPath


#########################################################################
#
#########################################################################
def CalculateMainDirs(gv, myArgs):
    logger = LnSetLogger(__package__)

        # ---------------------------------------------------------------
        # - prepare dirs
        # - devo partire dalla directory del caller in quanto mi serve
        # - la root di partenza di LnDisk
        # ---------------------------------------------------------------
    scriptMain         = Path(sys.argv[0]).resolve()

    gv.env.StartDir    = LnVerifyPath(myArgs['callerDir'])
    gv.env.Drive       = LnVerifyPath(gv.env.StartDir.drive)
    gv.env.RootDir     = LnVerifyPath(gv.env.StartDir.parent)

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
                LnRunProgram("executing SUBST command:", ['subst', substDrive, gv.subst.MountDir])
                sleep(1) #diamo tempo affinché avvenga il montaggio

            # verifico che il comando di SUBST sia andato a buon fine...
            gv.subst.FreeDir = LnVerifyPath(Path(substDrive).joinpath('/LnFree'), exitOnError=False)
            if gv.subst.FreeDir:
                gv.subst.Drive      = LnVerifyPath(Path(substDrive))
                gv.subst.StartDir   = LnVerifyPath(gv.subst.Drive.joinpath('/LnStart'))

                    # - setting and logging
                LnDetOsEnv('Ln.subst.Drive'     ,gv.subst.Drive)
                LnDetOsEnv('Ln.subst.MountDir'  ,gv.subst.MountDir)
                LnDetOsEnv('Ln.subst.StartDir'  ,gv.subst.StartDir)

            else:
                logger.warning("il comando di SUBST non ha avuto successo...")
                input()

            # - se abbiamo attivato il SUBST,
            # - modifichiamo anche le MAIN variables
            gv.env.Drive        = gv.subst.Drive
            gv.env.RootDir      = gv.subst.Drive
            gv.env.StartDir     = gv.subst.StartDir


    # - re-impostiamo le vriabili di ambiente
    LnDetOsEnv('Ln.Drive'     ,gv.env.Drive)
    LnDetOsEnv('Ln.RootDir'   ,gv.env.RootDir)
    LnDetOsEnv('Ln.StartDir'  ,gv.env.StartDir)


