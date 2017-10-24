#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2016, November
# ######################################################################################
import collections
import inspect, os
import sys

from LnLib.Common.LnColor  import LnColor
cPrint=LnColor()

# colori delle righe
DICT_LINE   = cPrint.CyanH
# VALUE_LINE  = cPrint.Yellow
VALUE_LINE  = cPrint.Cyan
VALUE_DATA  = cPrint.GreenH

getDICT_LINE   = cPrint.getCyanH
getVALUE_LINE  = cPrint.Cyan
getVALUE_DATA  = cPrint.GreenH

# LINEDATA_LIST=[]
# #######################################################
# #  ''' RECURSIVE '''
# # Ritorna una lista che contiene
# # l'alberatura delle key di un dictionary
# #    [level - keyName ]
# #######################################################
def PrintDictionary(myDict, myDictTYPES=[], keyList=[], level=0, whatPrint='LTKV', fPRINT=False, fEXIT=False, fPAUSE=False, maxDepth=10, header=None, stackLevel=2):
    if level == 0:
        PrintHeader('START - ', header, stackLevel=stackLevel+1)
        # LINEDATA_LIST = []

    if level > maxDepth: return

    # per evitare LOOP
    if level > 100: sys.exit()

    myTAB=' '*4*level   # Indent del dictionary
    for key, val in sorted(myDict.items()):                  # per tutte le chiavi del dict
        # if key in ['_myDictTYPES']: continue
            # - Se è un DICT iteriamo
        if type(val) in myDictTYPES:
            thisTYPE = str(type(val)).split("'")[1]
            if "DotMap" in thisTYPE:
                thisTYPE = 'LnDict'
            elif "OrderedDict" in thisTYPE:
                thisTYPE = 'oDict'
            else:
                thisTYPE = thisTYPE[-6:]
            # line0 = '[{LVL:2}] {TYPE:<8} {TAB}{KEY}'.format(LVL=level, TAB=myTAB, TYPE=thisTYPE, KEY=key)

            line0 = ''
            if 'L' in whatPrint: line0 = '[{LVL:2}]'.format(LVL=level)
            if 'T' in whatPrint: line0 = '{LINE0} {TYPE:<8}'.format(LINE0=line0, TYPE=thisTYPE)
            if 'K' in whatPrint: line0 = '{LINE0} {TAB}{KEY}'.format(LINE0=line0, TAB=myTAB, KEY=key)
            DICT_LINE(line0, tab=4)
            # LINEDATA_LIST.append(line0)
            # ---- recursive iteration
            PrintDictionary(val, myDictTYPES=myDictTYPES, keyList=keyList, level=level+1, whatPrint=whatPrint, fPRINT=fPRINT, maxDepth=maxDepth)    # in questo caso il return value non mi interessa

        else:
            getDictValue(key, val, level, myDictTYPES, whatPrint=whatPrint, fPRINT=True)


    if level == 0:
        if fEXIT:
            PrintHeader('END - ', header, stackLevel=stackLevel+1)
            sys.exit()
        else:
            # return LINEDATA_LIST
            return keyList
    else:
        print()
        return


# #######################################################
# #
# #######################################################
def PrintHeader(prefix, header, stackLevel=3):
    # from inspect import currentframe, getframeinfo
    # import traceback
    # message='ciao'
    # print (getframeinfo(currentframe()).filename + ':' + str(getframeinfo(currentframe()).lineno) + ' - ', message)
    # traceback.print_exc()
    try:
        # caller = inspect.trace()[stackLevel]
        caller = inspect.stack()[stackLevel]
        dummy, fileName, funcLineNO, funcName, lineCode, rest = caller

        # da errore su window anche se non sempre
    except:
        fileName    = sys._getframe(stackLevel).f_code.co_filename
        funcLineNO  = sys._getframe(stackLevel).f_lineno
        funcName    = sys._getframe(stackLevel).f_code.co_name
        lineCode    = ['dummy line. real line was not detected']

    finally:
        fName       = os.path.basename( fileName.split('.')[0])
        if funcName == '<module>': funcName = '__main__'
        caller = "Called by: [{FNAME}.{FUNC}:{LINEO}]".format(FNAME=fName, FUNC=funcName, LINEO=funcLineNO)


        # ---- Cerchiamo di catturare il dictionary richiamato
        # ---- da verificare con attenzione
    if not header:
        if '.PrintTreez' in lineCode[0]:
            dictionaryName = (lineCode[0].split('.PrintTree')[0].split()[-1])
            header = "dictionary: {0}".format(dictionaryName)
        else:
            header = "lineCode: {0}...".format(lineCode[0].strip()[:40])


    print()
    cPrint.Cyan("*"*60, tab=8)
    cPrint.Cyan("*     {0}".format(caller), tab=8)
    if header: cPrint.Cyan("*     {0}{1}".format(prefix, header), tab=8)
    cPrint.Cyan("*"*60, tab=8)




