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
    # print (hasattr(gv.args, 'root_dir'))
    # print ('root_dir' in gv.args)
    # print(gv.args['root_dir'])
    # if ('root_dir' in gv.args) and gv.args['root_dir']:
    try:
        rootDir = Path(gv.args['root_dir']).resolve()
        drive, *rest = rootDir.parts
        logger.info("drive:   {}".format(drive))
        logger.info("rootDir: {}".format(rootDir))

        # - altrimenti la calcoliamo
    except:
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
    # if gv.args['subst']:
    try:
        mountDir = createSUBSTDrive(substDrive=Path(gv.args['subst']), substMountDir=realRootDir)
        logger.info("subst required:  {}".format(gv.args['subst']))
    except:
        mountDir = None



        # ----------------------------------------
        # - verifica dell'esistenza delle myDirectories
        # ----------------------------------------
    myRootDir = mountDir if mountDir else realRootDir
    if str(myRootDir)[-1] == ':': myRootDir = myRootDir / '/'
    logger.info("myRootDir:  {}".format(myRootDir))
    for subdir in myDirectories:
        Ln.VerifyPath(myRootDir.joinpath(subdir))

    Ln.SetLogger(__name__, exiting=True) # log the caller
    # Ln.Exit(9999, 'debugging exit to test logger')
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
    if not str(substDrive).lower() in validDrives:
        errMsg = """il drive immesso [{DRIVE}] non è valido...
    immettere uno delle seguenti: {DRIVES}
        """.format(DRIVE=substDrive, DRIVES=validDrives)
        logger.warning(errMsg)
        Ln.Exit(22, errMsg)


    if substDrive.exists():
        logger.info('SUBST drive {} alredy present'.format(substDrive))

    else:
        # if gv.args['execute']:
        Ln.runProgram("executing SUBST command:", ['subst', substDrive, substMountDir])
        sleep(1) #diamo tempo affinché avvenga il montaggio

            # verifico che il comando di SUBST sia andato a buon fine...
        substDrive = Ln.VerifyPath(substDrive, exitOnError=False) # ritorna mountDir


    logger.info("SUBST drive: {0}".format(substDrive))
    Ln.SetLogger(__name__, exiting=True) # log the caller
    return substDrive



################################################
# Preparazione dell'ambiente in caso di
# totalCommander o Executor
################################################
def prepareEnv():
    Ln     = Prj.LnLib
    logger = Ln.SetLogger(__name__)
    gv     = Prj.gv

        # ------------------------------------------------------------------
        # leggiamo il file.ini solo per prelevare il SubstDrive
        # se viene passato da riga di comando prevale
        # altrimenti prendiamo quello definito nel file.ini (se esiste)
        # ------------------------------------------------------------------
    iniFile     = Ln.ReadIniFile(gv.args.config_file, strict=True)
    gv.cfgFile  = iniFile.toDict(dictType=Ln.Dict)

    if 'subst' in gv.args:
    # if not gv.args['subst']:
        if 'Subst_Drive' in gv.cfgFile.MAIN:
            gv.args['subst'] = gv.cfgFile.MAIN.Subst_Drive





        # -----------------------------------------------
        # - imposta Ln_Drive, Ln_rootDir e Ln_StartDir.
        # -----------------------------------------------
    logger.info('Real Mount dir prima:')
    realDrive, realMountDir, substDrive = CalculateRootDir() # set Ln_Drive, Ln_rootDir e Ln_StartDir
    realRootDir = realMountDir


    logger.info('Real Mount dir: {}'.format(realMountDir))
    logger.info('substDrive    : {}'.format(substDrive))
    logger.info('realDrive     : {}'.format(realDrive))


        # -----------------------------------------------
        # - prima di leggere il file INI impostiamo
        # - alcune dati utili per la risoluzione
        # - delle variabili rial-time
        # -----------------------------------------------
    extraSect                              = {}
    extraSect['VARS']                      = {}
    extraSect['VARS']['Ln_Drive']          = str(realDrive)
    extraSect['VARS']['Ln_RootDir']        = str(realRootDir)
    extraSect['VARS']['Ln_subst_MountDir'] = str(realMountDir)

    programDIR = Path(sys.argv[0]).resolve().parent
    extraSect['VARS']['Ln_ProgramDIR'] = str(programDIR)

    if substDrive:
        '''
            set the SUBST drive
        '''
        extraSect['VARS']['Ln_subst_Drive']    = str(substDrive)
        extraSect['VARS']['Ln_subst_RootDir']  = str(substDrive)
    else:
        '''
            set the SUBST dirs to realRootDir
        '''
        extraSect['VARS']['Ln_subst_Drive']    = str(realDrive)
        extraSect['VARS']['Ln_subst_RootDir']  = str(realRootDir)

    if gv.fDEBUG:
        print (type(extraSect), extraSect)

        test = Ln.Dict(extraSect)
        test.printDict(header='Extra Section', fPAUSE=True)


    return extraSect