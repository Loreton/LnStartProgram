# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 20-01-2020 08.41.37
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
def ParseInput(program_names):
    import argparse
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='command line tool to start programs')
    parser.add_argument('--program', help='Specify progra to be started)', choices=program_names, required=True)
    parser.add_argument('--root-dir', help='LnDisk ROOT directory (ex: D:\\LnDisk)', required=False, default=None)
    # parser.add_argument('--python-version', help='Specify python version to be used', required=False,  choices=python_versions, default='default')

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
    # args.python_version='Python_' + args.python_version
    # print (args); sys.exit()
    return  args

def setMainPaths():
    global g_script_path, g_prj_name
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
    from zipfile import ZipFile
    import io
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
    zip_filename=setMainPaths()
    config_raw = readConfigFile(zip_filename)
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
    # python_versions = [k.lstrip('Python_') for k in config_raw.keys() if k.startswith('Python_')]


    # - Parse Input
    # inpArgs = ParseInput(program_names=programs, python_versions=python_versions)
    inpArgs = ParseInput(program_names=programs)
    if inpArgs.display_args:
        import json
        json_data = json.dumps(vars(inpArgs), indent=4, sort_keys=True)
        C.printColored(color=C.cyan, text='input arguments: {0}'.format(json_data), tab=8)
        sys.exit()


    ''' 
        Searching for ROOT path in the script path. It's identified by 'LnDisk' subdirectory
    '''
    # root_dir = Path(sys.argv[0]).resolve()
    root_dir = Path(g_script_path)
    while root_dir.name.lower() not in ['lndisk']:
        root_dir = root_dir.parent
        if root_dir.name == '':
            print('ROOT directory "LnDisk" NOT FOUND in path:', g_script_path)
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
    config = Ln.processYamlData(config_raw, prefix=r'${', suffix=r'}', errorOnNotFound=True, mylogger=lnLogger)
    # lnLogger.info('default configuration data', config_default)





        # -------------------------------------------------
        # - Choose right python version
        # -------------------------------------------------
    # if inpArgs.python_version not in 'Python_default':
    #     for k,v in config_raw[inpArgs.python_version].items():
    #         config_raw['VARS'][k] = v

    #     # - re-read configuration file
    #     config = Ln.processYamlData(config_raw, prefix=r'${', suffix=r'}', errorOnNotFound=True, mylogger=lnLogger)

    # else:
    #     config = config_default

    lnLogger.info('running configuration data', config)
        # -------------------------------------------------
        # - Setting environment variables
        # -------------------------------------------------
    for _name, _path in config['VARS'].items():
        if isinstance(_path, (list, tuple)):
            multiple_paths=[]
            for item in _path:
                item = Path.LnCheckPath(item, errorOnPathNotFound=False)
                if item:
                    multiple_paths.append(item)
            lnLogger.info('envar {0:<15}'.format(_name), multiple_paths)

            if _name == 'JAVA_HOME': 
                ''' get the first valid path and prepare it to be inserted into the PATH '''
                os.environ[_name] = multiple_paths[0]
                config['PATHS'].append(multiple_paths[0] + '/bin')
            else:
                os.environ[_name] = ';'.join(multiple_paths)

        else:
            _path = Path.LnCheckPath(_path, errorOnPathNotFound=False)
            lnLogger.info('envar {0:<15}'.format(_name), _path)
            os.environ[_name] = _path

        # -------------------------------------------------
        # - Setting path variables
        # -------------------------------------------------

    myPath = os.getenv('PATH').split(';')

    for _path in config['PATHS']:
        path = Path.LnCheckPath(_path, errorOnPathNotFound=False)
        lnLogger.info('adding PATH', _path)
        if _path in myPath:
            myPath.remove(_path) # delete if exists... per averli in ordine
        myPath.insert(0, _path)

        # - remove default python paths...
    python_home=config['VARS']['PYTHONHOME']
    path_len=len(python_home)
    # myPath = [_path for _path in myPath if not _path.startswith(current_python_dir)]
    myPath = [_path for _path in myPath if not _path[:path_len].lower() == python_home.lower()]

        # - add python home path
    myPath.insert(0, python_home)

        # - replace PATH environment variable
    myPath = [i for i in myPath if i.strip()]   # remove empty entries
    os.environ['PATH'] = ';'.join(myPath)
    lnLogger.info('new PATHs', os.getenv('PATH'))

        # -------------------------------------------------
        # - Setting pythonpath variable
        # -------------------------------------------------
    pyPath = os.getenv('PYTHONPATH').split(';')

    for _path in config['PYTHON_PATHS']:
        path = Path.LnCheckPath(_path, errorOnPathNotFound=False)
        lnLogger.info('adding PATH', _path)
        if _path in pyPath:
            myPath.remove(_path) # delete if exists... per averli in ordine
        pyPath.append(_path)
    pyPath = [i for i in pyPath if i.strip()]   # remove empty entries
    os.environ['PYTHONPATH'] = ';'.join(pyPath)
    lnLogger.info('new PYTHONPATHs', os.getenv('PYTHONPATH'))




    # print()
    # for index, item in enumerate(myPath):
    #     print("[{index:04}] {item}".format(**locals()))





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