# #######################################################
# # Stampa i soli valori contenuti in un ramo, indicato
# #  da dotQualifers, partendo dal dict myDictRoot
# #######################################################
def getDictValue(key, value, level, myDictTYPES, whatPrint='LT', fPRINT=True):

    # level = 0
    myTAB=' '*4*level

        # - dict forzato nell'ordine di immissione
    retValue  = collections.OrderedDict()
    valueTYPE = str(type(value)).split("'")[1]
    listOfValue = []

    # ------------------------------
    # - valutazione del valore
    # ------------------------------
    if valueTYPE == 'str':
        s = value
        if s.find('\n') >= 0:
            listOfValue.extend(s.split('\n'))
        elif s.find(';') >= 0:
            listOfValue.extend(s.split(';'))
        else:
            STEP = 60
            while s:
                listOfValue.append(s[:STEP])
                s = s[STEP:]

    elif valueTYPE == 'list':
        listOfValue.append('[')
        """
            quanto segue NON va sempre bene in quanto potrebbe esserci una lista di liste...
            x = ['  ' + item for item in value]
            listOfValue.extend(x)
        """
            # indentiamo leggermete i valori
        for item in value:
            listOfValue.append(cPrint.getMagenta('   {0}'.format(item)))

        listOfValue.append(']')

    else:
        listOfValue.append(value)



    # =========================================
    # = P R I N T
    # =========================================
        # - print della riga con la key a lunghezza fissa baseStartValue
    baseStartValue = 52
    # line0 = '[{LVL:2}] {TYPE:<8} {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=valueTYPE, KEY=key)
    line0 = ''
    if 'L' in whatPrint: line0 = '[{LVL:2}]'.format(LVL=level)
    if 'T' in whatPrint: line0 = '{LINE0} {TYPE:<8}'.format(LINE0=line0, TYPE=valueTYPE)
    if 'K' in whatPrint: line0 = '{LINE0} {TAB}{KEY}'.format(LINE0=line0, TAB=myTAB, KEY=key)

    line0 = line0.ljust(baseStartValue)
    if not 'V' in whatPrint:
        VALUE_LINE(line0, tab=4)
        return

    VALUE_LINE(line0, tab=4, end='')

    VALUE_DATA (': ', end='')


        # - print del valore della prima entry della lista
    if len(listOfValue) == 0:
        line  = ''
        VALUE_DATA(line)

    else:
        line  = '{VAL}'.format(VAL=listOfValue[0])
        VALUE_DATA(line)

            # - print delle altre righe se presenti
        for line in listOfValue[1:]:
            line  = '{LINE:<{LUN}}  {VAL}'.format(LINE=' ', LUN=baseStartValue, VAL=line)
            VALUE_DATA(line, tab=4)
        else:
            retValue[key] = value




if __name__ == '__main__':

    example_dict = { 'key1' : 'value1',
                     'key2' : 'value2',
                     'key3' : { 'key3a': 'value3a' },
                     'key4' : {
                                'key4b': 'value4b',

                                'key4a':    {
                                                'key4aa': 'value4aa',
                                                'key4ab': 'value4ab',
                                                'key4ac': 'value4ac'
                                            },

                                'key4c' :   {
                                                'key4ca': 'value4ca'
                                            },
                            }
                    }


