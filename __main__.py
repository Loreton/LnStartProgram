#
# __author__  : 'Loreto Notarantonio'
# __version__ : '27-10-2017 11.38.58'
#


# import LnLib.System.SetOsEnv      as  SetEnv
from  LnLib.System import SetOsEnv      as  OsEnv

from LnLib.Common.LnLogger import init as initLogger

# from LnLib.Common.LnLogger        import InitLogger

from LnLib.Common.Exit            import Exit        as LnExit
from LnLib.Dict.LnDict_DotMap     import DotMap      as LnDict
from LnLib.File.ReadIniFile_Class import ReadIniFile as LnReadIniFile

from LnLib.System.RunProgram      import RunProgram  as runProgram

import  Source as Prj


# from pathlib import Path
# from LnLib.File.LnPath import Path

if __name__ == '__main__':
    gv        = LnDict()

    args      = Prj.ParseInput() # ; print (args)
    gv.args   = LnDict(args)
    gv.fDEBUG = gv.args.debug
    if gv.fDEBUG: gv.args.printTree(fPAUSE=True)

    logger    = initLogger(toFILE=gv.args.log, logfilename=gv.args.log_filename, toCONSOLE=gv.args.log_console, ARGS=args)



        # -----------------------------------------------
        # imposta Ln_Drive, Ln_rootDir e Ln_StartDir.
        # in teoria sono già impostati ma serve in caso
        # di subst perché li modifica opportunamente.
        # -----------------------------------------------
    myDrive, myRootDir = Prj.CalculateRootDir(args, fDEBUG=gv.fDEBUG) # set Ln_Drive, Ln_rootDir e Ln_StartDir


    extraSect = {}
    extraSect['VARS']  = {}
    extraSect['VARS']['Ln_RootDir'] = myRootDir
    extraSect['VARS']['Ln_Drive']   = myDrive


    iniFile = LnReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.extraSections(extraSect)
    iniFile.read(resolveEnvVars=False)
    gv.cfgFile = LnDict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(fPAUSE=True)


    OsEnv.setVars(gv.cfgFile.VARS)
    OsEnv.setPaths(gv.cfgFile.PATHS)

    programToStart = gv.args.programToStart
    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)
        runProgram('TotalCommander command list:', CMDList)

    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv.cfgFile.EXECUTOR)
        runProgram('Executor command list:', CMDList)

    else:
        LnExit(1, "Program: {} not yet implemented".format(programToStart))

    LnExit(0, "Process completed, {} has been started".format(programToStart))




