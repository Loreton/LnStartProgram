#
# __author__  : 'Loreto Notarantonio'
# __version__ : '07-11-2017 14.10.09'
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
    realDrive, realRootDir, substDrive = Prj.CalculateRootDir(args, fDEBUG=gv.fDEBUG) # set Ln_Drive, Ln_rootDir e Ln_StartDir
    # my = Prj.CalculateRootDir(args, fDEBUG=gv.fDEBUG) # set Ln_Drive, Ln_rootDir e Ln_StartDir

    realMountDir = realRootDir
    if substDrive: # override
        realDrive    = substDrive
        realRootDir  = substDrive



    extraSect = {}
    extraSect['VARS']  = {}
    extraSect['VARS']['Ln_Drive']   = str(realDrive)
    extraSect['VARS']['Ln_RootDir'] = str(realRootDir)
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
        test = LnDict(extraSect)
        test.printDict(header='Extra Section', fPAUSE=True)

    iniFile = LnReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.extraSections(extraSect)
    iniFile.read(resolveEnvVars=False)
    gv.cfgFile = LnDict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(header="INI File", fPAUSE=True)


    OsEnv.setVars(gv.cfgFile.VARS)
    OsEnv.setPaths(gv.cfgFile.PATHS)

    programToStart = gv.args.programToStart
    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)

    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv.cfgFile.EXECUTOR)

    else:
        LnExit(1, "Program: {} not yet implemented".format(programToStart))

    runProgram('{PRGNAME} command list:'.format(PRGNAME=programToStart), CMDList)
    LnExit(0, "Process completed, {} has been started".format(programToStart))
