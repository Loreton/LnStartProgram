#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

__author__  : 'Loreto Notarantonio'
__version__ = '24-10-2017 15.41.20'


import sys
import os
import argparse
import collections
import platform
# mi serve per poi cercare i metodi dentro
this_mod = sys.modules[__name__]

posizARGS = 0
#############################################################
# - parseInput()
#############################################################
def ParseInput(gVars, args, programVersion=None):
    global cPrint,  gv, posizARGS
    posizARGS = 1
    gv = gVars

    cPrint = gv.Ln.LnColor()
    if not programVersion: programVersion = 'unknown'

     # definizioni per mantenere insalterato l'ordine
    if posizARGS == 2:
        positionalActionsDict  =  {
            'edit': {
                'conf'    : "edit configuration file"
            },

            'connect': {
                'ssh'       : "kitty ssh verso un server",
                'winscp'    : "winscp interface",
                'jbossgui'  : "apertura di una cli GUI verso JBoss",
                'gui'       : "apertura di una cli GUI verso JBoss",
                'cli'       : "apertura di una cli verso JBoss",
            },
        }
    else:
        positionalActionsDict  =  {
            'conf'      : "edit configuration file",

            'LnDisk'    : "copia della directory Lndisk..",
        }




        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) <= posizARGS: sys.argv.append('-h')

    # mainArgs   = prepareArgParse2Levels(positionalActionsDict2, programVersion)
    mainArgs                 = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM               = commonParsing(mainArgs.mainCommand)
    InputPARAM.mainCommand   = mainArgs.mainCommand
    InputPARAM.actionCommand = '.'.join(mainArgs.mainCommand)

        # ---------------------------------
        # setting della parte di logging
        # logMODULE  contiene la lista dei moduli da tracciare
        # logCONSOLE True/False
        # LOGGER     True/False
        # ---------------------------------
    InputPARAM.LOGGER  = False
        # - copiamo i moduli in logMODULE
    if not InputPARAM.logCONSOLE == False: # potrebbe essere [] oppure ['xxx', 'yyyy']
        InputPARAM.logMODULE    = InputPARAM.logCONSOLE[:]
        InputPARAM.LOGGER       = True
        InputPARAM.logCONSOLE   = True

    elif not InputPARAM.logMODULE == False: # potrebbe essere [] oppure ['xxx', 'yyyy']
        InputPARAM.LOGGER       = True
        InputPARAM.logCONSOLE   = False


    print ()



        # -----------------------------------------------------
        # - convert  InputPARAM (argparse.Namespace) in dict
        # -----------------------------------------------------
    myDict = {}
    for key, val in vars(InputPARAM).items():
        myDict[key] = val

            # -----------------------------------------
            # - Controlli
            # -----------------------------------------
    if InputPARAM.fDisplayParam:
        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        dictID = vars(InputPARAM)
        for key, val in sorted(dictID.items()):
            TYPE = '(' + str(type(val)).split("'")[1] + ')'
            cPrint.Cyan('{0:<20} : {1:<6} - {2}'.format(key, TYPE, val), tab = 8)


        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()

    # if InputPARAM.fEDIT_CONFIG or InputPARAM.serverName.startswith('conf'):
    #     EditPrjConfig(gv)

    # sys.exit()
    return myDict



#############################################################
# - prepareArgParse()
#############################################################
def prepareArgParse(positionalActionsDict, programVersion):
    mainHelp    = "default help"
    description = "call Program"

    # - preparazione lista per il display
    totalCMDLIST = []


    if posizARGS == 2:
        for key, val in positionalActionsDict.items():
            totalCMDLIST.append('\n')
            totalCMDLIST.append('      * {0}'.format(key))
            if isinstance(val, dict):
                for key1, val1 in val.items():
                    totalCMDLIST.append('          {0:<30} : {1}'.format(key1, val1))
        cmdLIST = '\n'.join(totalCMDLIST)
        metavarStr  = cPrint.getCyanH('primaryCommand & actionCommand\n')
        helpStr = 'comando e sottocomando come elencato di seguito.'

    else:
        for key, val in positionalActionsDict.items():
            totalCMDLIST.append('\n')
            totalCMDLIST.append('          {0:<30} : {1}'.format(key, val))
        cmdLIST = ''.join(totalCMDLIST)
        metavarStr = cPrint.getCyanH('primaryCommand\n')
        helpStr     = 'comando come elencato di seguito.'



    mainHelp="""
        Immettere uno dei seguenti valori/comandi/action:
        (con il parametro -h se si desidera lo specifico help)
                {CMDLIST}\n""".format(CMDLIST=cmdLIST)

    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=cPrint.getYellow(description),
        usage='',                                          # non voglio lo usage
        epilog=cPrint.getYellow(mainHelp),
        conflict_handler='resolve',
    )


    myParser.add_argument('--version',
                            action='version',
                            version='{PROG} Version: {VER}'.format(PROG='JBossCMK', VER=programVersion))
                            # version='%(prog)s {VER}'.format(VER=programVersion))


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


    if posizARGS == 2:
        actionCommand = mainArgs.mainCommand[1]
            # print dell'HELP in base al primaryComand passato
        ptr = positionalActionsDict[primaryCommand]
        if not actionCommand in ptr.keys():
            print()
            cPrint.Cyan(".... Unrecognized subcommand [{0}]. Valid values for [{1}] command are:".format(actionCommand, primaryCommand), tab=8)
            for key, val in ptr.items():
                cPrint.CyanH ('{0:<20}    : {1}'.format(key, val), tab=16)
            exit(1)


    return mainArgs



