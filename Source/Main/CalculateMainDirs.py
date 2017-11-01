#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# __author__  : 'Loreto Notarantonio'
# __version__ : '26-10-2017 17.53.21'
#
# -----------------------------------------------

import  os, sys
from    pathlib import Path, PurePath         # dalla versione 3.4

# migliore implementazione di pathlib.Path
#    https://pathpy.readthedocs.io/en/latest/
from    LnLib.File.LnPath import Path as LnPath

from    time import sleep

from    LnLib.Common.LnLogger import SetLogger

from    LnLib.Common.Exit         import Exit        as LnExit
from    LnLib.Dict.LnDict_DotMap  import DotMap      as LnDict
import  LnLib.System.SetOsEnv                        as OsEnv
from    LnLib.File.VerifyPath     import VerifyPath  as LnVerifyPath
from    LnLib.System.RunProgram   import RunProgram  as LnRunProgram
from    LnLib.File.VerifyPath     import VerifyPath  as LnVerifyPath

from LnLib.File.DirList           import DirList as LnDirList



#########################################################################
# - Ln_Drive, Ln_rootDir e Ln_StartDir.
# -     in teoria sono già impostati ma serve in caso
# -     di subst perché li modifica opportunamente.
#########################################################################
def CalculateMainDirs(myArgs, fDEBUG=False):
    logger = SetLogger(__package__)

        # ---------------------------------------------------------------
        # - prepare dirs
        # - devo partire dalla directory del caller in quanto mi serve
        # - la root di partenza di LnDisk
        # ---------------------------------------------------------------

        # ---------------------------------------------------------------
        # - oppure posso cercare LnStart...
        # -  nel path di scriptMain
        # -  ricerca a partire dalla root per maxDepth=10
        # ---------------------------------------------------------------
    # scriptMain1         = Path(sys.argv[0]).resolve()
    scriptMain         = LnPath(sys.argv[0]).realpath()
    scriptMainParts    = LnPath(scriptMain).splitall()
    myPatternDir = 'LnDisk'
    myPatternDir = 'LnStart'

    drive, *rest = scriptMainParts

    if myPatternDir in rest:
        for dir in rest:
            rootDir = rootDir.joinpath(dir)
            if dir == myPatternDir: break

    else:
        # rootDir = scriptMain1.drive
        # dirs = Path('D:\\').rglob('*.py')
        # for dir in dirs:
        #     print (dir)
        dirs = LnDirList(drive, patternLIST=[myPatternDir], onlyDir=True, maxDeep=5)
        rootDir = dirs[0]
        # print (dirs)

    print (type(rootDir), rootDir)
    LnExit(9999)


    scriptMain         = LnPath(sys.argv[0]).realpath()
    # print (type(scriptMain), scriptMain)


    ln = LnDict()
    ln.RootDir    = LnVerifyPath(myArgs['rootDir'])
    ln.Drive      = LnVerifyPath(ln.RootDir.drive)

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


        # - re-impostiamo le vriabili di ambientez
    OsEnv.setVar('Ln_Drive'     ,ln.Drive)
    OsEnv.setVar('Ln_RootDir'   ,ln.RootDir)

    if fDEBUG:
        subst.printTree(header="subst_variables", fPAUSE=False)
        ln.printTree(header="ln_variables", fPAUSE=True)

