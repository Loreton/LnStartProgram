
from . S110_MyHelp import myHELP

from LnLib.Common.LnColor import LnColor
C=LnColor()
#######################################################
# PROGRAM POSITIONAL parameters
#######################################################
def positionaParameters(myParser, required=False):
    # mandatory = cPrint.getMagentaH('is MANDATORY - ') if required else cPrint.getCyanH('is OPTIONAL - ')

    posizARGS = 1
    positionalParametersDict  =  {
        'totalcommander'        : "Total Commander",
        'tc'                    : "Total Commander",
        'executor'              : "Executor",
    }

    cmdList = []
    cmdList.append(C.getColored(color=C.magentaH, text='\n      Primary MANDATORY Parameters... enter one of them'))
    for key, val in positionalParametersDict.items():
        keyColor = C.getColored(color=C.yellowH, text=key)
        valColor = C.getColored(color=C.yellow, text=val)
        cmdList.append('\n')
        cmdList.append('          {0:<20} : {1}'.format(key, valColor))

        # -------------------------------------------------------
        # - con nargs viene tornata una lista con nArgs
        # - deve prendere il comando primario e poi il sottocomando
        # -------------------------------------------------------
    myParser.add_argument('mainCommand',
                metavar=''.join(cmdList),
                type=_checkPositionaParam,
                nargs=1,
                help='')
        #         help=C.getColored(color=C.yellowH, text='''
        # immettere uno dei comandi sopra elencati'''))

    '''
    cmdList = []
    for key, val in positionalActionsDict.items():
        cmdList.append('\n')
        cmdList.append('          {0:<30} : {1}'.format(key, val))
    positionalParametersString = ''.join(cmdList)
    metavarStr = cPrint.getCyanH('primaryCommand\n')
    helpStr    = 'comando come elencato di seguito.'



    mainHelp="""
        Immettere uno dei seguenti valori/comandi/action:
        (con il parametro -h se si desidera lo specifico help)
                {CMDLIST}\n""".format(CMDLIST=cmdList)

        # -------------------------------------------------------
        # - con nargs viene tornata una lista con nArgs
        # - deve prendere il comando primario e poi il sottocomando
        # -------------------------------------------------------
    myParser.add_argument('mainCommand',
                metavar=metavarStr + cPrint.getYellow(mainHelp),
                type=str,
                nargs=posizARGS,
                help=helpStr
                )


        # ----------------------------------------------------------
        # - lanciamo il parse dei parametri subito dopo quelli posizionali
        # ----------------------------------------------------------
    mainArgs         = myParser.parse_args(sys.argv[1:posizARGS+1])
    primaryCommand   = mainArgs.mainCommand[0]

        # print dell'HELP per il primaryCommand errato
    if not (primaryCommand in positionalActionsDict.keys()):
        myParser.print_help()
        cPrint.Yellow(".... Unrecognized command [{0}]. Valid values are:".format(primaryCommand), tab=8)
        for positionalParm in positionalActionsDict.keys():
            cPrint.Yellow (positionalParm, tab=16)
        exit(1)


    return mainArgs
    '''




####################################
# # _fileCheck()
####################################
def _checkPositionaParam(value):
    print (value)

    return value
