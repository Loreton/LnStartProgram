#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 04-01-2018 16.18.16
#

import  sys
from    pathlib import Path
from    time    import strftime

from  . CreateParser         import createParser         as LnCreateParser
from  . PositionalParameters import positionalParameters as LnPositionalParameters
from  . Options.Log_Options          import logOptions           as LnLogOptions
from  . Options.IniFile_Options      import iniFileOptions       as LnIniFileOptions
from  . Options.Debug_Options        import debugOptions         as LnDebugOptions
from .. Common.Exit          import Exit                 as LnExit

#######################################################
# ParseInput
#######################################################
def processInput(nPosArgs, parmDict, funcLibPtr, defFuncToCall='programOptions', progrVersion=None, prjDescr='', prjDir=None, prjName=None):
    '''
        process command line input
        funcLibPtr: where to looking for the function to be called

    '''

        # ---------------------------------------------------------
        # -   Identifichiamo il nome progetto dal nome directory
        # ---------------------------------------------------------
    if not prjDir:
        prjDir = Path(sys.argv[0]).resolve().parent
        if prjDir.name.lower() in ['bin',  'source']:
            prjDir = prjDir.parent

    if not prjName:
        prjName = prjDir.name   # nome della dir del programma




            # ====================================================
            # = POSITIONAL PARAMETERs
            # - read positional paramenters
            # - ...and create functionToBeCalled as:
            # ====================================================
    if nPosArgs > 0:
            # - create a specific parser for positional parameters
        posParser = LnCreateParser(prjName=prjName,
                                    prjVersion=progrVersion,
                                    prjDescr=prjDescr,
                                    usageDescr='Enter positional parameters',
                                    )        # creazione di un parser..

            # - get positional Parameter
        positionalParm = LnPositionalParameters(posParser, nPosArgs, parmDict)
            # - try to create a function to be called
        functionToBeCalled  = '_'.join(positionalParm).upper()                       # function: PRI_SEC

    else:
        functionToBeCalled = defFuncToCall


        # - if not posParam force fixedName for OptionalParameters
    # if not functionToBeCalled:


        # - search functionToBeCalled in Prj package
    if not hasattr(funcLibPtr, functionToBeCalled):
        msg = ['''[{0}] - Command not defined in funcLibPtr lib!
            valid functions are:
        '''.format(functionToBeCalled)]
        for item in vars(funcLibPtr):
            if item.startswith('__'): continue
            msg.append((item))
        LnExit(1, msg)



        # ====================================================
        # = OPTIONAL PARAMETERs
        # ====================================================
    defaultIniFile = str(Path(prjDir , 'conf', prjName + '.ini'))
    defaultLogFile = Path(prjDir , 'log', prjName + strftime('_%Y-%m-%d') + '.log')

        # - create PARSER for optional parameters
    myParser = LnCreateParser(prjName=prjName,
                                    prjVersion=progrVersion,
                                    prjDescr='options for {} command'.format(functionToBeCalled),
                                    usageDescr='please enter one o more listed options...',
                                )        # creazione di un parser ..

        # call the function...
    getattr(funcLibPtr,  functionToBeCalled)(myParser)

        # ====================================================
        # - DEFAULT optional parameters valid for all projects
        # ====================================================
    LnIniFileOptions(myParser, defaultIniFile)
    LnLogOptions(myParser, defaultLogFile)
    LnDebugOptions(myParser)




        # ===========================================================
        # = lancio del parser... per i restanti parametri opzionali
        # ===========================================================
    args = vars(myParser.parse_args(sys.argv[nPosArgs+1:]))


        # ----------------------------------------------
        # - creazione entry per i parametri posizionali
        # ----------------------------------------------
    if nPosArgs > 0: args['firstPosParameter']  = positionalParm[0]
    if nPosArgs > 1: args['secondPosParameter'] = positionalParm[1]



        # --------------------------------------------
        # - verifica della congruenza di alcuni parametri:
        # - --log=False azzera anche il --log-filename]
        # --------------------------------------------
    if args['log'] == False: args['log_filename'] = None
    args['config_file'] = args['ini_file']


        # ----------------------------------------
        # - cancellazione delle option di comodo
        # -    containing -->   'options '
        # ----------------------------------------
    keysToBeDeleted = []
    for key, val in args.items():
        if 'options ' in key:
            keysToBeDeleted.append(key)

    for key in keysToBeDeleted:
        if args['debug']: print ('.... deleting ', key)
        del args[key]


        # ----------------------------------------
        # - ... e print dei parametri
        # ----------------------------------------
    if args['dis_parameters']:
        print()
        for key, val in args.items():
            print('     {0:<20}: {1}'.format(key, val))
        print()
        choice = input('press Enter to continue... (q|x to exit): ')
        if choice.lower() in ('x', 'q'): sys.exit()

    return args