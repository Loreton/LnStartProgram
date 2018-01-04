#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import collections
import sys

# from LnLib.Common.LnColor  import LnColor
from  .. Common.LnColor import LnColor
cPrint=LnColor().printColored


# #######################################################
# # ''' RECURSIVE '''
# # Ritorna una lista che contiene
# # l'alberatura delle key di un dictionary
# #    [level - keyName ]
# #######################################################
def KeyTree(myDict, myDictTYPES=[], keyList=[], level=0, fPRINT=False):

    if level > 100:   # per sicurezza
        sys.exit()

    for key, val in myDict.items():                  # per tutte le chiavi del dict2
        valType = type(val)                            # otteniamo il TYPE

            # - Se è un DICT iteriamo
        if valType in myDictTYPES:
            entry = '{0} - {1}{2}'.format(level, level*' '*4, key)
            keyList.append(entry) #  ottendo una lista di tutte le entry
            if fPRINT: print (entry)
            KeyTree(val, myDictTYPES=myDictTYPES, keyList=keyList, level=level+1, fPRINT=fPRINT)    # in questo caso il return value non mi interessa

        else:
            ''' il valore ma non ci interessa... '''
            pass

    if not level == 0:
        return


    return keyList


# #######################################################
# # Ritorna una lista che contiene una lista di liste.
# #    [keya, keya1, keya2]
# #    [keyb, keyb1, keyb2]
# #    [.....]
# #######################################################
def KeyList(myDict, myDictTYPES=[]):
        # Leggiamo l'l'alberatura
    keyList = KeyTree(myDict, myDictTYPES=myDictTYPES)

    prevLevel = -1
    retLIST = []
    currPTR = []

    for line in keyList:
        if line.strip() == '':  continue
        level, item = line.split('-', 1)
        level = int(level.strip())
        item  = item.strip()

        if level == 0:        # siamo sulla root
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            currPTR = [item]
            prevLevel = 0

        elif level > prevLevel:    # andiamo in basso nella struttura
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            currPTR.append(item)
            prevLevel = level

        elif level == prevLevel:   # vuol dire che stiamo risalendo nella struttura
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            delta = 1
            currPTR = currPTR[:-delta]  # saliamo di un livello
            currPTR.append(item)    # aggiungiamo il current item

        elif level < prevLevel:   # vuol dire che stiamo risalendo nella struttura
            delta = prevLevel-level + 1
            if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # salviamo il precedente
            currPTR = currPTR[:-delta]  # saliamo di due livelli
            currPTR.append(item)    # aggiungiamo il current item
            prevLevel = level

    if currPTR and not currPTR in retLIST: retLIST.append(currPTR) # last entry
    retLIST.append([]) # inserisci la root
    return retLIST





# #######################################################
# # Stampa i soli valori contenuti in un ramo, indicato
# #  da dotQualifers, partendo dal dict myDictRoot
# #######################################################
def getValue(mainRootDict, listOfQualifiers, myDictTYPES, fPRINT=True):
    rootDict = mainRootDict
    level = 0
    myTAB=' '*4
    baseStartValue = 52
    for key in listOfQualifiers:
        rootDict = rootDict[key]
        thisTYPE = str(type(rootDict)).split("'")[1][-6:]
        if "DotMap" in thisTYPE: thisTYPE = 'LnDict'
        if fPRINT:
            line = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
            cPrint(C.YellowH, line, tab=4)
        level += 1

        # - dict forzato nell'ordine di immissione
    retValue = collections.OrderedDict()
    for key, val in rootDict.items():
        if key == '_myDictTYPES': continue
        if not type(val) in myDictTYPES:    # ignoriamo le entrate che sono dictionary
            retValue[key] = val
            if fPRINT:
                thisTYPE = str(type(val)).split("'")[1]
                line0 = '[{LVL:2}] - {TYPE:<8}- {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=thisTYPE, KEY=key)
                line  = '{LINE:<{LUN}}: {VAL}'.format(LINE=line0, LUN=baseStartValue, VAL=val)
                cPrint(C.greenH, line, tab=4)


    if fPRINT: print()
    return retValue



'''
# #######################################################
# # Stampa l'alberatura di un dict: mainDictRoot
# #######################################################
def PrintTree(mainRootDict, myDictTYPES):
    keyList = KeyList(mainRootDict, myDictTYPES=myDictTYPES)

    for listOfQualifiers in keyList:
        PrintValue(mainRootDict, listOfQualifiers, myDictTYPES)
'''


































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




    # keyTree = gv.song.dict.KeyTree(fPRINT=False)
    # for line in keyTree: print(line)

    # keyList = gv.song.dict.KeyList()
    # for line in keyList: print(line)

    # ptrDict = gv.song.dict.Ptr(['Bambini', "Canzoni sotto l'albero"])
    # ptrDict.PrintTree()

    # gv.song.dict.PrintTree(listOfQualifiers=['Bambini', "Canzoni sotto l'albero", 'Varie', 'Alla scoperta di Babbo NATALE'])