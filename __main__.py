# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 17.34.36
#
# #############################################

import sys; sys.dont_write_bytecode = True


# -----------------------------------------
# - impostiamo qui le variabili globali
# - in modo che il resto dei moduli
# - abbiamo accesso diretto ad esse
# -----------------------------------------
import      Source as Prj

# -----------------------------------------
# - inseriamo la LnLib all'interno della Prj
# - in modo che ce la ritroviamo in tutti i moduli
# - facendo il solo import della Prj
# -----------------------------------------
Prj.LnLib = Prj.GVM.LibPath('LnLib.dir')
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


        # -----------------------------------------------
        # - imposta Ln_Drive, Ln_rootDir e Ln_StartDir.
        # -----------------------------------------------
    realDrive, realRootDir, substDrive = Prj.CalculateRootDir(gv, args) # set Ln_Drive, Ln_rootDir e Ln_StartDir
    realMountDir = realRootDir
    if substDrive: # override
        realDrive    = substDrive
        realRootDir  = substDrive



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

    Ln.runProgram('{PRGNAME} command list:'.format(PRGNAME=programToStart), CMDList)
    Ln.Exit(0, "Process completed, {} has been started".format(programToStart))
