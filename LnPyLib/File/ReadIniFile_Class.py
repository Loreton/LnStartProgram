#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
# updated by Loreto: 24-10-2017 09.30.00
# ######################################################################################
import sys
import os

import collections
import configparser
import codecs

from pathlib import Path

from  .. Logger.LnLogger import SetLogger
from  .. Common.LnColor  import LnColor
from  .. Common.Exit     import Exit as LnExit

TAB = 4*' '
class ReadIniFile(object):
    """docstring for ClassName"""
    # def __init__(self, fileName, strict=True):

    def __init__(self,
                    fileName,
                    strict=True,
                    kvDelimiters=('=', ':'),
                    comment_prefixes=('#',';'),
                    inline_comment_prefixes=None,  # (';')
                    extraSections={},
                    subSectionChar=[],
                    resolveEnvVars=False,
                    ):

        assert type(kvDelimiters)           == list or type(kvDelimiters) == tuple
        assert type(comment_prefixes)       == list or type(comment_prefixes) == tuple

        self._filename                = str(fileName) # potrebbe essere della classe pathlib
        self._kvDelimiters            = kvDelimiters
        self._comment_prefixes        = comment_prefixes
        self._inline_comment_prefixes = inline_comment_prefixes
        self._strict                  = strict # True: impone unique key/session
        self._empty_lines_in_values   = True
        self._default_section         = 'DEFAULT'
        self._interpolation           = configparser.ExtendedInterpolation()
        self._returnRAW               = False
        # self._returnOrderedDict       = False
        self._allow_no_value          = False
        self._subSectionChar          = []   # es ('\\', '/' , '.')
        self._exitOnError             = False
        self._SetLogger               = SetLogger

        # self._onlySection       = onlySection
        self._subSectionChar    = subSectionChar
        self._resolveEnvVars    = resolveEnvVars
        self._extraSections     = extraSections

        self._myDict            = collections.OrderedDict # default

        self._SetParser()

        self._parsingFile()




    def _SetParser(self):
            # Setting del parser
        self._configMain = configparser.ConfigParser(
                allow_no_value          = self._allow_no_value,
                delimiters              = self._kvDelimiters,
                comment_prefixes        = self._comment_prefixes,
                inline_comment_prefixes = self._inline_comment_prefixes,
                strict                  = self._strict,
                empty_lines_in_values   = self._empty_lines_in_values,
                default_section         = self._default_section,
                interpolation           = self._interpolation
        )
        self._configMain.optionxform = str        # mantiene il case nei nomi delle section e delle Keys (Assicurarsi che i riferimenti a vars interne siano case-sensitive)





    # ######################################################
    # # https://docs.python.org/3/library/configparser.html
    # ######################################################
    def _parsingFile(self):
        logger  = self._SetLogger(package=__name__)
        logger.info("Reading ini file: {FILE}".format(FILE=self._filename))

        try:
            data = codecs.open(self._filename, "r", "utf8")
            self._configMain.readfp(data)

        except (Exception) as why:
            print(TAB, "Errore nella lettura del file: {FILE} - {WHY}".format(FILE=self._filename, WHY=str(why)))
            sys.exit(-1)

        if self._extraSections:
            self.updateSection(reqSections=self._extraSections)

        logger  = self._SetLogger(package=__name__, exiting=True)

    ############################################################
    #
    ############################################################
    def __getMaxKeyLen_Raw(self, data):
        MAX_KEY_LEN = 0
        for sectionName in data.sections():
            for key, val in data.items(sectionName, raw=True):
                keyLen = len(key)
                if keyLen > MAX_KEY_LEN: MAX_KEY_LEN = keyLen

        return MAX_KEY_LEN

    def exitOnError(self, flag):
        self._exitOnError = flag

    def returnRAW(self, flag):
        self._returnRAW = flag

    ############################################################
    # updateSection()
    #   add dictType-section to configparserType-section
    ############################################################
    def updateSection(self, reqSections={}):
        assert type(reqSections) ==  dict
        logger = SetLogger(package=__name__)
            # ------------------------------------------------------------------
            # - per tutte le sezioni che sono extra facciamo il merge.
            # - Se Key-Val esistono esse sono rimpiazzate
            # ------------------------------------------------------------------
        for sectionName in reqSections:
            logger.debug('adding Section: {SECTION}'.format(SECTION=sectionName))
            logger.debug('          data: {EXTRA}'.format(EXTRA=reqSections[sectionName]))
            extraSection = reqSections[sectionName]

            if not self._configMain.has_section(sectionName):
                logger.debug('creating Section: {0}'.format(sectionName))
                self._configMain.add_section(sectionName)

            for key, val in extraSection.items():
                logger.debug('adding on Section {0}:'.format(sectionName))
                logger.debug('   key: {0}'.format(key))
                logger.debug('   val: {0}'.format(val))
                if isinstance(val, int):
                    val = str(val)
                self._configMain.set(sectionName, key, val)

        return self.toDict(dictType=self._myDict)


    # def writeIniFile(gv, fileName, configDict, excludeSections=[], RAW=False, INDENT=False, REMOVE_BLANK_LINES=True):
    def updateFile(  self,
                newFileName=None,
                replace=False,
                backup=False,
                excludeSections=[],
                RAW=False,
                INDENT=False,
                REMOVE_BLANK_LINES=True):

        logger = SetLogger(package=__name__)

            # get fileName
        if newFileName:
            fileName = newFileName

        elif replace:
            fileName = self._filename

        else:
            LnExit(1002, "missing newFileName and replace==False")

            # if backup required
        if backup:
            myFile = Path(fileName)
            if myFile.is_file():
                myFile.LnBackup()

        logger.info('writing file: {}'.format(fileName))

        data = self._configMain
        FILE = None
        if INDENT:
            try:
                MAX_KEY_LEN = self.__getMaxKeyLen_Raw(data)
                FILE = open(fileName, "wb")
                for sectionName in sorted(data.sections()):
                    if sectionName in excludeSections: continue
                    sectionLine = '\n\n[{}]\n'.format(sectionName)                              # SECTION Line
                    FILE.write(bytes(sectionLine, 'UTF-8'))
                    for key, val in data.items(sectionName, raw=RAW):
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
                print(TAB, gv.LN.cRED)
                print(TAB, "\n"*2)
                print(TAB, "="*60)
                print(TAB, "- ERRORE nella validazione del file:\n{}".format(gv.LN.cYELLOW + data))
                print(TAB, "-"*60)
                print(TAB, gv.LN.cRED + str(why))
                print(TAB, "="*60)
                gv.LN.exit(gv, 1501, "ERRORE nella validazione del file:\n{}".format(data))

            finally:
                if FILE: FILE.close()

        else:
            with open(fileName, 'w') as outFile:
                data.write(outFile)


        self._SetLogger(package=__name__, exiting=True)




    ############################################################
    # update:
    ############################################################
    def update(self):
        logger = SetLogger(package=__name__)
        logger.info('writing file: {}'.format(self._filename))

        data = self._configMain

        with open(self._filename, 'w') as outFile:
            data.write(outFile)


        self._SetLogger(package=__name__, exiting=True)




    ############################################################
    # getAsDict
    ############################################################
    def toDict(self, dictType=None):
        """
        Converts a ConfigParser object into a dictionary.

        The resulting dictionary has sections as keys which point to a dict of the
        sections options as key => value pairs.
        """
        logger  = self._SetLogger(package=__name__)
        C = LnColor()

        if dictType: self._myDict = dictType

        # myDict = dictType if dictType else self._myDict
        retDict = self._myDict()
        logger.debug('requested dictType: {}'.format(retDict))

        try:
            for section in self._configMain.sections():
                logger.debug('')
                logger.debug('[{SECT}]'.format(SECT=section))
                # -----------------------------------------------------------------------
                # - questo blocco serve per splittare eventuali section in cui il nome
                # - contiene un separatore (es. '.') ed interpretarli come subSections
                # -----------------------------------------------------------------------
                if self._subSectionChar:
                    myStr = section
                    tempSep = '$@$@$'
                    for sep in self._subSectionChar:
                        myStr = myStr.replace(sep, tempSep)
                    subSection = myStr.split(tempSep)

                else:
                    subSection = [section]  # una sola section

                currSECT = retDict  # top
                for sect in subSection:
                    if not sect in currSECT:
                        currSECT[sect] = self._myDict()
                    currSECT = currSECT[sect] #  aggiorna pointer


                for key, val in self._configMain.items(section, raw=self._returnRAW):
                    # logger.debug('  {KEY:<30} = {VAL}'.format(KEY=key, VAL=val))

                    # ---------------------------------------------------------------
                    # - cerchiamo di risolvere eventuali variabili di ambiente
                    # - il nome dovrebbero essere solo i dispari della lista
                    # ---------------------------------------------------------------
                    if self._resolveEnvVars:
                        envVars = val.split('%')
                        for index, envVarName in enumerate(envVars):
                            if index%2:
                                # print(TAB, envVarName)
                                envVarValue = os.getenv(envVarName)
                                if envVarValue:
                                    val = val.replace('%{}%'.format(envVarName), envVarValue)
                                else:
                                    msg = 'nome della variabile di ambiente: [{VAR}] non trovato.'.format(VAR=envVarName)
                                    logger.warning(msg)

                    currSECT[key] = val
                    logger.debug('    {KEY:<30} = {VAL}'.format(KEY=key, VAL=val))

        except (Exception) as why:
            print(TAB, "\n"*2)
            print(TAB, "="*60)
            print(TAB, "- ERRORE nella validazione del file")
            print(TAB, "-"*60)
            print(TAB, '-', str(why))
            print(TAB, "="*60)
            sys.exit(-2)



        logger  = self._SetLogger(package=__name__, exiting=True)
        return retDict

