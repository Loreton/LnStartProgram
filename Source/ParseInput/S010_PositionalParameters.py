
from . S110_MyHelp import myHELP

#######################################################
# PROGRAM POSITIONAL parameters
#######################################################
def positionaParameters(myParser, required=False):
    # mandatory = cPrint.getMagentaH('is MANDATORY - ') if required else cPrint.getCyanH('is OPTIONAL - ')

    posizARGS = 1
    positionalParametersDict  =  {
        'conf'      : "edit configuration file",
        'LnDisk'    : "copia della directory Lndisk..",
    }

    cmdList = []
    for key, val in positionalParametersDict.items():
        cmdList.append('\n')
        cmdList.append('          {0:<30} : {1}'.format(key, val))

        # -------------------------------------------------------
        # - con nargs viene tornata una lista con nArgs
        # - deve prendere il comando primario e poi il sottocomando
        # -------------------------------------------------------
    myParser.add_argument('mainCommand',
                metavar=''.join(cmdList),
                type=_checkPositionaParam,
                nargs=1,
                help='''
        immettere uno dei comandi sopra elencati''')


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
