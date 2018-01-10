#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 17.42.50
#


from . check_file  import check_file
from . ColoredHelp import coloredHelp

#######################################################
#
#######################################################
def iniFileOptions(myParser, defaultIniFile):

    myParser.add_argument('--ini-file', '--config-file',
                                metavar='',
                                type=check_file,
                                required=False,
                                default=defaultIniFile,
                                help=coloredHelp('Specifies ini configuration fileName...', default=defaultIniFile))
