#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.51.47
# -----------------------------------------------
from    sys     import argv as sysArgv, exit as sysExit
from    pathlib import Path
from    time import  strftime
import  argparse



# import  Functions as Prj


def ParseInput():
    # =============================================
    # = Parsing
    # =============================================
    if len(sysArgv) == 1: sysArgv.append('-h')

    programDir     = Path(sysArgv[0]).resolve().parent
    if programDir.name.lower() in ['bin',  'source']:
        programDir = programDir.parent

    prjName        = programDir.name   # nome della dir del programma

        # ---- DEFAULT VALUEs
    defaultLogDir     = programDir
    # print (programDir)
    # sysExit()
    defaultLogFile    = Path(defaultLogDir , 'log', prjName + strftime('_%Y-%m-%d') + '.log')
    defaultConfigFile = Path(programDir , 'conf', prjName + '.ini')
    defaultRootDir    = Path(sysArgv[0]).resolve().parent


    mainHelp=""
    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description='Partenza di programmi',
        usage='',                                          # non voglio lo usage
        epilog=mainHelp,
        conflict_handler='resolve',
    )

    myParser.add_argument('--program',
                                required=False,
                                default='TotalCommander',
                                metavar='program',
                                help=myHELP('Specify the program to start', 'TotalCommander'))

    myParser.add_argument('--subst',
                                required=False,
                                default=None,
                                metavar='subst',
                                help=myHELP('Specify the SUBST drive', None))

    myParser.add_argument('--config-file',
                                metavar='',
                                type=_fileCheck,
                                required=False,
                                default=defaultConfigFile,
                                help=myHELP('Specifies config fileName...', defaultConfigFile))

    myParser.add_argument('--go',
                                required=False,
                                action='store_true',
                                help=myHELP('Specifies if program must be started', False))

    myParser.add_argument('--debug',
                                required=False,
                                action='store_true',
                                help=myHELP('Specifies if program must be started', False))

    myParser.add_argument('--parameters',
                                required=False,
                                action='store_true',
                                help=myHELP('Display input paramenters..', False))

    myParser.add_argument('--log',
                                required=False,
                                action='store_true',
                                help=myHELP('Enable log on file... ', False))

        # log debug su console
    myParser.add_argument( "--log-console",
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=myHELP("""attivazione log sulla console.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo uto ciao""", False))


    myParser.add_argument('--log-filename',
                                metavar='',
                                required=False,
                                default=defaultLogFile,
                                help=myHELP('Specifies log fileName...', defaultLogFile))

    myParser.add_argument('--rootDir',
                                metavar='',
                                type=_fileCheck,
                                required=False,
                                default=defaultRootDir,
                                  help=myHELP('Specifies caller directory', defaultRootDir))

    args = vars(myParser.parse_args())


        # --------------------------------------------
        # - verifica del LOG
        # - if not [log] azzera anche il [log_file]
        # --------------------------------------------
    if not args['log']:
        args['log_file'] = None


        # -----------------------
        # - print dei parametri
        # -----------------------
    if args['parameters']:
        print()
        for key, val in args.items():
            print('     {0:<20}: {1}'.format(key,val))
        print()
        choice = input('press Enter to continue... (q|x to exit): ')
        if choice.lower() in ('x', 'q'): sysExit()

    return  args



def myHELP(text, default):
    myHelp = '''{TEXT}
    [ DEFAULT: {DEFAULT}]
            '''.format(TEXT=text, DEFAULT=default)

    return myHelp


####################################
# # _fileCheck()
####################################
def _fileCheck(fileName):
    fileName = fileName.strip().strip("'").strip()

    try:
        fileName = Path(fileName).resolve()     # strict=True dalla 3.6

    except Exception as why:
        print()
        print (str(why))
        # LnColor.printYellow ('  {FILE} is not a valid file...'.format(FILE=fileName) + LnColor.RESET)
        print()
        sysExit()

    return fileName

