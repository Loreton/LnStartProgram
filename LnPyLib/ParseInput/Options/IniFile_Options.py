#
# updated by ...: Loreto Notarantonio
# Version ......: 05-02-2018 16.55.57
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
