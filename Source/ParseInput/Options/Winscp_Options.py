#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-03-2018 09.07.25
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


    myParser.add_argument('--server',
                required=False,
                default='dummy',
                help=Ln.coloredHelp('Specify the SERVER name', default='dummy', required=False))


    myParser.add_argument('--port',
                required=False,
                default=22,
                metavar='portNO',
                help=Ln.coloredHelp('Specify the port number', default=22, required=False))

    myParser.add_argument('--new-instance',
                required=False,
                action='store_true',
                help=Ln.coloredHelp('Specify if NEW winScp-GUI must be started', default=False, required=False))

    myParser.add_argument('--checkdns',
                required=False,
                action='store_true',
                help=Ln.coloredHelp('Specify if launch gethostbyname before start winsco', default=False, required=False))

