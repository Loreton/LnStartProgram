#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################

import types, os, inspect, sys

from ..LnCommon.LnLogger import SetLogger       # OK funziona dalla upperDir del package
from ..LnCommon.LnColor  import LnColor


EXIT_KEYB   = -30
PAUSE_KEYB   = -31
EXIT_STACK  = -32

# =======================================================================
# - 13 Maggio 2010  : Aggiunto il parametro stackLevel
# - stackLevel viene impostato per indicare un livello diverso del chiamante
# - Ad esempio la Prj.exit() chimaera wuesta exit con stackLevel=2 in modo
# - da saltare se stessa.
# =======================================================================
def Exit(rcode, text, printStack=False, stackLevel=9, console=True):
    logger  = SetLogger(package=__name__)
    cPrint       = LnColor()

    if text == None:
        textList = ['No error message passed']
    elif isinstance(text, list):
        textList = text
        pass
    else:
        textList = text.split('\n')

        # -------------------------------
        # - Display dell'Errore
        # -------------------------------
    if rcode == 0:
        printColor = cPrint.Green
        logWrite = logger.debug
    else:
        printColor = cPrint.ERROR
        logWrite = logger.error


        # -------------------------------
        # - Display dello STACK
        # - http://blog.dscpl.com.au/2015/03/generating-full-stack-traces-for.html
        # -------------------------------

    if console:
        printColor("  RCODE       : {0}".format(rcode), tab=4)
        printColor("  TEXT Message: ", tab=4 )
        for line in textList:
            printColor (line, tab=8)

    else:
        logWrite("  RCODE       : {0}".format(rcode))
        logWrite("  TEXT Message: " )
        for line in textList:
            logWrite(' '*10 + "{0}".format(line))

    if printStack:
        logWrite("EXIT STACK:")
        print()
        for i in reversed(list(range(1, stackLevel))):
            caller = _calledBy(i)
            if not 'index out of range' in caller:
                logWrite("    {0}".format(caller))
                if console:
                    printColor(caller, tab=8)
    sys.exit(rcode)



###############################################
#
###############################################
def _calledBy(deepLevel=0):

    try:
        caller = inspect.stack()[deepLevel + 1]

    except Exception as why:
        return '{0}'.format(why)
        return 'Unknown - {0}'.format(why)

    programFile = caller[1]
    lineNumber  = caller[2]
    funcName    = caller[3]
    lineCode    = caller[4]

    fname       = os.path.basename(programFile).split('.')[0]
    str = "[{0}-{1}:{2}]".format(fname, caller[3], int (caller[2]) )
    if funcName == '<module>':
        str = "[{0}:{1}]".format(fname, lineNumber)
    else:
        str = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)
    return str