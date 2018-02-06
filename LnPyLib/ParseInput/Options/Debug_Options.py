#
# updated by ...: Loreto Notarantonio
# Version ......: 06-02-2018 09.50.49
#

from   . ColoredHelp import coloredHelp
from  ... Common.LnColor import LnColor; C=LnColor()

#######################################################
# DEBUG options
#######################################################
def debugOptions(myParser):

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------debug options ----')

    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=coloredHelp('', None))


    myParser.add_argument('--execute',
                                required=False,
                                action='store_true',
                                help=coloredHelp('Specifies if program must be started', default=False))

    myParser.add_argument('--debug',
                                required=False,
                                action='store_true',
                                help=coloredHelp('Specifies if program must be started', default=False))

    myParser.add_argument('--parameters',
                                required=False,
                                action='store_true',
                                help=coloredHelp('Display input paramenters..', default=False))


