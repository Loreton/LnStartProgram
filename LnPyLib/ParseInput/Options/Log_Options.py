# updated by ...: Loreto Notarantonio
# Version ......: 03-01-2018 10.14.17

from    . ColoredHelp import coloredHelp
from  ... Common.LnColor import LnColor; C=LnColor()

#######################################################
# LOG options
#######################################################
def logOptions(myParser, defaultLogFile):


        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------log options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=coloredHelp('', default=None))


    logGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo
        # log debug su console
    logGroup.add_argument( "--log-console",
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=coloredHelp("""attivazione log sulla console.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo pluto ciao""", default=False))

        # log debug su file
    logGroup.add_argument('--log',
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=coloredHelp("""attivazione log sul file.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo pluto ciao
    verra' utilizzao il file di log definito tramite --log-filename.""", default=False))


        # definizione file di log
    myParser.add_argument('--log-filename',
                                metavar='',
                                required=False,
                                default=defaultLogFile,
                                help=coloredHelp('log fileName... (valid only with --log option specified)', default=defaultLogFile))



    myParser.add_argument( "--loglevel",
                                metavar='',
                                required=False,
                                default='info',
                                choices=['info', 'warn', 'debug'],
                                help=coloredHelp("log level", default='info'))