###################################################
# - commonParsing
###################################################
def commonParsing(positionalParm, DESCR='CIAO DESCR'):
    if posizARGS == 2:
        mainCommand, actionCommand = positionalParm
        funcToCall = mainCommand.upper()                                           # function: CONNECT      param:ssh
    else:
        mainCommand   = 'CONNECT'
        mainCommand   = positionalParm[0]
        actionCommand = positionalParm[0]
        funcToCall    = mainCommand.upper() + '_' + '_'.join(positionalParm).upper()   # function: CONNECT_SSH
        funcToCall    = '_'.join(positionalParm).upper()                       # function: SSH


    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=cPrint.YEL, ACTION=mainCommand, COLRESET=cPrint.RESET)
    myParser = argparse.ArgumentParser( description='{0} Command'.format(mainCommand),
                                        add_help=True, usage=usageMsg,
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        )



        # use dispatch pattern to invoke method with same name
        # ritorna un nameSpace

    if hasattr(this_mod,  funcToCall):
        getattr(this_mod, funcToCall)(myParser, actionCommand)
    else:
        cPrint.Cyan ('[{0}] - Command not yet implemented!'.format(funcToCall))
        sys.exit(1)


        # ------------------------------------------------
        # - skip first/action parameter
        # ------------------------------------------------
    args = myParser.parse_args(sys.argv[len(positionalParm)+1:])

    return args







# ---------------------------
# - _debugOptions
# ---------------------------
def _debugOptions(myParser, required=False):
    '''
        parser.add_argument('--three',          nargs=3)
        parser.add_argument('--optional',       nargs='?')
        parser.add_argument('--all',            nargs='*')
        parser.add_argument('--one-or-more',    nargs='+')
    '''
    mandatory = cPrint.getMagentaH('is MANDATORY - ') if required else cPrint.getCyanH('is OPTIONAL - ')

    logGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo

        # log debug su file
    DEFAULT = False
    logGroup.add_argument( "--log",
                            required=required,
                            # action="store_true",
                            dest="logMODULE",
                            default=DEFAULT,
                            nargs='*',
                            help=mandatory + cPrint.getYellow("""attivazione log.
            E' possibile indicare una o più stringhe
            per identificare le funzioni che si vogliono inserire nel log.
            Possono essere anche porzioni di funcName separate da ' ' Es: pippo uto ciao
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))

        # log debug su console
    logGroup.add_argument( "--log-console",
                            required=required,
                            dest="logCONSOLE",
                            default=DEFAULT,
                            nargs='*',
                            help=mandatory + cPrint.getYellow("""attivazione log sulla console.
            E' possibile indicare una o più stringhe
            per identificare le funzioni che si vogliono inserire nel log.
            Possono essere anche porzioni di funcName separate da ' ' Es: pippo uto ciao
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))



    myParser.add_argument( "-D", "--debug",
                            required=required,
                            action="store_true",
                            dest="fDEBUG",
                            default=DEFAULT,
                            help=mandatory + cPrint.getYellow("""enter in DEBUG mode..
    [DEFAULT: {DEF}]
    """.format(DEF=DEFAULT)))

    myParser.add_argument( "--elapsed",
                            required=required,
                            action="store_true",
                            dest="fELAPSED",
                            default=DEFAULT,
                            help=mandatory + cPrint.getYellow("""display del tempo necessario al processo..
    [DEFAULT: {DEF}]
    """.format(DEF=DEFAULT)))


    myParser.add_argument( "--parameters",
                            required=required,
                            action="store_true",
                            dest="fDisplayParam",
                            default=DEFAULT,
                            help=mandatory + cPrint.getYellow("""display del tempo necessario al processo..
    [DEFAULT: {DEF}]
    """.format(DEF=DEFAULT)))







# ---------------------------
# - A C T I O N s
# ---------------------------

def SHARED_COMMAND(myParser, action):
    from . import ParseInput_Rsync as connect

    if len(sys.argv) <= posizARGS: sys.argv.append('-h')

    connect.SetGlobals(cPrint)
    connect.ExecuteOptions(myParser, required=False)
    # connect.DestServer(myParser, required=True)

    _debugOptions(myParser)


def LNDISK(myParser, action):
    SHARED_COMMAND(myParser, action)







# ------------------------------------------
# - EDIT nel caso di comandi ad un livello
# ------------------------------------------
def CONF(myParser, action):
    EditPrjConfig()

def EditPrjConfig():
    myEditor = (os.environ.get('EDITOR'))
    if not myEditor:
        if 'editor' in gv.ini.MAIN:
            myEditor = gv.ini.MAIN.editor
        elif platform.system() == 'Windows':
            myEditor = 'wordpad.exe'
        else:
            myEditor = 'vi'

    command = [
                myEditor,
                gv.env.iniFileName
            ]

    # print ('running command:', command)
    rCode = os.system(' '.join(command))

    # cPrint.Cyan('configuration file can be edited [RCODE: {}]'.format(rCode), tab=4)
    sys.exit()