# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-06-2019 19.02.19
#
# #############################################

import  sys; sys.dont_write_bytecode = True
import  os
import  yaml
from    pathlib import Path
import  pdb
from    collections import OrderedDict
from    dotmap import DotMap


import Source.Utils  as Ln
import Source.Main  as Prj


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
    # parser.add_argument('--subst', help='Specify the SUBST drive', required=False, default=None)
    parser.add_argument('--root-dir', help='LnDisk ROOT directory (ex: D:\\LnDisk)', required=False, default=None)
    # parser.add_argument('--ini-file', help='ini configuration fileName', required=False, default='K:\\Filu\\LnDisk\\LnStart\\conf\\LnStart.ini')
    # parser.add_argument('--edit-ini', help='Edit ini configuration file', action='store_true')

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

    stdout_file     = str(Path(script_path / 'log' / '{0}.stdout'.format(prj_name)))
    C               = Ln.Color(filename = stdout_file)
    printColored    = C.printColored
    gv              = DotMap(_dynamic=False)

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
    lnLogger.info('input arguments', vars(inpArgs))


    # - read configuration file
    yaml_config_file = str(Path(script_path / 'conf' / '{0}.yml'.format(prj_name)))
    # config = Ln.LoadYmlFile(yaml_config_file, prefix=r'${', suffix=r'}', errorOnNotFound=False)
    config_str = Ln.LoadYamlFile_2(yaml_config_file)
    config = Ln.processYamlData(config_str, prefix=r'${', suffix=r'}', errorOnNotFound=False)
    lnLogger.info('configuration data', config)


        # -------------------------------------------------
        # - Setting environment variables
        # -------------------------------------------------
    for name, value in config['VARS'].items():
        lnLogger.info('envar {0:<15}: {1}'.format(name, value))
        os.environ[name] = str(value)

    for _name, _path in config['export_vars'].items():
        lnLogger.info('envar {0:<15}: {1}'.format(_name, _path))
        _path = Path(_path).resolve()
        os.environ[name] = str(_path)

    myPath = os.getenv('PATH')
    for path in config['PATHS']:
        path = Path(path).resolve()  # rimuove eventuali eccessi di \\\\\\
        lnLogger.info('adding PATH', path)
        myPath = myPath.replace(str(path), '').replace(';;', ';')     # delete if exists
        myPath = '{0};{1}'.format(str(path), myPath)


    config = Ln.processYamlData(config, prefix=r'${', suffix=r'}', errorOnNotFound=False)
    lnLogger.info('configuration data', config)

    programToStart = inpArgs.program

    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(config['TOTAL_COMMANDER'], logger=lnLogger)
    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(config['EXECUTOR'], logger=lnLogger)
    else:
        Ln.Exit(1, "Program: {} not yet implemented".format(programToStart))


    '''
    Ln.OsEnv.setVars(gv.cfgFile.OPT_VARS, mandatory=False)
    Ln.OsEnv.setPaths(gv.cfgFile.PATHS)



    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR)

    elif programToStart.lower().strip() in ['executor64']:
        CMDList = Prj.SetExecutor(gv, gv.cfgFile.EXECUTOR64)

    elif programToStart.lower().strip() in ['winscp_bdi']:
        CMDList = Prj.SetWinSCP(gv.cfgFile.WINSCP_BDI)

    elif programToStart.lower().strip() in ['winscp_loreto']:
        CMDList = Prj.SetWinSCP(gv.cfgFile.WINSCP_LORETO)

    '''

    if inpArgs.go:
        Ln.runProgram('{0} command list:'.format(programToStart), CMDList, logger=lnLogger)
        msg = "Process completed, {0} has been started".format(programToStart)
    else:
        print ()
        for item in CMDList:
            C.printColored(color=C.yellowH, text=item, tab=4)
        print ()
        msg = "enter --go    to launch the program: {0}".format(programToStart)

    C.printColored(color=C.greenH, text=msg, tab=4)
    sys.exit(0)



# E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\winscp.exe ssh-loreton.loreton /ini=E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\Ln_ini\WinSCP_Loreto.ini /log=D:/temp/winscp.log /sessionname=SSH-LORETON