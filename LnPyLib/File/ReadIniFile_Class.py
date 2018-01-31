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

# from  .. Logger.SetLogger import SetLogger
from  .. Logger.LnLogger import SetLogger
# from .. Logger.LnLogger_Class import SetLogger       # OK funziona dalla upperDir del package
from  .. Common.LnColor  import LnColor

class ReadIniFile(object):
    """docstring for ClassName"""
    def __init__(self, fileName, strict=True):
        self._filename                = str(fileName) # potrebbe essere della classe pathlib
        self._delimiters              = ('=', ':')
        self._comment_prefixes        = ('#',';')
        self._inline_comment_prefixes = (';',)
        self._strict                  = strict # True: impone unique key/session
        self._empty_lines_in_values   = True
        self._default_section         = 'DEFAULT'
        self._interpolation           = configparser.ExtendedInterpolation()
        self._returnRAW               = False
        self._returnOrderedDict       = False
        self._extraSections           = []
        self._allow_no_value          = False
        self._resolveEnvVars          = False
        self._fDEBUG                  = False
        self._subSectionChar          = []   # es ('\\', '/' , '.')
        self._exitOnError             = False
        self._SetLogger                 = SetLogger

        self._SetParser()



    def _SetParser(self):
            # Setting del parser
        self._configMain = configparser.ConfigParser(
                allow_no_value          = self._allow_no_value,
                delimiters              = self._delimiters,
                comment_prefixes        = self._comment_prefixes,
                inline_comment_prefixes = self._inline_comment_prefixes,
                strict                  = self._strict,
                empty_lines_in_values   = self._empty_lines_in_values,
                default_section         = self._default_section,
                interpolation           = self._interpolation
        )
        self._configMain.optionxform = str        # mantiene il case nei nomi delle section e delle Keys (Assicurarsi che i riferimenti a vars interne siano case-sensitive)


    def delimiters(self, delimiters):
        self._delimiters = delimiters
        self._SetParser()

    def commentPrefix(self, comment_prefixes):
        self._comment_prefixes = comment_prefixes
        self._SetParser()

    def extraSections(self, extraSections=[]):
        self._extraSections = extraSections

    def resolveEnvVars(self, flag):
        self._resolveEnvVars = flag

    def setDebug(self, flag):
        self._fDEBUG = flag

    def exitOnError(self, flag):
        self._exitOnError = flag

    def returnRAW(self, flag):
        self._returnRAW = flag

    # def setLogger(self, logger):
    #     self._logger = logger

    def subSectionChar(self, charList):
        if isinstance(charList, str):
            charList = [charList]
        self._subSectionChar = charsList




    # ######################################################
    # # https://docs.python.org/3/library/configparser.html
    # ######################################################
    def read(self, onlySection=None, returnOrderedDict=False, resolveEnvVars=False):
        logger  = self._SetLogger(package=__name__)
        self._onlySection       = onlySection
        self._returnOrderedDict = returnOrderedDict
        self._resolveEnvVars    = resolveEnvVars

        configMain = self._configMain

        try:
            data = codecs.open(self._filename, "r", "utf8")
            self._configMain.readfp(data)

        except (Exception) as why:
            print("Errore nella lettura del file: {FILE} - {WHY}".format(FILE=self._filename, WHY=str(why)))
            sys.exit(-1)

            # ------------------------------------------------------------------
            # - per tutte le sezioni che sono extra facciamo il merge.
            # - Se Key-Val esistono esse sono rimpiazzate
            # ------------------------------------------------------------------
        extraSections = self._extraSections
        for sectionName in self._extraSections:
            logger.info('adding Section: {SECTION}'.format(SECTION=sectionName))
            logger.info('          data: {EXTRA}'.format(EXTRA=extraSections[sectionName]))
            extraSection = extraSections[sectionName]

            if not self._configMain.has_section(sectionName):
                logger.debug('creating Section: {0}'.format(sectionName))
                self._configMain.add_section(sectionName)

            for key, val in extraSection.items():
                logger.debug('adding on Section {0}:'.format(sectionName))
                logger.debug('   key: {0}'.format(key))
                logger.debug('   val: {0}'.format(val))
                self._configMain.set(sectionName, key, val)



            # Parsing del file
        if type(self._configMain) in [configparser.ConfigParser]:
            self.dict = self._iniConfigAsDict()
        else:
            self.dict = self._configMain

        logger  = self._SetLogger(package=__name__, exiting=True)



    ############################################################
    # subSectionChar:  carattere da individuare nel nome della section per
    #                  interpretare la stessa come section+subsection
    ############################################################
    def _iniConfigAsDict(self):
        logger  = self._SetLogger(package=__name__)
        C = LnColor()
        """
        Converts a ConfigParser object into a dictionary.

        The resulting dictionary has sections as keys which point to a dict of the
        sections options as key => value pairs.
        """

        the_dict = collections.OrderedDict({}) if self._returnOrderedDict else {}

        try:
            for section in self._configMain.sections():
                # -----------------------------------------------------------------------
                # - questo blocco serve per splittare eventuali section in cui il nome
                # - contiene un separatore (es. '.') ed interpretarli come subSections
                # -----------------------------------------------------------------------
                if self._subSectionChar:
                    myStr = section
                    tempSep = '$@$@$'
                    for sep in self._subSectionChar:
                        myStr = myStr.replace(sep, tempSep)
                    # subSection = section.split(self._subSectionChar)
                    subSection = myStr.split(tempSep)

                else:
                    subSection = [section]  # una sola section

                currSECT = the_dict  # top
                for sect in subSection:
                    if not sect in currSECT:
                        currSECT[sect] = collections.OrderedDict({}) if self._returnOrderedDict else {}
                    currSECT = currSECT[sect] #  aggiorna pointer

                if self._fDEBUG:
                    print()
                    print('[{SECT}]'.format(SECT=section))


                # for key, val in self._configMain.items(section):
                for key, val in self._configMain.items(section, raw=self._returnRAW):

                    # ---------------------------------------------------------------
                    # - cerchiamo di risolvere eventuali variabili di ambiente
                    # - il nome dovrebbero essere solo i dispari della lista
                    # ---------------------------------------------------------------
                    if self._resolveEnvVars:
                        envVars = val.split('%')
                        for index, envVarName in enumerate(envVars):
                            if index%2:
                                # print(envVarName)
                                envVarValue = os.getenv(envVarName)
                                if envVarValue:
                                    val = val.replace('%{}%'.format(envVarName), envVarValue)
                                else:
                                    msg = 'nome della variabile di ambiente: [{VAR}] non trovato.'.format(VAR=envVarName)
                                    # C.Yellow(msg, tab=4)
                                    logger.warning(msg)
                                    if self._fDEBUG: C.Yellow(msg, tab=4)

                    currSECT[key] = val
                    if self._fDEBUG: print('    {KEY:<30} : {VAL}'.format(KEY=key, VAL=val))

        except (configparser.InterpolationMissingOptionError) as why:
            print("\n"*2)
            print("="*60)
            print("ERRORE nella validazione del file")
            print("-"*60)
            print(str(why))
            print("="*60)
            sys.exit(-2)

        except (Exception) as why:
            print("\n"*2)
            print("="*60)
            print("ERRORE nella validazione del file")
            print("-"*60)
            print(str(why))
            print("="*60)
            sys.exit(-2)


        if self._onlySection:
            retDict = the_dict[self._onlySection]
        else:
            retDict = the_dict

        logger  = self._SetLogger(package=__name__, exiting=True)
        return retDict

