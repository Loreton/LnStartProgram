#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.56.43
# -----------------------------------------------
from  subprocess import Popen
from  pathlib import PureWindowsPath, WindowsPath         # dalla versione 3.4


from .. Logger.SetLogger import SetLogger

#########################################################################
#
#########################################################################
def StartProgram(textMsg, CMDList):
    logger = SetLogger(__name__)

        # --------------------------------------------------
        # - Nella lista del comando potrebbero essere presenti
        # - path di file in formato PurePath... o simili
        # - e devo convertirli in str prima di lanciarli
        # --------------------------------------------------
    logger.info(textMsg)
    myCMDList = []
    for line in CMDList:
        if isinstance(line, (PureWindowsPath, WindowsPath )):
            line = str(line)
        myCMDList.append(line)
        logger.info('   ' + line)

    procID = Popen(myCMDList, shell=False, universal_newlines=True)
    # print(procID)


import subprocess

##########################################################
# - timeout solo dalla Versione 3.3
##########################################################
def ExecGetOut(cmdList, timeout=5):
    rCode, errData, outData = 0, '', ''

    try:
        # universal_newlines=False ritorna byteData
        outData = subprocess.check_output(cmdList, stdin=None, stderr=None, shell=False, universal_newlines=True, timeout=timeout)

    except subprocess.TimeoutExpired:
        errData = "TimedOUT occurred"
        rCode = 1

    except (Exception) as why:
        errData  = '{0} - {1}'.format('Exception', str(why))
        rCode = 1


    # print(type(outData))
    # print (outData)
    return rCode, outData, errData


##########################################################
# - timeout solo dalla Versione 3.3
##########################################################
def OutOnFile(cmdList, timeout=5):
    rCode, errData, fileData = 0, '', "/tmp/outOnFile.txt"
    vin  = None; # vin  = open("validationInput", 'r')
    vout = open(fileData, 'w')


    try:
        rCode = subprocess.call(cmdList, stdin=vin, stdout=vout, stderr=vout, shell=False, timeout=timeout)

    except subprocess.TimeoutExpired:
        errData = "TimedOUT occurred"
        rCode = 1

    except (Exception) as why:
        errData  = '{0} - {1}'.format('Exception', str(why))
        rCode = 1

    vout.close();  # vin.close()

    with open(fileData, 'r') as f:
        outData = f.read()

    return rCode, outData, errData, fileData



