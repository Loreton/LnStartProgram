#
#  updated by Loreto: 24-10-2017 14.24.09
#

# import  Source as Prj
import  platform

import  winreg
import logging

# from LnLib.LnCommon.LnLogger      import SetLogger
from LnLib.Common.LnLogger        import InitLogger
from LnLib.Common.Exit            import Exit        as LnExit
from LnLib.Dict.LnDict_DotMap     import DotMap      as LnDict
from LnLib.File.ReadIniFile_Class import ReadIniFile as LnReadIniFile
from LnLib.System.SetOsEnv        import SetEnvVars  as LnSetEnvVars
from LnLib.System.SetOsEnv        import SetEnvPaths as LnSetEnvPaths
from LnLib.System.RunProgram      import RunProgram  as LnRunProgram

from Source.CalculateMainDirs      import CalculateMainDirs as prjCalculateMainDirs
from Source.SetTotalCommander      import SetTotalCommander as prjSetTotalCommander
from Source.SetExecutor             import SetExecutor      as prjSetExecutor
from Source.ParseInput             import ParseInput      as prjParseInput


if __name__ == '__main__':
    gv        = LnDict()


    args      = prjParseInput() # ; print (args)
    gv.args   = LnDict(args)
    gv.fDEBUG = gv.args.debug
    logger    = InitLogger(toFILE=gv.args.log_file, toCONSOLE=gv.args.log_console, ARGS=args)



        # -----------------------------------------------
        # imposta Ln_Drive, Ln_rootDir e Ln_StartDir.
        # in teoria sono già impostati ma serve in caso
        # di subst perché li modifica opportunamente.
        # -----------------------------------------------
    prjCalculateMainDirs(args, fDEBUG=gv.fDEBUG) # set Ln_Drive, Ln_rootDir e Ln_StartDir

    iniFile = LnReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.read(resolveEnvVars=True)
    gv.cfgFile = LnDict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(fPAUSE=True)


    LnSetEnvVars(gv.cfgFile.VARS)
    LnSetEnvPaths(gv.cfgFile.PATHS)


    if gv.args.program.lower().strip() in ['tc', 'totalcommander']:
        CMDList = prjSetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)
        LnRunProgram('TotalCommander command list:', CMDList)

    elif gv.args.program.lower().strip() in ['executor']:
        CMDList = prjSetExecutor(gv.cfgFile.EXECUTOR)
        LnRunProgram('Executor command list:', CMDList)

    else:
        LnExit(1, "Program: {} not yet implemented".format(gv.args.program))

    LnExit(0, "Process completed, {} has been started".format(gv.args.program))




