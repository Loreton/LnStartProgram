# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-06-2019 18.41.35
#
# #############################################

import  sys; sys.dont_write_bytecode = True
import  os
import  yaml
from    pathlib import Path
import  pdb
from    collections import OrderedDict
from    dotmap import DotMap


import myFunctions  as Ln


##############################################################
# - Parse Input
##############################################################
def ParseInput():
    import argparse
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='command line tool to start programs')
    parser.add_argument('--program', help='Specify progra to be started)', required=True)
    parser.add_argument('--subst', help='Specify the SUBST drive', required=False, default=None)
    parser.add_argument('--root-dir', help='LnDisk ROOT directory (ex: D:\\LnDisk)', required=False, default=None)
    parser.add_argument('--ini-file', help='ini configuration fileName', required=False, default='K:\\Filu\\LnDisk\\LnStart\\conf\\LnStart.ini')
    parser.add_argument('--edit-ini', help='Edit ini configuration file', action='store_true')

    parser.add_argument('--go', help='disable dry-run', action='store_true')
    parser.add_argument('--display-args', help='Display input paramenters', action='store_true')

        # log debug su file
    parser.add_argument('--log-modules',
                                metavar='',
                                required=False,
                                default=['*'],
                                nargs='*',
                                help="""attivazione log.
    E' anche possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono filtrare nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: --log-module pippo pluto ciao
    """)


    # args = vars(parser.parse_args())
    args = parser.parse_args()
    # print (args); sys.exit()
    return  args



######################################
# sample call:
#    python.exe __main__.py TotalCommander --config-file .\LnStartProgram.ini --subst=y:
#
######################################
if __name__ == '__main__':

    script_path          = Path(sys.argv[0]).resolve().parent
    if script_path.name  == 'bin': # potrei essere anche all'interno dello zip
        script_path = script_path.parent
    prj_name  = script_path.name

    os.environ['Ln_Drive'] = str(script_path.drive)
    os.environ['Ln_RootDir'] = str(script_path.parent)
    os.environ['Ln_ProgramDir'] = str(script_path)
    # all_env_Vars = os.environ
    # for key, val in os.environ.items():
    #     print ('{0:<25} = {1}'.format(key, val))

    stdout_file     = str(Path(script_path / 'log' / '{0}.stdout'.format(prj_name)))
    C               = Ln.Color(filename = stdout_file)
    printColored    = C.printColored
    gv              = DotMap(_dynamic   = False)
    gv.Ln           = Ln
    gv.Color        = C
    gv.printColored = C.printColored

    # - Parse Input
    inpArgs = ParseInput()
    inpArgs.script_path = str(script_path)
    if inpArgs.display_args:
        import json
        json_data = json.dumps(vars(inpArgs), indent=4, sort_keys=True)
        C.printColored(color=C.cyan, text='input arguments: {0}'.format(json_data), tab=8)
        sys.exit()



    # - logger
    log_file = str(Path(script_path  / 'log' / '{0}.log'.format(prj_name)))
    lnLogger = Ln.setLogger(filename=os.path.abspath(log_file), debug_level=3, dry_run=not inpArgs.go, log_modules=inpArgs.log_modules, color=Ln.Color() )
    lnStdout = Ln.setLogger(filename=os.path.abspath(stdout_file), color=Ln.Color() )
    # gv.logger = lnLogger
    # gv.LnLogger = lnLogger
    lnLogger.info('input arguments', vars(inpArgs))



    # - configuration file
    yaml_config_file = str(Path(script_path / 'conf' / '{0}.yml'.format(prj_name)))
    config = Ln.LoadYamFile(yaml_config_file, prefix=r'${', suffix=r'}', errorOnNotFound=False)
    lnLogger.info('configuration data', config)
    # config = DotMap(config, _dynamic=False) # pass to dotMap
    # lnLogger.info('configuration data', config.toDict())





    # lnLogger.console('temporary exit', config.toDict())
    # lnLogger.console('temporary exit'); sys.exit()



    # extraSect   = Prj.prepareEnv()
    # iniFile     = Ln.ReadIniFile(gv.args.ini_file, extraSections=extraSect, inline_comment_prefixes=(';'), strict=True)
    # gv.cfgFile  = iniFile.toDict(dictType=Ln.Dict)
    # if gv.fDEBUG: gv.cfgFile.printTree(header="INI File", fPAUSE=True)


        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for name, value in config['VARS'].items():
        lnLogger.info('envar {0:<15}: {1}'.format(name, value))
        os.environ[name] = str(value)

    for name, value in config['env_VARS'].items():
        lnLogger.info('envar {0:<15}: {1}'.format(name, value))
        os.environ[name] = str(value)

    myPath = os.getenv('PATH')
    for path in config['PATHS']:
        path = '{0};'.format(str(Path(path)))  # rimuove eventuali eccessi di \\\\\\
        # path = '{0};'.format(path)           # add ;
        myPath = myPath.replace(path, '')     # delete if exists
        # lnLogger.info('adding path:', ('PATH', path))
        # lnLogger.info('adding PATH: {0}'.format(path))
        lnLogger.info('adding PATH', path)
        myPath = '{0};{1}'.format(path, myPath)

        # paths = pathValue.split(sepChar)
        # for path in paths:
        #     path    = LnVerifyPath(path, exitOnError=fMANDATORY)

        # setVar(pathName, newPATH, fDEBUG=False)

    '''
    Ln.OsEnv.setVars(gv.cfgFile.OPT_VARS, mandatory=False)
    Ln.OsEnv.setPaths(gv.cfgFile.PATHS)

    programToStart = gv.args.firstPosParameter

    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(gv.cfgFile.TOTAL_COMMANDER, fDEBUG=gv.fDEBUG)

    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR)

    elif programToStart.lower().strip() in ['executor64']:
        CMDList = Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR64)

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
    '''



# E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\winscp.exe ssh-loreton.loreton /ini=E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\Ln_ini\WinSCP_Loreto.ini /log=D:/temp/winscp.log /sessionname=SSH-LORETON