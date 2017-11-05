#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# __author__  : 'Loreto Notarantonio'
# __version__ : '26-10-2017 17.53.21'
#
# -----------------------------------------------

import  os, sys
from    pathlib                  import Path, PurePath         # dalla versione 3.4
from    LnLib.File.LnPath        import Path as LnPath

from    time                     import sleep

from    LnLib.Common.LnLogger    import SetLogger

from    LnLib.Common.Exit        import Exit        as LnExit
from    LnLib.Dict.LnDict_DotMap import DotMap      as LnDict
from    LnLib.File.VerifyPath    import VerifyPath  as LnVerifyPath
from    LnLib.System.RunProgram  import RunProgram  as LnRunProgram
from    LnLib.System             import SetOsEnv    as OsEnv




#########################################################################
# - Ln_Drive, Ln_rootDir e Ln_StartDir e GIT-REPO.
#########################################################################
def CalculateMainDirs(myArgs, fDEBUG=False):
    logger = SetLogger(__package__)

        # ---------------------------------------------------------------
        # - prepare dirs
        # - mi server la rootDir di partenza di LnDisk
        # - cerco la subDir LnStart o LnFree nel path di scriptMain
        # ---------------------------------------------------------------
    myDirectories = ('LnStart', 'LnFree', 'GIT-REPO')

    if myArgs['root_dir']:
        rootDir = Path(myArgs['root_dir'])
        drive, *rest = rootDir.parts
    else:
        FOUND = False
        ''' pathlib
        scriptMain   = Path(sys.argv[0]).resolve()
        drive, *rest = scriptMain.parts
        rootDir      = Path(drive).resolve()
        '''

        scriptMain   = LnPath(sys.argv[0]).realpath()
        drive, *rest = scriptMain.splitall()
        rootDir      = drive.realpath()

        for dirname in rest:
            if dirname in myDirectories:
                FOUND = True
                break
            else:
                rootDir = rootDir.joinpath(dirname)

        if not FOUND:
            LnExit(21, "root_dir NOT found.")


    ln = LnDict()
    ln.RootDir    = LnVerifyPath(rootDir)
    ln.Drive      = LnVerifyPath(drive)

    if fDEBUG: ln.printTree(header="ln. variables", fPAUSE=True)

        # --------------------------------------------
        # - se e' richiesto un drive SUBST ...
        # - impostiamo anche i path per quel drive
        # --------------------------------------------
    if myArgs['subst']:
        subst = LnDict()
        substDrive = LnPath(myArgs['subst'].strip())
        if substDrive.lower() in ['x:', 'y:', 'w:', 'z:']:
            subst.MountDir  = ln.RootDir
            if not substDrive.exists():
                LnRunProgram("executing SUBST command:", ['subst', substDrive, subst.MountDir])
                sleep(1) #diamo tempo affinché avvenga il montaggio

            # verifico che il comando di SUBST sia andato a buon fine...
            subst.FreeDir = LnVerifyPath(substDrive.joinpath('LnFree'), exitOnError=False)
            if subst.FreeDir:
                subst.Drive      = LnVerifyPath(substDrive)

                    # - setting and logging
                OsEnv.setVar('Ln_subst_Drive'     ,subst.Drive)
                OsEnv.setVar('Ln_subst_MountDir'  ,subst.MountDir)

            else:
                logger.warning("il comando di SUBST non ha avuto successo...")
                input()

                # ----------------------------------------
                # - se abbiamo attivato il SUBST,
                # - modifichiamo anche le MAIN variables
                # ----------------------------------------
            ln.Drive   = subst.Drive
            ln.RootDir = subst.Drive


        # ----------------------------------------
        # - verifica dell'esistenza delle myDirectories
        # ----------------------------------------
    for subdir in myDirectories:
        LnVerifyPath(ln.RootDir.joinpath(subdir))

        # - re-impostiamo le vriabili di ambientez
    OsEnv.setVar('Ln_Drive'     ,ln.Drive)
    OsEnv.setVar('Ln_RootDir'   ,ln.RootDir)



    if fDEBUG:
        if myArgs['subst']: subst.printTree(header="subst_variables", fPAUSE=False)
        ln.printTree(header="ln_variables", fPAUSE=True)

