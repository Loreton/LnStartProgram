#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 17-10-2017 08.47.22
# -----------------------------------------------
import sys, os
import argparse

def ParseInput():
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='PyD3 is a command line tool used to organize metadata of mp3 files')
    parser.add_argument('--program', metavar='program', help='Specify the program to start', required=False, default='TotalCommander')
    parser.add_argument('--subst',   metavar='subst', help='Specify the SUBST drive', required=False, default=None)
    parser.add_argument('--go',      help='Specifies if program must be started', action='store_true')
    parser.add_argument('--console', help='Specifies if console-log is desired', action='store_true')
    parser.add_argument('--caller',  help='Specifies caller directory', required=False, default=os.path.dirname(sys.argv[0]))
    args = vars(parser.parse_args())
    # print (args)

        # -----------------------
        # - verifica del caller
        # -----------------------
    caller = args['caller'].strip().strip("'").strip()
    if caller[-1] == '\\': caller = caller[:-1]
    args['caller'] = caller
    return  args
    # path,  action = args['p'], args['go']


