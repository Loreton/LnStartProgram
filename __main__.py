# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 19-08-2019 16.02.44
#
# #############################################

import  sys; sys.dont_write_bytecode = True
import  os
import  yaml
from    pathlib import Path, WindowsPath
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
    parser.add_argument('--root-dir', help='LnDisk ROOT directory (ex: D:\\LnDisk)', required=False, default=None)

    parser.add_argument('--go', help='disable dry-run', action='store_true')
    parser.add_argument('--debug', help='display mai paths and input args', action='store_true')
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


def readConfigFile():
    global g_script_path, g_yaml_config_file, g_prj_name
    from zipfile import ZipFile
    import io
    # pdb.set_trace()
    _this_path          = Path(sys.argv[0]).resolve()
    # _this_path          = Path('K:/Filu/LnDisk/LnStart/LnStartProgram.zip').resolve()
    #_this_path = Path('K:\\Filu\\LnDisk\\LnStart\\LnStartProgram_New.zip').resolve()
    if _this_path.suffix == '.zip':
        _I_AM_ZIP = True
        g_prj_name    = _this_path.stem # first get name of zip file
        g_script_path = _this_path.parent # ... then up one level
        zip_filename = _this_path

    else:
        _I_AM_ZIP = False
        g_script_path = _this_path.parent
        g_prj_name  = g_script_path.name

    # yaml_filename = '{0}.yml'.format(g_prj_name)
    yaml_filenames = ['{0}.yml'.format(g_prj_name), 'conf/{0}.yml'.format(g_prj_name)]

    content = None
    if _I_AM_ZIP:
        z = ZipFile(zip_filename, "r")
        #zinfo = z.namelist()
        for name in yaml_filenames:
            if name in z.namelist():
                yaml_filename = name
                with z.open(yaml_filename) as f:
                    _data = f.read()
                _buffer = io.TextIOWrapper(io.BytesIO(_data))# def get_config(yaml_filename):
                # contents  = io.TextIOWrapper(io.BytesIO(_data), encoding='iso-8859-1', newline='\n')# def get_config(yaml_filename):
                content=[]
                for line in _buffer:
                    content.append(line)
                #result = yaml.safe_load(contents)
                break

    else:
        for name in yaml_filenames:
            yaml_filename = Path(g_script_path / name)
            if yaml_filename.exists():
                # yaml_filename = name
                with open(yaml_filename, 'r') as f:
                    content = f.readlines() # splitted in rows
                    # content = f.read() # single string
                break

    if content: # it's a LIST containing file rows...
        """ removal of all commented lines to avoid solving
        variables that could create errors"""
        rows = []
        for line in content:
            if not line.strip(): continue
            if line.strip()[0]=='#': continue
            rows.append(line)

        result = '\n'.join(rows)
        content = yaml.safe_load(result)

    else:
        print ('configuration file {0} NOT FOUND'.format(g_prj_name))
        sys.exit(1)
    g_yaml_config_file = yaml_filename
    return content # it's a dictionary


