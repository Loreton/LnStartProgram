#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 31-01-2018 16.49.12
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


