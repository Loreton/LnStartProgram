# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-03-2018 09.46.24
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
    Ln      = Prj.LnLib
    gv      = Prj.gv
    C       = Ln.Color()
    # -----------------------------------------------

    args        = Prj.ParseInput(programVersion='v2018-03-05')  # ; print (args)
    gv.args     = Ln.Dict(args)     # covert to DotMap()

    gv.fDEBUG   = gv.args.debug
    if gv.fDEBUG: gv.args.printTree(fPAUSE=False)


        # -------------------------------
        # - Inizializzazione del logger
        # -------------------------------
    logger    = Ln.InitLogger(  name='MAIN',
                                logfilename=gv.args.log_filename,
                                toFILE=gv.args.log,
                                toCONSOLE=gv.args.log_console,
                                defaultLogLevel=gv.args.loglevel,
                                # rotationType='time', when="m", interval=60,
                                rotationType='size', maxBytes=500000,
                                backupCount=5,
                            )

    logger.info(gv.args, dictTitle='command line parameters...')


    extraSect   = Prj.prepareEnv()
    iniFile     = Ln.ReadIniFile(gv.args.ini_file, extraSections=extraSect, inline_comment_prefixes=(';'), strict=True)
    gv.cfgFile  = iniFile.toDict(dictType=Ln.Dict)
    if gv.fDEBUG: gv.cfgFile.printTree(header="INI File", fPAUSE=True)

    Ln.OsEnv.setVars(gv.cfgFile.VARS)
    Ln.OsEnv.setPaths(gv.cfgFile.PATHS)

    programToStart = gv.args.firstPosParameter

    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)

    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR)

    elif programToStart.lower().strip() in ['winscp_bdi']:
        CMDList = Prj.SetWinSCP(gv.cfgFile.WINSCP_BDI)

    elif programToStart.lower().strip() in ['winscp_loreto']:
        CMDList = Prj.SetWinSCP(gv.cfgFile.WINSCP_LORETO)

    else:
        Ln.Exit(1, "Program: {} not yet implemented".format(programToStart))

    if args['execute']:
        Ln.runProgram('{PRGNAME} command list:'.format(PRGNAME=programToStart), CMDList)
        msg = "Process completed, {} has been started".format(programToStart)
    else:
        print ()
        for item in CMDList:
            C.printColored(color=C.yellowH, text=item, tab=4)
        print ()
        msg = "enter --execute to launch the program: {}".format(programToStart)

    Ln.Exit(0, msg)



# E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\winscp.exe ssh-loreton.loreton /ini=E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\Ln_ini\WinSCP_Loreto.ini /log=D:/temp/winscp.log /sessionname=SSH-LORETON