######################################
# sample call:
#    python.exe __main__.py TotalCommander --go
#
######################################
if __name__ == '__main__':
    config = readConfigFile()
    stdout_file = str(Path(g_script_path / 'log' / '{0}.stdout'.format(g_prj_name)))
    C = Ln.Color(filename=stdout_file)

    # - Parse Input
    inpArgs = ParseInput()
    if inpArgs.display_args:
        import json
        json_data = json.dumps(vars(inpArgs), indent=4, sort_keys=True)
        C.printColored(color=C.cyan, text='input arguments: {0}'.format(json_data), tab=8)
        sys.exit()


    # Searching for ROOT path identified by 'LnDisk' dirname
    root_dir = Path(sys.argv[0]).resolve()
    while root_dir.name.lower() not in ['lndisk']:
        root_dir = root_dir.parent
        if root_dir.name == '':
            print('ROOT directory "LnDisk" NOT FOUND in path:', _this_path)
            sys.exit(1)

    os.environ['Ln_RootDir'] = str(root_dir)
    os.environ['Ln_Drive'] = str(g_script_path.drive)
    os.environ['Ln_ScriptDir'] = str(g_script_path)




    if inpArgs.debug:
        for k,v in vars(inpArgs).items():
            print('     {0:<15}: {1}'.format(k, v))
        print()
        print('     {0:<15}: {1}'.format('g_prj_name', g_prj_name))
        print('     {0:<15}: {1}'.format('Ln_RootDir', str(root_dir)))
        print('     {0:<15}: {1}'.format('Ln_Drive', str(g_script_path.drive)))
        print('     {0:<15}: {1}'.format('Ln_ScriptDir', str(g_script_path)))
        print('     {0:<15}: {1}'.format('stdout', stdout_file))
        print('     {0:<15}: {1}'.format('config file', g_yaml_config_file))

        sys.exit()

    # - logger
    log_file = str(Path(g_script_path  / 'log' / '{0}.log'.format(g_prj_name)))
    lnLogger = Ln.setLogger(filename=os.path.abspath(log_file), debug_level=3, dry_run=not inpArgs.go, log_modules=inpArgs.log_modules, color=Ln.Color() )
    lnStdout = Ln.setLogger(filename=os.path.abspath(stdout_file), color=Ln.Color() )
    lnLogger.info('input arguments', vars(inpArgs))


    # - process configuration file
    config = Ln.processYamlData(config, prefix=r'${', suffix=r'}', errorOnNotFound=True, mylogger=lnLogger)
    lnLogger.info('configuration data', config)

# https://stackoverflow.com/questions/31392057/configparser-loading-config-files-from-zip
        # -------------------------------------------------
        # - Setting environment variables
        # -------------------------------------------------

    for _name, _path in config['VARS'].items():
        _path = Path.LnVerify(_path, errorOnPathNotFound=False)
        lnLogger.info('envar {0:<15}'.format(_name), _path)
        os.environ[_name] = _path

    myPath = os.getenv('PATH')+';'
    for _path in reversed(config['PATHS']):
        path = Path.LnVerify(_path, errorOnPathNotFound=False)
        lnLogger.info('adding PATH', _path)
        myPath = myPath.replace(_path+';', '')     # delete if exists
        myPath = '{0};{1}'.format(_path, myPath)

    os.environ['PATH'] = myPath
    lnLogger.info('new PATHs', os.getenv('PATH'))

    # sys.exit()
    # config = Ln.processYamlData(config, prefix=r'${', suffix=r'}', errorOnNotFound=False)
    # lnLogger.info('configuration data', config)

    programToStart = inpArgs.program

    if programToStart.lower().strip() in ['tc', 'totalcommander']:
        CMDList = Prj.SetTotalCommander(config['TOTAL_COMMANDER'], logger=lnLogger)
    elif programToStart.lower().strip() in ['executor']:
        CMDList = Prj.SetExecutor(config['EXECUTOR'], logger=lnLogger, fEXECUTE=inpArgs.go)
    elif programToStart.lower().strip() in ['vscode', 'vscode_insiders']:
        CMDList = Prj.SetVSCode(config['VSCODE_INSIDERS'], logger=lnLogger, fEXECUTE=inpArgs.go)
    else:
        print("Program: {} not yet implemented".format(programToStart))
        sys.exit(1)



    # - EXECUTION
    print ()
    C.printColored(color=C.magentaH, text="Working dir: {}".format(os.getcwd()), tab=4)
    print ()

    if inpArgs.go:
        Ln.runProgram('{0} command list:'.format(programToStart), CMDList, logger=lnLogger)
        msg = "Process completed, {0} has been started".format(CMDList[0])
    else:
        print ()
        for item in CMDList:
            C.printColored(color=C.yellowH, text=item, tab=4)
        print ()
        msg = "enter --go    to launch the program: {0}".format(programToStart)
        lnLogger.info("program {0} NOT started due to dry-run option.".format(CMDList[0]))

    C.printColored(color=C.greenH, text=msg, tab=4)
    sys.exit(0)

