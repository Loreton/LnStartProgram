#
# updated by ...: Loreto Notarantonio
# Version ......: 15-02-2018 14.10.06
#


from . check_file  import check_file
from . ColoredHelp import coloredHelp

#######################################################
#
#######################################################
def iniFileOptions(myParser, defaultIniFile):

    # myParser.add_argument('--ini-file', '--config-file',
    myParser.add_argument('--ini-file',
                                metavar='',
                                type=check_file,
                                required=False,
                                default=defaultIniFile,
                                help=coloredHelp('Specifies ini configuration fileName...', default=defaultIniFile))

    myParser.add_argument('--edit-ini',
                                required=False,
                                action='store_true',
                                help=coloredHelp('Edit ini configuration fileName...', default=False))
