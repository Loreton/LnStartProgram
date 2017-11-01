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
from LnLib.File.LnPath import Path

if __name__ == '__main__':
    gv        = LnDict()


    # myDirectory = Path('.')
    # myDirectory = Path('d:\Loreto\LnDisk\GIT-REPO\Python3')
    # myDirectory = Path('d:\\')

    # for f in myDirectory.iterdir():
    #     print(f)
    #     if f.is_dir() and f.name == 'LnStart':
    #         print('foune', f)
    #         break

    # pattern = 'LnStart'
    # for f in myDirectory.walkdirs(pattern):
    #     print(f)
        # if f.name == 'LnStart':
        #     print('foune', f)
        #     break







    # LnExit(9999, 'ciai')

    args      = Prj.ParseInput() # ; print (args)
    gv.args   = LnDict(args)
    gv.fDEBUG = gv.args.debug

    logger    = initLogger(toFILE=gv.args.log, logfilename=gv.args.log_filename, toCONSOLE=gv.args.log_console, ARGS=args)



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




