#
# updated by ...: Loreto Notarantonio
# Version ......: 09-01-2018 16.03.12
#

import sys

from  .. Common.LnColor import LnColor; C=LnColor()


#######################################################
# PROGRAM POSITIONAL parameters
#######################################################
def positionalParameters(myParser, nARGS, positionalParametersDict):
    '''
    read and check positional parameters.
    args:
        myParser:   parser already defined from the caller
        nARGS:      number o positional parameters
        pos...Dict:      dictionary with positional parameters

    return:
        []                          if nARGS == 0
        [firstParam]                if nARGS == 1
        [firstParam, secondParam]   if nARGS == 2
    '''
    global posizARGS
    posizARGS                = nARGS

        # - usciamo se non abbiamo positional Parameters da gestire
    if posizARGS < 1 or posizARGS > 2: return []
    if positionalParametersDict == {}: return []

    if len(sys.argv) == 1: sys.argv.append('-h')


        # ----------------------------------------------
        # - praparazione del display dei parametri...
        # ----------------------------------------------
    cmdList = []
    if posizARGS == 1:
        cmdList.append(C.getColored(color=C.magentaH, text='\n      Primary MANDATORY Parameters... enter one of them'))
        for key, val in positionalParametersDict.items():
            # keyColor = C.getColored(color=C.yellowH, text=key)
            valColor = C.getColored(color=C.yellow, text=val)
            cmdList.append('')
            cmdList.append('          {0:<20} : {1}'.format(key, valColor))
            cmdList.append('')

        paramName = 'primaryCommand'

    elif posizARGS == 2:
        cmdList.append(C.getColored(color=C.magentaH, text='\n      Primary MANDATORY Parameters... enter a couple of them'))
        for key, val in positionalParametersDict.items():
            cmdList.append('')
            cmdList.append('      * {0}'.format(key))
            if isinstance(val, dict):
                for key1, val1 in val.items():
                    valColor = C.getColored(color=C.yellow, text=val1)
                    cmdList.append('          {0:<15} : {1}'.format(key1, valColor))
            cmdList.append('')

        paramName = 'priSecCommand'

    else:
        return []


        # -----------------------------------
        # - creazione di un parser ad hoc
        # -----------------------------------

    myParser.add_argument(paramName,
                metavar='\n'.join(cmdList),
                type=str,
                nargs=posizARGS,
                help='')

        # ----------------------------------------------------------
        # - read positional parameter forcing sys.argv[xx]
        # ----------------------------------------------------------
    mainArgs   = myParser.parse_args(sys.argv[1:posizARGS+1])
    myPosParam = vars(mainArgs)[paramName]

    checkPositionaParam(myParser, myPosParam, positionalParametersDict)

    # return listtype
    return myPosParam

####################################
# # _checkPositionaParam()
####################################
def checkPositionaParam(myParser, posParam, positionalParametersDict):

    primaryCommand   = posParam[0].lower()
    if not (primaryCommand in positionalParametersDict.keys()):
        myParser.print_help()
        C.printColored(color=C.yellow, text=".... Unrecognized command [{0}]. Valid values are:".format(primaryCommand), tab=8)
        for positionalParm in positionalParametersDict.keys():
            C.printColored(color=C.yellow, text=positionalParm, tab=16)
        print()
        exit(1)

    if posizARGS == 2:
        ptr = positionalParametersDict[primaryCommand]
        secondaryCommand = posParam[1].lower()
        if not secondaryCommand in ptr.keys():
            myParser.print_help()
            print()
            C.printColored(color=C.cyan, text=".... Unrecognized subcommand [{0}]. Valid values for '{1}' primary command are:".format(secondaryCommand, primaryCommand), tab=8)
            for key, val in ptr.items():
                C.printColored(color=C.cyan, text='{0:<20}    : {1}'.format(key, val), tab=16)
            print()
            exit(1)
