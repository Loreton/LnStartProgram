# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-11-2019 18.34.49
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
def ParseInput(program_names, python_versions):
    import argparse
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='command line tool to start programs')
    parser.add_argument('--program', help='Specify progra to be started)', choices=program_names, required=True)
    parser.add_argument('--root-dir', help='LnDisk ROOT directory (ex: D:\\LnDisk)', required=False, default=None)
    parser.add_argument('--python-version', help='Specify python version to be used', required=False,  choices=python_versions, default='default')

    parser.add_argument('--go', help='disable dry-run', action='store_true')
    parser.add_argument('--debug', help='display main paths and input args', action='store_true')
    parser.add_argument('--display-args', help='Display input paramesters', action='store_true')

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
    args.python_version='Python_' + args.python_version
    # print (args); sys.exit()
    return  args

def setMainPaths():
    global g_script_path, g_prj_name
    from zipfile import ZipFile
    import io
    # pdb.set_trace()
    _this_path          = Path(sys.argv[0]).resolve()
    # _this_path          = Path('K:/Filu/LnDisk/LnStart/LnStartProgram.zip').resolve()
    #_this_path = Path('K:\\Filu\\LnDisk\\LnStart\\LnStartProgram_New.zip').resolve()
    if _this_path.suffix == '.zip':
        # _I_AM_ZIP = True
        g_prj_name    = _this_path.stem # first get name of zip file
        g_script_path = _this_path.parent # ... then up one level
        zip_filename = _this_path

    else:
        # _I_AM_ZIP = False
        g_script_path = _this_path.parent
        g_prj_name  = g_script_path.name
        zip_filename = None

    return zip_filename

def readConfigFile(zip_filename=None):
    global g_yaml_config_file
    # yaml_filename = '{0}.yml'.format(g_prj_name)
    yaml_filenames = ['{0}.yml'.format(g_prj_name), 'conf/{0}.yml'.format(g_prj_name)]

    content = None
    if zip_filename:
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

    if content: # LIST containing file rows...
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
    return content # dictionary data


######################################
# sample call:
#    python.exe __main__.py --program TotalCommander --python python_3741 --go
#
######################################
if __name__ == '__main__':
    i_am_zip=setMainPaths()
    config_raw = readConfigFile(i_am_zip)
    stdout_file = str(Path(g_script_path / 'log' / '{0}.stdout'.format(g_prj_name)))
    C = Ln.Color(filename=stdout_file)


    # -------
    # mapping program_name with python function module
    # -------
    module_map = {
        "totalcommander" : {
            'module': Prj.SetTotalCommander,
            'config': 'TOTAL_COMMANDER',
        },
        "tc" : {
            'module': Prj.SetTotalCommander,
            'config': 'TOTAL_COMMANDER',
        },
        "executor" : {
            'module': Prj.SetExecutor,
            'config': 'EXECUTOR',
        },
    }
    programs = [k for k in module_map.keys()]
    python_versions = [k.lstrip('Python_') for k in config_raw.keys() if k.startswith('Python_')]


    # - Parse Input
    inpArgs = ParseInput(program_names=programs, python_versions=python_versions)
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
    config_default = Ln.processYamlData(config_raw, prefix=r'${', suffix=r'}', errorOnNotFound=True, mylogger=lnLogger)
    lnLogger.info('default configuration data', config_default)



    myPath = os.getenv('PATH').split(';')

        # - remove default python paths...
    default_python_dir=config_default['Python_default']['Ln_pythonDir']
    myPath = [_path for _path in myPath if not _path.startswith(default_python_dir)]


        # -------------------------------------------------
        # - Choose right python version
        # -------------------------------------------------
    if inpArgs.python_version not in 'Python_default':
        for k,v in config_raw[inpArgs.python_version].items():
            config_raw['VARS'][k] = v

        # - re-read configuration file
        config = Ln.processYamlData(config_raw, prefix=r'${', suffix=r'}', errorOnNotFound=True, mylogger=lnLogger)

    else:
        config = config_default

    lnLogger.info('running configuration data', config)

        # -------------------------------------------------
        # - Setting environment variables
        # -------------------------------------------------
    for _name, _path in config['VARS'].items():
        _path = Path.LnCheck(_path, errorOnPathNotFound=False)
        lnLogger.info('envar {0:<15}'.format(_name), _path)
        os.environ[_name] = _path

        # -------------------------------------------------
        # - Setting path variables
        # -------------------------------------------------
    for _path in config['PATHS'] + config['PYTHON_PATHS']:
        path = Path.LnCheck(_path, errorOnPathNotFound=False)
        lnLogger.info('adding PATH', _path)
        if _path in myPath:
            myPath.remove(_path) # delete if exists... per averi in ordine
        myPath.insert(0, _path)


    myPath = [i for i in myPath if i.strip()]   # remove empty entries
    # print()
    # for index, item in enumerate(myPath):
    #     print("[{index:04}] {item}".format(**locals()))
    os.environ['PATH'] = ';'.join(myPath)
    # sys.exit(1)
    lnLogger.info('new PATHs', os.getenv('PATH'))





    programToStart = inpArgs.program
    moduleToCall = module_map[programToStart]['module']
    # moduleConfig = module_map[programToStart]['config']
    module_config_data = config[module_map[programToStart]['config']]
    CMDList = moduleToCall(module_config_data, logger=lnLogger)



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

