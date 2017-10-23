#
#  updated by Loreto: 23-10-2017 15.35.08
#

import  Functions as Prj
import  LnLib as Ln
import  winreg


#@TODO: spostare le directory su un file di configurazione
#@TODO: preparare per Executor






if __name__ == '__main__':
    # gv        = myFunc.LnClass() # definita nell __init__.py
    # gv.env    = myFunc.LnClass()
    gv        = Ln.LnDict()
    gv.env    = Ln.LnDict()
    gv.Prj    = Prj
    gv.Ln     = Ln


    args      = gv.Prj.ParseInput() # ; print (args)
    gv.args   = Ln.LnDict(args)
    gv.fDEBUG = gv.args.debug
    logger    = gv.Prj.InitLogger(fFILE=gv.args.log_file, fCONSOLE=gv.args.log_console, ARGS=args)
    gv.logger = logger


    gv.Prj.CalculateMainDirs(gv, args)

    iniFile = gv.Ln.ReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile.setDebug(False)
    iniFile.read(resolveEnvVars=True)
    gv.cfgFile = gv.Ln.LnDict(iniFile.dict)
    if gv.fDEBUG: gv.cfgFile.printTree(fPAUSE=True)


    gv.Prj.SetEnvVars(gv, gv.cfgFile.VARS)
    gv.Prj.SetEnvPaths(gv, gv.cfgFile.PATHS)


        # =====================================================================
        # * Verifichiamo la versione del sistema operativo
        # * Set "RegQry=HKLM\Hardware\Description\System\CentralProcessor\0"
        # * "%SystemRoot%\system32\REG.exe"  Query %RegQry%
        # =====================================================================
    reg_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Hardware\Description\System\CentralProcessor\0',0, (winreg.KEY_WOW64_64KEY+ winreg.KEY_READ))
    gv.env.OSbits = winreg.EnumValue(reg_obj, 1)[1].split()[0]   # ('Identifier', 'Intel64 Family 6 Model 69 Stepping 1', 1)
    winreg.CloseKey(reg_obj)
    logger.info("Windows OS bits: {}".format(gv.env.OSbits))


    # prev_cwd = Path.cwd() # Save current directory
    if gv.args.program.lower().strip() in ['tc', 'totalcommander']:
        CMDList = gv.Prj.SetTotalCommander(gv, gv.cfgFile.TOTAL_COMMANDER)
        gv.Prj.LaunchProgram(gv, 'TotalCommander command list:', CMDList)

    elif gv.args.program.lower().strip() in ['executor']:
        CMDList = gv.Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR)
        gv.Prj.LaunchProgram(gv, 'Executor command list:', CMDList)

    else:
        gv.Ln.Exit(1, "Program: {} notyet implemented".format(gv.args.program))

    gv.Ln.Exit(0, "Process completed, {} has been started".format(gv.args.program))



