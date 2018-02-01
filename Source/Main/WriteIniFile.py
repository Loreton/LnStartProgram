#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope: Lettura e scrittura di un file di configurazione nel formato INI
# ######################################################################################

import configparser
import collections

# ######################################################
# # writeIniFile(gv, fileName, configDict, INDENT=True)
# # gv          : global Variables
# # fileName    : nome del file da creare
# # configDict  : dictionary da scrivere (può essere di diversi tipi)
# # INDENT      : Scrive gli item cercando di ordinarli indentati
# ######################################################
def writeIniFile(gv, fileName, configDict, excludeSections=[], RAW=False, INDENT=False, REMOVE_BLANK_LINES=True):
    logger = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))


    logger.info('writing file: {}'.format(fileName))

    if isinstance(configDict, configparser.ConfigParser):
        data = configDict

    elif isinstance(configDict, collections.OrderedDict):
        data = configparser.ConfigParser()
        data.read_dict(configDict)


    else:
        print("{} - dataType NON SUPPORTATO".format(__name__))
        sys.exit()

    if INDENT:
        # print(fileName, RAW)
        try:
            MAX_KEY_LEN = getMaxKeyLen(data)
            FILE = open(fileName, "wb")
            for sectionName in sorted(data.sections()):
                if sectionName in excludeSections: continue
                sectionLine = '\n\n[{}]\n'.format(sectionName)                              # SECTION Line
                FILE.write(bytes(sectionLine, 'UTF-8'))
                for key, val in data.items(sectionName, raw=RAW):
                # sectID  = data[sectionName]
                # for key, val in sorted(sectID.items()):
                    indent = ' '*4
                    lines = val.split('\n')     # potrebbe essere multiline
                    if len(lines) > 1:
                        myLine = "{0}{1:{2}} = {3}\n".format(indent, key, MAX_KEY_LEN, lines[0])
                        indent = ' '*(4 + MAX_KEY_LEN + 2)     # imposto indent per all'ineamento al primo valore
                        for line in lines[1:]:      # ogni riga
                            if REMOVE_BLANK_LINES and line.strip() == '': continue
                            myLine += "{}{}\n".format(indent+' ', line)         # la aggiungiamo indentata al newVal

                        myLine += "\n"         # Una riga BLANk di separazione (solo dopo una MultiLine)

                    else:
                        myLine = '{0}{1:{2}} = {3}\n'.format(indent, key, MAX_KEY_LEN, val)

                    FILE.write(bytes(myLine, 'UTF-8'))

        except (configparser.InterpolationMissingOptionError) as why:
            print(gv.LN.cRED)
            print("\n"*2)
            print("="*60)
            print("ERRORE nella validazione del file:\n{}".format(gv.LN.cYELLOW + data))
            print("-"*60)
            print(gv.LN.cRED + str(why))
            print("="*60)
            gv.LN.exit(gv, 1501, "ERRORE nella validazione del file:\n{}".format(data))

        finally:
            FILE.close()

    else:
        with open(fileName, 'w') as configfile:
            data.write(configfile)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))


# ######################################################
# # writeIniFile(gv, fileName, configDict, INDENT=True)
# # gv          : global Variables
# # fileName    : nome del file da creare
# # configDict  : dictionary da scrivere (può essere di diversi tipi)
# # INDENT      : Scrive gli item cercando di ordinarli indentati
# ######################################################
def writeIniFile_LAST_OK(gv, fileName, configDict, INDENT=False, REMOVE_BLANK_LINES=True):
    logger = gv.LN.logger.setLogger(gv, package=__name__)
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))


    logger.info('writing file: {}'.format(fileName))

    if isinstance(configDict, configparser.ConfigParser):
        data = configDict

    elif isinstance(configDict, collections.OrderedDict):
        data = configparser.ConfigParser()
        data.read_dict(configDict)


    else:
        print("{} - dataType NON SUPPORTATO".format(__name__))
        sys.exit()

    if INDENT:
        try:
            MAX_KEY_LEN = getMaxKeyLen(data)
            FILE = open(fileName, "wb")
            for sectionName in sorted(data.sections()):
                sectionLine = '\n\n[{}]\n'.format(sectionName)                              # SECTION Line
                FILE.write(bytes(sectionLine, 'UTF-8'))
                sectID  = data[sectionName]
                for key, val in sorted(sectID.items()):
                    indent = ' '*4
                    lines = val.split('\n')     # potrebbe essere multiline
                    if len(lines) > 1:
                        myLine = "{0}{1:{2}} = {3}\n".format(indent, key, MAX_KEY_LEN, lines[0])
                        indent = ' '*(4 + MAX_KEY_LEN + 2)     # imposto indent per all'ineamento al primo valore
                        for line in lines[1:]:      # ogni riga
                            if REMOVE_BLANK_LINES and line.strip() == '': continue
                            myLine += "{}{}\n".format(indent+' ', line)         # la aggiungiamo indentata al newVal

                        myLine += "\n"         # Una riga BLANk di separazione (solo dopo una MultiLine)

                    else:
                        myLine = '{0}{1:{2}} = {3}\n'.format(indent, key, MAX_KEY_LEN, val)

                    FILE.write(bytes(myLine, 'UTF-8'))

        except (configparser.InterpolationMissingOptionError) as why:
            print(gv.LN.cRED)
            print("\n"*2)
            print("="*60)
            print("ERRORE nella validazione del file:\n{}".format(gv.LN.cYELLOW + data))
            print("-"*60)
            print(gv.LN.cRED + str(why))
            print("="*60)
            gv.LN.exit(gv, 1501, "ERRORE nella validazione del file:\n{}".format(data))

        finally:
            FILE.close()

    else:
        with open(fileName, 'w') as configfile:
            data.write(configfile)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))


# ######################################################
def writeIniFile_OK(gv, fileName, configDict):
# ######################################################
    logger = gv.LN.logger.setLogger(gv, package=__name__)

    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))


    logger.info('writing file: {}'.format(fileName))
    with open(fileName, 'w') as configfile:
        configDict.write(configfile)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))


# ######################################################
def writeDictAsIniFile_OK(gv, fileName, myDict):
# ######################################################
    logger = gv.LN.logger.setLogger(gv, package=__name__)

    # print('......................', type(myDict))
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    parser = configparser.ConfigParser()
    parser.read_dict(myDict)

    logger.info('writing file: {}'.format(fileName))
    with open(fileName, 'w') as configfile:
        parser.write(configfile)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))



############################################################
#
############################################################
def getMaxKeyLen(config):
        # ------ TEST per verificare che non ci siano variabili irrisolte nel configParser - Devo trovare un'altra soluzione
    MAX_KEY_LEN = 0
    # try:
    for section in config.sections():
        sectID  = config[section]
        for key, val in sectID.items():
            keyLen = len(key)
            if keyLen > MAX_KEY_LEN: MAX_KEY_LEN = keyLen

    # except (configparser.InterpolationMissingOptionError) as why:
    #     print(gv.LN.cRED)
    #     print("\n"*2)
    #     print("="*60)
    #     print("ERRORE nella validazione del file:\n{}".format(gv.LN.cYELLOW + config))
    #     print("-"*60)
    #     print(gv.LN.cRED + str(why))
    #     print("="*60)
    #     gv.LN.exit(gv, 1501, "ERRORE nella validazione del file:\n{}".format(config))

    return MAX_KEY_LEN
