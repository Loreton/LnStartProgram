#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# __author__  : 'Loreto Notarantonio'
# __version__ : '07-11-2017 12.53.32'
#
# -----------------------------------------------

import  sys
from    pathlib                  import Path         # dalla versione 3.4
from    time                     import sleep

import   Source as Prj

#########################################################################
# - Ln_Drive, Ln_rootDir e Ln_StartDir e GIT-REPO.
#########################################################################
def CalculateRootDir():
    '''
    calculate root directory for LnDisk
        args:
        gv    : DotMap() formmat of global Vars
        gv.args: command line input arguments
    '''

    # ----- common part into the Prj modules --------
    global Ln, gv
    Ln     = Prj.LnLib
    logger = Ln.SetLogger(__name__)
    gv      = Prj.gv
    # -----------------------------------------------


        # ---------------------------------------------------------------
        # - prepare dirs
        # - mi server la rootDir di partenza di LnDisk
        # - cerco la subDir LnStart o LnFree nel path di scriptMain
        # ---------------------------------------------------------------
    myDirectories = ('LnStart', 'LnFree', 'GIT-REPO')

        # - se la root dir viene passata prendiamola per ciò che è
    if gv.args['root_dir']:
        rootDir = Path(gv.args['root_dir']).resolve()
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
            Ln.Exit(21, "root_dir NOT found.")


        # - rootdir di base
    realDrive      = Ln.VerifyPath(drive)
    realRootDir    = Ln.VerifyPath(rootDir)

    logger.info("realDrive:    {}".format(realDrive))
    logger.info("realRootDir:  {}".format(realRootDir))
        # --------------------------------------------
        # - se e' richiesto un drive SUBST...
        # - impostiamo tutti i path per quel drive
        # --------------------------------------------
    print (gv.args['subst'])
    if gv.args['subst']:
        mountDir = createSUBSTDrive(substDrive=Path(gv.args['subst']), substMountDir=realRootDir)
    else:
        mountDir = None



        # ----------------------------------------
        # - verifica dell'esistenza delle myDirectories
        # ----------------------------------------
    myRootDir = mountDir if mountDir else realRootDir
    if str(myRootDir)[-1] == ':': myRootDir = myRootDir / '/'
    logger.info("myRootDir:  {}".format(myRootDir))
    for subdir in myDirectories:
        Ln.VerifyPath(myRootDir.joinpath(subdir))

    Ln.SetLogger(__name__, reset=True) # log the caller
    Ln.Exit(9999, 'debugging exit')
    return realDrive, realRootDir, mountDir



# ######################################################
# - attiva il Sust
# ######################################################
def createSUBSTDrive(substDrive, substMountDir):
    '''
    execute SUBST windows command to create a virtualDrive pointing to a path
    '''

    logger = Ln.SetLogger(__name__)

    logger.info("parameter substDrive:    {}".format(substDrive))
    logger.info("parameter substMountDir: {}".format(substMountDir))

    validDrives = ('j:','k:','l:','m:','n:','o:','p:','q:','r:','s:','t:','u:','v:','w:','x:','y:','z:')
    # if not str(substDrive).lower() in ['x:', 'y:', 'w:', 'z:']:
    if not str(substDrive).lower() in validDrives:
        errMsg = """il drive immesso [{DRIVE}] non è valido...
    immettere uno delle seguenti: {DRIVES}
        """.format(DRIVE=substDrive, DRIVES=validDrives)
        logger.warning(errMsg)
        Ln.Exit(22, errMsg)


    if substDrive.exists():
        logger.info('SUBST drive {} alredy present'.format(substDrive))
        # mountDir = substDrive

    else:
        # if gv.args['execute']:
        Ln.runProgram("executing SUBST command:", ['subst', substDrive, substMountDir])
        sleep(1) #diamo tempo affinché avvenga il montaggio

            # verifico che il comando di SUBST sia andato a buon fine...
        # print ('1.{}.'.format(substDrive))
        # Ln.VerifyPath(substDrive, exitOnError=True) # ritorna substDrive
        substDrive = Ln.VerifyPath(substDrive, exitOnError=False) # ritorna substDrive
        # print ('2.{}.'.format(substDrive))


    logger.info("SUBST drive: {0}".format(substDrive))
    Ln.SetLogger(__name__, reset=True) # log the caller
    return substDrive