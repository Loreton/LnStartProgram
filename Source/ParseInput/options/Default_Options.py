#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 15.19.14
#
# -----------------------------------------------
import  Source as Prj
#######################################################
# PROGRAM options
#######################################################
def programOptions(myParser):
    Ln = Prj.LnLib
    C = Ln.Color()

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------program options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=Ln.coloredHelp('', None))


    myParser.add_argument('--subst',
                                required=False,
                                default=None,
                                metavar='subst',
                                help=Ln.coloredHelp('Specify the SUBST drive', default=None, required=False))

    myParser.add_argument('--root-dir',
                                metavar='',
                                type=Ln.check_file,
                                required=False,
                                # default=gVar.defaultRootDir,
                                default=None,
                                  help=Ln.coloredHelp('Specifies LnDisk ROOT directory (ex: D:\LnDisk)', default=None))


