#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# LnVer_2017-11-01_12.21.31
# -----------------------------------------------

from . S110_MyHelp      import myHELP
from . S120_check_file  import check_file

#######################################################
# PROGRAM options
#######################################################
def programParameters(myParser, gVar, required=False):
    # mandatory = cPrint.getMagentaH('is MANDATORY - ') if required else cPrint.getCyanH('is OPTIONAL - ')
    myParser.add_argument('---------------program-options ----',
                                required=False,
                                action='store_true',
                                help=myHELP('', None))

    myParser.add_argument('--program',
                                required=False,
                                default='noProgram',
                                metavar='program',
                                help=myHELP('Specify the program to start', 'noProgram'))

    myParser.add_argument('--subst',
                                required=False,
                                default=None,
                                metavar='subst',
                                help=myHELP('Specify the SUBST drive', None))

    myParser.add_argument('--config-file',
                                metavar='',
                                type=check_file,
                                required=False,
                                default=gVar.defaultConfigFile,
                                help=myHELP('Specifies config fileName...', gVar.defaultConfigFile))


    myParser.add_argument('--rootDir',
                                metavar='',
                                type=check_file,
                                required=False,
                                default=gVar.defaultRootDir,
                                  help=myHELP('Specifies caller directory', gVar.defaultRootDir))




