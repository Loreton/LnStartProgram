#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# __author__  : 'Loreto Notarantonio'
# __version__ : '06-11-2017 18.23.29'
#
# -----------------------------------------------

import  os, sys
from    pathlib                  import Path, PurePath         # dalla versione 3.4
# from    LnLib.File.LnPath        import Path as LnPath

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
def CalculateRootDir(myArgs, fDEBUG=False):
    logger = SetLogger(__package__)

        # ---------------------------------------------------------------
        # - prepare dirs
        # - mi server la rootDir di partenza di LnDisk
        # - cerco la subDir LnStart o LnFree nel path di scriptMain
        # ---------------------------------------------------------------
    myDirectories = ('LnStart', 'LnFree', 'GIT-REPO')

        # - se la root dir viene passata prendiamola per ciò che è
    if myArgs['root_dir']:
        rootDir = Path(myArgs['root_dir']).resolve()
        drive, *rest = rootDir.parts
        logger.info("drive:   {}".format(drive))
        logger.info("rootDir: {}".format(rootDir))

        # - altrimenti la calcoliamo
    else:
        FOUND = False
        scriptMain   = Path(sys.argv[0]).resolve()
        drive, *rest = scriptMain.parts
        rootDir      = Path(drive).resolve()
        for dirname in rest:
            if dirname in myDirectories:
                FOUND = True
                break
            else:
                rootDir = rootDir.joinpath(dirname)

        if not FOUND:
            logger.error("root_dir NOT found.")
            LnExit(21, "root_dir NOT found.")


    # ln = LnDict()

        # - rootdir di base
    realDrive      = LnVerifyPath(drive)
    realRootDir    = LnVerifyPath(rootDir)

    logger.info("realDrive:    {}".format(realDrive))
    logger.info("realRootDir:  {}".format(realRootDir))

        # --------------------------------------------
        # - se e' richiesto un drive SUBST...
        # - impostiamo tutti i path per quel drive
        # --------------------------------------------
    if myArgs['subst']:
        substDrive = createSUBSTDrive(substDrive=Path(myArgs['subst']), substMountDir=realRootDir)
    else:
        substDrive = None


        # ----------------------------------------
        # - verifica dell'esistenza delle myDirectories
        # ----------------------------------------
    testRootDir = substDrive if substDrive else realRootDir
    logger.info("testRootDir:  {}".format(testRootDir))
    errore con questi parametri: executor --log-co
    for subdir in myDirectories:
        # LnVerifyPath(testRootDir.joinpath(subdir))
        LnVerifyPath(testRootDir.absolute() / '/' / subdir)

    return realDrive, realRootDir, substDrive



# ######################################################
# - attiva il Sust
# ######################################################
def createSUBSTDrive(substDrive, substMountDir):
    logger = SetLogger(__package__)

    logger.info("parameter substDrive:    {}".format(substDrive))
    logger.info("parameter substMountDir: {}".format(substMountDir))

    # retVal = None

    if not str(substDrive).lower() in ['x:', 'y:', 'w:', 'z:']:
        errMsg = "il drive immesso [{DRIVE}] non è previsto...".format(DRIVE=substDrive)
        logger.warning(errMsg)
        LnExit(22, errMsg)


    if substDrive.exists():
        logger.info('SUBST drive {} alredy present'.format(substDrive))

    else:
        LnRunProgram("executing SUBST command:", ['subst', substDrive, substMountDir])
        sleep(1) #diamo tempo affinché avvenga il montaggio

            # verifico che il comando di SUBST sia andato a buon fine...
        substDrive = LnVerifyPath(substDrive, exitOnError=False) # ritorna substDrive


    logger.info("SUBST drive: {0}".format(substDrive))

    return substDrive