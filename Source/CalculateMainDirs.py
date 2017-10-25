#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# __author__  : 'Loreto Notarantonio'
# __version__ : '25-10-2017 17.32.14'
#
# -----------------------------------------------

import  os, sys
from    pathlib import Path, PurePath         # dalla versione 3.4
from    time import sleep

from LnLib.Common.LnLogger     import SetLogger   as LnSetLogger
from LnLib.Common.Exit         import Exit        as LnExit
from LnLib.Dict.LnDict_DotMap  import DotMap      as LnDict
from LnLib.System.SetOsEnv     import setOsEnv    as LnDetOsEnv
from LnLib.File.VerifyPath     import VerifyPath  as LnVerifyPath
from LnLib.System.RunProgram   import RunProgram  as LnRunProgram
from LnLib.File.VerifyPath     import VerifyPath  as LnVerifyPath


#########################################################################
#
#########################################################################
def CalculateMainDirs(myArgs, fDEBUG=False):
    logger = LnSetLogger(__package__)

        # ---------------------------------------------------------------
        # - prepare dirs
        # - devo partire dalla directory del caller in quanto mi serve
        # - la root di partenza di LnDisk
        # ---------------------------------------------------------------
    scriptMain         = Path(sys.argv[0]).resolve()


    ln = LnDict()
    ln.RootDir    = LnVerifyPath(myArgs['rootDir'])
    ln.Drive      = LnVerifyPath(ln.RootDir.drive)
    ln.StartDir   = LnVerifyPath(ln.RootDir.joinpath('LnStart'))

    if fDEBUG: ln.printTree(header="ln. variables", fPAUSE=True)

        # --------------------------------------------
        # - se e' richiesto un drive SUBST ...
        # - impostiamo anche i path per quel drive
        # --------------------------------------------
    if myArgs['subst']:
        subst = LnDict()
        substDrive = myArgs['subst'].strip()
        if substDrive.lower() in ['x:', 'y:', 'w:', 'z:']:
            subst.MountDir  = ln.RootDir
            if not Path(substDrive).exists():
                LnRunProgram("executing SUBST command:", ['subst', substDrive, subst.MountDir])
                sleep(1) #diamo tempo affinché avvenga il montaggio

            # verifico che il comando di SUBST sia andato a buon fine...
            subst.FreeDir = LnVerifyPath(Path(substDrive).joinpath('/LnFree'), exitOnError=False)
            if subst.FreeDir:
                subst.Drive      = LnVerifyPath(Path(substDrive))
                subst.StartDir   = LnVerifyPath(subst.Drive.joinpath('/LnStart'))

                    # - setting and logging
                LnDetOsEnv('Ln_subst_Drive'     ,subst.Drive)
                LnDetOsEnv('Ln_subst_MountDir'  ,subst.MountDir)
                LnDetOsEnv('Ln_subst_StartDir'  ,subst.StartDir)

            else:
                logger.warning("il comando di SUBST non ha avuto successo...")
                input()

            # - se abbiamo attivato il SUBST,
            # - modifichiamo anche le MAIN variables
            ln.Drive        = subst.Drive
            ln.RootDir      = subst.Drive
            ln.StartDir     = subst.StartDir


    # - re-impostiamo le vriabili di ambientez
    LnDetOsEnv('Ln_Drive'     ,ln.Drive)
    LnDetOsEnv('Ln_RootDir'   ,ln.RootDir)
    LnDetOsEnv('Ln_StartDir'  ,ln.StartDir)

    if fDEBUG:
        subst.printTree(header="subst_variables", fPAUSE=False)
        ln.printTree(header="ln_variables", fPAUSE=True)

