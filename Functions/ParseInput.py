#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 19-10-2017 15.57.50
# -----------------------------------------------
from    sys     import argv as sysArgv, exit as sysExit
# import sys
from    pathlib import Path
# import  os
import  argparse
import  time




def ParseInput():
    # =============================================
    # = Parsing
    # =============================================
    if len(sysArgv) == 1: sysArgv.append('-h')

    defaultLogDir  = Path(sysArgv[0]).resolve().parent
    defaultFname   = defaultLogDir.name
    defaultLogFile = Path(defaultLogDir , 'log', defaultFname + time.strftime('_%Y-%m-%d') + '.log')

    defaultCallerDir  = Path(sysArgv[0]).resolve().parent

    mainHelp=""
    # myParser = argparse.ArgumentParser(description='PyD3 is a command line tool used to organize metadata of mp3 files')
    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description='Partenza di programmi',
        usage='',                                          # non voglio lo usage
        epilog=mainHelp,
        conflict_handler='resolve',
    )

    myParser.add_argument('--program',     required=False, default='TotalCommander', metavar='program', help=myHELP('Specify the program to start', 'TotalCommander'))
    myParser.add_argument('--subst',       required=False, default=None, metavar='subst', help=myHELP('Specify the SUBST drive', None))
    myParser.add_argument('--go',          required=False, action='store_true',  help=myHELP('Specifies if program must be started', False))
    myParser.add_argument('--debug', '-D',  required=False, action='store_true',  help=myHELP('Specifies if program must be started', False))
    myParser.add_argument('--parameters',  required=False, action='store_true', help=myHELP('Display input paramenters..', False))
    myParser.add_argument('--log',         required=False, action='store_true', help=myHELP('Enable log on file... ', False))
    myParser.add_argument('--log-console', required=False, action='store_true', help=myHELP('Enable log on console... ', False))
    myParser.add_argument('--log-file',    required=False, default=defaultLogFile, help=myHELP('Specifies log fileName...', defaultLogFile))
    myParser.add_argument('--callerDir',   required=False, default=defaultCallerDir, help=myHELP('Specifies caller directory', defaultCallerDir))

    args = vars(myParser.parse_args())

        # -----------------------
        # - verifica del caller
        # -----------------------
    callerDir = args["callerDir"].strip().strip("'").strip()
    try:
        callerDir = Path(callerDir).resolve()     # strict=True dalla 3.6
    except Exception as why:
        print()
        print (str(why))
        print()
        sysExit()
    args["callerDir"] = callerDir


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