#
# updated by ...: Loreto Notarantonio
# Version ......: 04-01-2018 16.08.20
#

import  argparse

from  .. Common.LnColor import LnColor; C=LnColor()
from   . Options.ColoredHelp import coloredHelp

# ----------------------------------------------
# - creazione del parser
# ----------------------------------------------
# def createParser(passedData):
def createParser(prjName, prjVersion, prjDescr, usageDescr='usage Description', epilogDescr='='):
    '''
    create a parser with the program descriptions characteristics
    '''
    desciption = C.getColored(color=C.yellow, text="{} commands".format(prjDescr))
    if epilogDescr == '=': epilogDescr = usageDescr

    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=desciption,
        # usage='',                                          # non voglio lo usage
        usage=C.getColored(color=C.yellow, text=usageDescr),
        epilog=C.getColored(color=C.yellow, text=epilogDescr),
        conflict_handler='resolve',
    )

    myParser.add_argument('--version',
            action='version',
            version='{PROG}  Version: {VER}'.format (PROG=prjName, VER=prjVersion ),
            help=coloredHelp("show program's version number and exit") )

    return myParser