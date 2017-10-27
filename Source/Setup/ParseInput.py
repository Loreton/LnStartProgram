#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.51.47
# -----------------------------------------------
from    sys     import argv as sysArgv, exit as sysExit
from    pathlib import Path
from    time import  strftime
import  argparse


class LnClass(): pass
gVar = LnClass()
from . import Parse_positionalParameters    as posParam
from . import Parse_logParameters           as logParam
from . import Parse_debugParameters         as debugParam




#######################################################
# ParseInput
#######################################################
def ParseInput(programVersion=0.1):
    if len(sysArgv) == 1: sysArgv.append('-h')

        # ---------------------------------------------------------
        # -   Identifichiamo il nome progetto dal nome directory
        # -   oppure passiamolo come parametro....
        # ---------------------------------------------------------
    gVar.programDir     = Path(sysArgv[0]).resolve().parent
    if gVar.programDir.name.lower() in ['bin',  'source']:
        gVar.programDir = gVar.programDir.parent

    gVar.prjName        = gVar.programDir.name   # nome della dir del programma

        # --------------------------
        # -   DEFAULT args VALUEs
        # --------------------------
    gVar.defaultLogFile    = Path(gVar.programDir , 'log', gVar.prjName + strftime('_%Y-%m-%d') + '.log')
    gVar.defaultConfigFile = Path(gVar.programDir , 'conf', gVar.prjName + '.ini')
    gVar.defaultRootDir    = gVar.programDir


        # --------------------------
        # -   MAIN HELP message
        # --------------------------
    mainHelp=""
    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description='Partenza di programmi',
        usage='',                                          # non voglio lo usage
        epilog=mainHelp,
        conflict_handler='resolve',
    )






        # configurazione Args ..
    myParser.add_argument('--version',
                            action='version',
                            version='{PROG}  Version: {VER}'.format (PROG=gVar.prjName, VER=programVersion ),
                            help=myHELP("show program's version number and exit") )

    # _programPositionaParameters(myParser)
    _programParameters(myParser)
    _logParameters(myParser)
    _debugParameters(myParser)



        # lancio del parser...
    args = vars(myParser.parse_args())


        # --------------------------------------------
        # - verifica della congruenza di alcuni parametri:
        # - --log=False azzera anche il --log-filename]
        # --------------------------------------------
    if args['log'] == False: args['log_filename'] = None


        # -----------------------
        # - print dei parametri
        # -----------------------
    if args['parameters']:
        print()
        for key, val in args.items():
            if 'options ____' in key:
                continue
            print('     {0:<20}: {1}'.format(key,val))
        print()
        choice = input('press Enter to continue... (q|x to exit): ')
        if choice.lower() in ('x', 'q'): sysExit()

    return  args







#######################################################
# DEBUG options
#######################################################
def _debugParameters(myParser, required=False):
    myParser.add_argument('---------------debug-options ----',
                                required=False,
                                action='store_true',
                                help=myHELP('', None))


    myParser.add_argument('--go',
                                required=False,
                                action='store_true',
                                help=myHELP('Specifies if program must be started', False))

    myParser.add_argument('--debug',
                                required=False,
                                action='store_true',
                                help=myHELP('Specifies if program must be started', False))

    myParser.add_argument('--parameters',
                                required=False,
                                action='store_true',
                                help=myHELP('Display input paramenters..', False))


#######################################################
# LOG options
#######################################################
def _logParameters(myParser, required=False):
    logGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo
    myParser.add_argument('---------------log-options ----',
                                required=False,
                                action='store_true',
                                help=myHELP('', None))

        # log debug su console
    logGroup.add_argument( "--log-console",
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=myHELP("""attivazione log sulla console.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo pluto ciao""", False))

        # log debug su file
    logGroup.add_argument('--log',
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=myHELP("""attivazione log sul file.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo pluto ciao
    verra' utilizzao il file di log definito tramite --log-filename.""", False))


        # definizione file di log
    myParser.add_argument('--log-filename',
                                metavar='',
                                required=False,
                                default=gVar.defaultLogFile,
                                help=myHELP('Specifies log fileName...', gVar.defaultLogFile))



#######################################################
# PROGRAM POSITIONAL parameters
#######################################################
def _programPositionaParameters(myParser, required=False):
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





#######################################################
# PROGRAM options
#######################################################
def _programParameters(myParser, required=False):
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
                                type=_fileCheck,
                                required=False,
                                default=gVar.defaultConfigFile,
                                help=myHELP('Specifies config fileName...', gVar.defaultConfigFile))


    myParser.add_argument('--rootDir',
                                metavar='',
                                        type=_fileCheck,
                                        required=False,
                                default=gVar.defaultRootDir,
                                  help=myHELP('Specifies caller directory', gVar.defaultRootDir))




















################################################
# formatting help message
################################################
def myHELP(text, default=None):
    if default:
        myHelp = '''{TEXT}
    [DEFAULT: {DEFAULT}]
        '''.format(TEXT=text, DEFAULT=default)
    else:
        myHelp = '''{TEXT}
        '''.format(TEXT=text)

    return myHelp


####################################
# # _fileCheck()
####################################
def _fileCheck(fileName):
    fileName = fileName.strip().strip("'").strip()

    try:
        fileName = Path(fileName).resolve()     # strict=True dalla 3.6

    except Exception as why:
        print()
        print (str(why))
        # LnColor.printYellow ('  {FILE} is not a valid file...'.format(FILE=fileName) + LnColor.RESET)
        print()
        sysExit()

    return fileName



####################################
# # _fileCheck()
####################################
def _checkPositionaParam(value):
    print (value)

    return value







# ELAPSED
'''
    myParser.add_argument( "--elapsed",
                            required=False,
                            action="store_true",
                            dest="fELAPSED",
                            default=False,
                            help=LnColor.getYellow("""display del tempo necessario al processo..
    [DEFAULT: False]
    """))

    gv.Time.processServices.end = time.time()

    gv.Time.Main.end = time.time()

    if gv.INPUT_PARAM.fELAPSED:
        print ()
        C.printYellow (' read ini file    : {0}'.format(gv.Time.readIniFile.end         - gv.Time.readIniFile.start))
        C.printYellow (' process ini file : {0}'.format(gv.Time.processIniFile.end      - gv.Time.processIniFile.start))
        C.printYellow (' get instances    : {0}'.format(gv.Time.getInstances.end        - gv.Time.getInstances.start))
        C.printYellow (' process services : {0}'.format(gv.Time.processServices.end     - gv.Time.processServices.start))
        print ()
        C.printYellow (' total job tooks  : {0}'.format(gv.Time.Main.end                - gv.Time.Main.start))
        print ()

'''
