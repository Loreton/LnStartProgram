# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-01-2018 11.24.54
#
# #############################################

import sys; sys.dont_write_bytecode = True
# from pathlib import Path

# -----------------------------------------
# - impostiamo qui le variabili globali
# - in modo che il resto dei moduli
# - abbiamo accesso diretto ad esse
# -----------------------------------------
# thisDir  = Path(sys.argv[0]).resolve().parent
# sys.path.insert(0, str(thisDir))
import  Source as Prj


myLibName = ['LnPyLib', 'LnLib_2018-01-04xxx.zip']
LnLib     = Prj.SPE.LibPath(myLibName, fDEBUG=False)

# -------------------------------------------------------
# - inseriamo la LnLib e le gVars all'interno della Prj
# - in modo che ce la ritroviamo in tutti i moduli
# - facendo il solo import della Prj
# -------------------------------------------------------
Prj.LnLib = LnLib
Prj.gv    = Prj.LnLib.Dict()



######################################
# sample call:
#    python.exe __main__.py TotalCommander --config-file .\LnStartProgram.ini --subst=y:
#
######################################
if __name__ == '__main__':
    # ----- common part into the Prj modules --------
    Ln          = Prj.LnLib
    gv          = Prj.gv
    # -----------------------------------------------

    args        = Prj.ParseInput()  # ; print (args)
    gv.args     = Ln.Dict(args)     # covert to DotMap()

    gv.fDEBUG   = gv.args.debug
    if gv.fDEBUG: gv.args.printTree(fPAUSE=False)

    logger  = Ln.InitLogger(toFILE=gv.args.log, logfilename=gv.args.log_filename, toCONSOLE=gv.args.log_console, ARGS=args, defaultLogLevel='debug')


        # ------------------------------------------------------------------
        # leggiamo il file.ini solo per prelevare il SubstDrive
        # se viene passato da riga di comando prevale
        # altrimenti prendiamo quello definito nel file.ini (se esiste)
        # ------------------------------------------------------------------
    iniFile = Ln.ReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.read(resolveEnvVars=False)
    gv.cfgFile = Ln.Dict(iniFile.dict)

    if not args['subst']:
        if 'Subst_Drive' in gv.cfgFile.MAIN:
            args['subst'] = gv.cfgFile.MAIN.Subst_Drive





        # -----------------------------------------------
        # - imposta Ln_Drive, Ln_rootDir e Ln_StartDir.
        # -----------------------------------------------
    logger.info('Real Mount dir prima:')
    realDrive, realMountDir, substDrive = Prj.CalculateRootDir() # set Ln_Drive, Ln_rootDir e Ln_StartDir
    realRootDir = realMountDir

    # logger.info('realDrive   : {}'.format(realDrive))
    # logger.info('realRootDir : {}'.format(realRootDir))
    # logger.info('substDrive  : {}'.format(substDrive))

    # if substDrive: # override
        # realDrive    = substDrive
        # realRootDir  = substDrive

    # logger.info('realDrive   : {}'.format(realDrive))
    # logger.info('realRootDir : {}'.format(realRootDir))
    # logger.info('substDrive  : {}'.format(substDrive))

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
        test = Ln.Dict(extraSect)
        test.printDict(header='Extra Section', fPAUSE=True)

    iniFile = Ln.ReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.extraSections(extraSect)
    iniFile.read(resolveEnvVars=False)
    gv.cfgFile = Ln.Dict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(header="INI File", fPAUSE=True)

    Ln.OsEnv.setVars(gv.cfgFile.VARS)
    Ln.OsEnv.setPaths(gv.cfgFile.PATHS)

    programToStart = gv.args.firstPosParameter
    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)

    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR)

    else:
        Ln.Exit(1, "Program: {} not yet implemented".format(programToStart))

    if args['execute']:
        Ln.runProgram('{PRGNAME} command list:'.format(PRGNAME=programToStart), CMDList)
        msg = "Process completed, {} has been started".format(programToStart)
    else:
        msg = "enter --execute to launch the program: {}".format(programToStart)

    Ln.Exit(0, msg)
