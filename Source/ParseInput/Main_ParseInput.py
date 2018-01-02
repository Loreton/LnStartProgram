#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 17.17.50
#
# -----------------------------------------------

import  Source as Prj

# -----------------------------------------------------
# mi serve per passarlo come puntatore al ParseInput
# per chiamare la funzione delle command-line options
# La directory option conterrà i file che verranno
# richiamati in base ai parametri di input.
# -----------------------------------------------------
from . import options as functionsLibPtr



#######################################################
# USER ParseInput
#######################################################
def ParseInput(description='Loreto Start Program', programVersion='V0.1'):
    Ln = Prj.LnLib

    posizARGS = 1
    positionalParametersDict  =  {
        'totalcommander'        : "Total Commander",
        'tc'                    : "Total Commander",
        'executor'              : "Executor",
        'vscode'                : "Visual Studio code",
    }



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
    return  inpArgs
    Ln.Exit(9999)

