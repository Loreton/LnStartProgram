#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 15-02-2018 15.19.07
#
# -----------------------------------------------

import  Source as Prj

# -----------------------------------------------------
# mi serve per passarlo come puntatore al ParseInput
# per chiamare la funzione delle command-line options
# La directory option conterrà i file che verranno
# richiamati in base ai parametri di input.
# -----------------------------------------------------
from . import Options as functionsLibPtr



#######################################################
# USER ParseInput
#######################################################
def ParseInput(description='Loreto Start Program', programVersion='v2018.01.31'):
    Ln = Prj.LnLib

    posizARGS = 1
    positionalParametersDict  =  {
        'totalcommander'        : "Total Commander",
        'tc'                    : "Total Commander",
        'executor'              : "Executor",
        'vscode'                : "Visual Studio code",
        'winscp_bdi'            : "WinSCP con il winscp_bdi.ini",
        'winscp_loreto'         : "WinSCP con il winscp_loreto.ini",
    }

    ''' DEBUG
    msg = []
    for item in vars(functionsLibPtr):
        if item.startswith('__'): continue
        msg.append(item)
    Ln.Exit(1, msg)
    '''

    inpArgs = Ln.processInput(
            nPosArgs=posizARGS,
            parmDict=positionalParametersDict,
            funcLibPtr=functionsLibPtr,
            defFuncToCall='programOptions', # function to call only for posizARGS==0
            progrVersion=programVersion,
            prjDescr=description,
            prjDir=None,
            prjName=None)

    # inpArgs['programToStart'] = inpArgs['firstPosParameter']

    # if inpArgs['edit_ini']:
    #     EditPrjConfig(inpArgs['ini_file'])

    return  inpArgs
    Ln.Exit(9999)







import os, platform, sys
# ------------------------------------------
# - EDIT nel caso di comandi ad un livello
# ------------------------------------------
def EditPrjConfig(filename01, filename02='', filename03=''):
    myEditor = (os.environ.get('LN_EDITOR'))


    if not myEditor:
        if platform.system() == 'Windows':
            myEditor = 'notepad.exe'
        else:
            myEditor = 'vi'


    command = [
                myEditor,
                filename01,
                filename02,
                filename03,

            ]

    # print ('running command:', command)
    rCode = os.system(' '.join(command))

    # cPrint.Cyan('configuration file can be edited [RCODE: {}]'.format(rCode), tab=4)
    sys.exit()