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
        # imposta Ln.Drive, Ln.rootDir e Ln.StartDir.
        # in teoria sono già impostati ma serve in caso
        # di subst perché li modifica opportunamente.
        # -----------------------------------------------

    prjCalculateMainDirs(args, fDEBUG=gv.fDEBUG)

    iniFile = LnReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.read(resolveEnvVars=True)
    gv.cfgFile = LnDict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(fPAUSE=True)


    LnSetEnvVars(gv.cfgFile.VARS)
    LnSetEnvPaths(gv.cfgFile.PATHS)


        # =====================================================================
        # * Verifichiamo la versione del sistema operativo
        # * Set "RegQry=HKLM\Hardware\Description\System\CentralProcessor\0"
        # * "%SystemRoot%\system32\REG.exe"  Query %RegQry%
        # =====================================================================
    # reg_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Hardware\Description\System\CentralProcessor\0',0, (winreg.KEY_WOW64_64KEY+ winreg.KEY_READ))
    # gv.env.OSbits = winreg.EnumValue(reg_obj, 1)[1].split()[0]   # ('Identifier', 'Intel64 Family 6 Model 69 Stepping 1', 1)
    # winreg.CloseKey(reg_obj)

    # OSbits = platform.architecture()[0]
    # logger.info("Windows OS bits: {}".format(OSbits))

    # prev_cwd = Path.cwd() # Save current directory
    if gv.args.program.lower().strip() in ['tc', 'totalcommander']:
        CMDList = prjSetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)
        LnRunProgram('TotalCommander command list:', CMDList)

    elif gv.args.program.lower().strip() in ['executor']:
        CMDList = prjSetExecutor(gv.cfgFile.EXECUTOR)
        LnRunProgram('Executor command list:', CMDList)

    else:
        LnExit(1, "Program: {} not yet implemented".format(gv.args.program))

    LnExit(0, "Process completed, {} has been started".format(gv.args.program))




