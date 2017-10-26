#
#  updated by Loreto: 24-10-2017 14.24.09
#


# import LnLib.System.SetOsEnv      as  SetEnv
from  LnLib.System import SetOsEnv      as  OsEnv

from LnLib.Common.LnLogger import init as initLogger

# from LnLib.Common.LnLogger        import InitLogger

from LnLib.Common.Exit            import Exit        as LnExit
from LnLib.Dict.LnDict_DotMap     import DotMap      as LnDict
from LnLib.File.ReadIniFile_Class import ReadIniFile as LnReadIniFile
# from LnLib.System.SetOsEnv        import SetEnvVars  as LnSetEnvVars
# from LnLib.System.SetOsEnv        import SetEnvPaths as LnSetEnvPaths

from LnLib.System.RunProgram      import RunProgram  as runProgram

import  Source as Prj
# ... oppure
# from Source.CalculateMainDirs      import CalculateMainDirs as CalculateMainDirs
# from Source.SetTotalCommander      import SetTotalCommander as SetTotalCommander
# from Source.SetExecutor            import SetExecutor       as SetExecutor
# from Source.ParseInput             import ParseInput        as ParseInput



if __name__ == '__main__':
    gv        = LnDict()
    for module in dir():
        if not module.startswith('__'):
            print ('    ', module)


    args      = Prj.ParseInput() # ; print (args)
    gv.args   = LnDict(args)
    gv.fDEBUG = gv.args.debug
    logger    = initLogger(toFILE=gv.args.log_filename, toCONSOLE=gv.args.log_console, ARGS=args)



        # -----------------------------------------------
        # imposta Ln_Drive, Ln_rootDir e Ln_StartDir.
        # in teoria sono già impostati ma serve in caso
        # di subst perché li modifica opportunamente.
        # -----------------------------------------------
    Prj.CalculateMainDirs(args, fDEBUG=gv.fDEBUG) # set Ln_Drive, Ln_rootDir e Ln_StartDir

    iniFile = LnReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.read(resolveEnvVars=True)
    gv.cfgFile = LnDict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(fPAUSE=True)


    OsEnv.setVars(gv.cfgFile.VARS)
    OsEnv.setPaths(gv.cfgFile.PATHS)


    if gv.args.program.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)
        runProgram('TotalCommander command list:', CMDList)

    elif gv.args.program.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv.cfgFile.EXECUTOR)
        runProgram('Executor command list:', CMDList)

    else:
        LnExit(1, "Program: {} not yet implemented".format(gv.args.program))

    LnExit(0, "Process completed, {} has been started".format(gv.args.program))




